from typing import Optional, List

from src.backend.models import BaselineMatrices, Category, Location, DiscountMatrices, Segment, UserAvito, \
    CalculatedPrices
from sqlalchemy.orm import Session


class PriceCRUDService:

    @staticmethod
    def get_parent_location(db: Session, location_id: int) -> Optional[int]:
        return db.query(Location.parent_id).filter(Location.id == location_id).scalar()

    @staticmethod
    def check_is_category_parents_discount_exists(db: Session, location_id: int, category_id: int,
                                                  discount_matrix_id: int) -> bool:
        discount_exists = db.query(DiscountMatrices).filter(
            DiscountMatrices.location_id == location_id,
            DiscountMatrices.category_id == category_id,
            DiscountMatrices.matrix_id == discount_matrix_id
        ).first()
        if discount_exists:
            return True

        parent_id = PriceCRUDService.get_parent_category(db, category_id)
        if parent_id:
            return False

        return PriceCRUDService.check_is_category_parents_discount_exists(db, location_id, parent_id,
                                                                          discount_matrix_id)

    @staticmethod
    def find_locations_for_price_update(db: Session, location_id: int, category_id: int, discount_matrix_id: int) -> \
            List[int]:
        child_locations = db.query(Location).filter(Location.parent_id == location_id).all()
        valid_child_ids = []

        for location in child_locations:
            discount_exists = PriceCRUDService.check_is_category_parents_discount_exists(db, location.id, category_id,
                                                                                         discount_matrix_id)

            if discount_exists:
                continue

            valid_child_ids.append(location.id)
            valid_child_ids.extend(
                PriceCRUDService.find_locations_for_price_update(db, location.id, category_id, discount_matrix_id))

        return valid_child_ids

    @staticmethod
    def get_parent_category(db: Session, category_id: int) -> Optional[int]:
        return db.query(Category.parent_id).filter(Category.id == category_id).scalar()

    @staticmethod
    def find_category_child_for_price_update(db: Session, category_id: int, location_id: int,
                                             discount_matrix_id: int) -> List[int]:
        child_categories = db.query(Category).filter(Category.parent_id == category_id).all()
        valid_child_ids = []

        for category in child_categories:
            discount_exists = db.query(DiscountMatrices).filter(
                DiscountMatrices.category_id == category.id,
                DiscountMatrices.location_id == location_id,
                DiscountMatrices.matrix_id == discount_matrix_id
            ).first()

            if discount_exists:
                continue

            valid_child_ids.append(category.id)
            valid_child_ids.extend(
                PriceCRUDService.find_category_child_for_price_update(db, category.id, category_id, discount_matrix_id))

        return valid_child_ids

    def find_price_by_discount_matrix(self, db: Session, location_id: int, category_id: int, discount_matrix_id: int) -> \
            Optional[dict]:
        location_to_check = location_id

        while location_to_check:
            category_to_check = category_id
            while category_to_check:
                # Проверяем скидочную матрицу для сегмента пользователя
                discount_matrix = db.query(DiscountMatrices).filter(
                    DiscountMatrices.matrix_id == discount_matrix_id,
                    DiscountMatrices.location_id == location_to_check,
                    DiscountMatrices.category_id == category_to_check
                ).first()
                if discount_matrix:
                    return discount_matrix.price

                category_to_check = self.get_parent_category(db, category_to_check)
            location_to_check = self.get_parent_location(db, location_to_check)

        # Если в скидочных нет, то ищем в базовой
        baseline_matrix = db.query(BaselineMatrices).filter(
            BaselineMatrices.matrix_id == self.baseline_matrix_id,
            BaselineMatrices.location_id == location_id,
            BaselineMatrices.category_id == category_id
        ).first()
        if baseline_matrix:
            return baseline_matrix.price

        # Если в базовой, вдруг, нет, то возвращаем None
        return None

    def update_calculated_child_prices(self, db: Session, location_id: int, category_id: int, discount_matrix_id: int,
                                       price: int, autocommit: bool = True):
        locations_ids = [location_id] + self.find_locations_for_price_update(db, location_id, category_id,
                                                                             discount_matrix_id)

        for current_location_id in locations_ids:
            categories_ids = [category_id] + self.find_category_child_for_price_update(db, category_id,
                                                                                       current_location_id,
                                                                                       discount_matrix_id)
            for current_category_id in categories_ids:
                calculated_price = db.query(CalculatedPrices).filter(
                    CalculatedPrices.discount_matrix_id == discount_matrix_id,
                    CalculatedPrices.location_id == current_location_id,
                    CalculatedPrices.category_id == current_category_id
                ).first()

                if calculated_price:
                    calculated_price.price = price

        if autocommit:
            db.commit()

    def create_discount_price(self, db: Session, location_id: int, category_id: int, discount_matrix_id: int,
                              price: int):
        new_discount_price = DiscountMatrices(
            matrix_id=discount_matrix_id,
            location_id=location_id,
            category_id=category_id,
            price=price
        )
        db.add(new_discount_price)  # Если уже есть, будет ошибка
        # db.commit()

        self.update_calculated_child_prices(db, location_id, category_id, discount_matrix_id, price)

    def update_discount_price(self, db: Session, location_id: int, category_id: int, discount_matrix_id: int,
                              price: int):
        discount_price = db.query(DiscountMatrices).filter(
            DiscountMatrices.matrix_id == discount_matrix_id,
            DiscountMatrices.location_id == location_id,
            DiscountMatrices.category_id == category_id
        ).first()

        if discount_price:
            discount_price.price = price
            # db.commit()

            self.update_calculated_child_prices(db, location_id, category_id, discount_matrix_id, price)

    def delete_discount_price(self, db: Session, location_id: int, category_id: int, discount_matrix_id: int):
        discount_price = db.query(DiscountMatrices).filter(
            DiscountMatrices.matrix_id == discount_matrix_id,
            DiscountMatrices.location_id == location_id,
            DiscountMatrices.category_id == category_id
        ).first()

        if discount_price:
            db.delete(discount_price)
            # db.commit()

            price = self.find_price_by_discount_matrix(db, location_id, category_id, discount_matrix_id)
            self.update_calculated_child_prices(db, location_id, category_id, discount_matrix_id, price)

    def init_calculated_prices(self, db: Session, baseline_matrix_id: int):
        self.baseline_matrix_id = baseline_matrix_id

        db.query(CalculatedPrices).delete()

        # TODO придумать более быстрый способ инициализации
        discount_matrices = db.query(DiscountMatrices).all()

        for line in discount_matrices:
            self.update_calculated_child_prices(db, line.location_id, line.category_id, line.matrix_id, line.price,
                                                autocommit=False)

        db.commit()

    def get_price(self, db: Session, location_id: int, category_id: int, user_id: int) -> Optional[int]:
        # Получаем ID сегментов пользователя
        user_segments_ids = db.query(UserAvito.segment_id).filter(UserAvito.user_id == user_id).all()

        # Получаем ID скидочных матриц для сегмента пользователя
        discount_matrices_ids = db.query(Segment.discount_matrix_id).filter(Segment.id.in_(user_segments_ids)).order_by(
            Segment.id.desc()).all()
        discount_matrices_ids = [dm[0] for dm in discount_matrices_ids]  # Преобразование в список ID

        for discount_matrix_id in discount_matrices_ids:
            calculated_price = db.query(CalculatedPrices.price).filter(
                CalculatedPrices.discount_matrix_id == discount_matrix_id,
                CalculatedPrices.location_id == location_id,
                CalculatedPrices.category_id == category_id
            ).first()
            if calculated_price:
                return {
                    "price": calculated_price
                }

        return None
