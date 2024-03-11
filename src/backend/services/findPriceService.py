from typing import Optional, List

from src.backend.models import PriceMatrix, Category, Location, DiscountPriceMatrix, Segment
from sqlalchemy.orm import Session


class FindPriceService:

    @staticmethod
    def get_parent_locations(db: Session, location_id: int) -> List[int]:
        parent_ids = []
        current_location = db.query(Location).filter(Location.id == location_id).first()

        while current_location and current_location.parent_id:
            parent_ids.append(current_location.parent_id)
            current_location = db.query(Location).filter(Location.id == current_location.parent_id).first()

        return parent_ids

    @staticmethod
    def get_parent_categories(db: Session, category_id: int) -> List[int]:
        parent_ids = []
        current_category = db.query(Category).filter(Category.id == category_id).first()

        while current_category and current_category.parent_id:
            parent_ids.append(current_category.parent_id)
            current_category = db.query(Category).filter(Category.id == current_category.parent_id).first()

        return parent_ids

    def find_price(self, db: Session, location_id: int, category_id: int, user_segment_id: int) -> Optional[dict]:
        locations_to_check = [location_id] + self.get_parent_locations(db, location_id)
        categories_to_check = [category_id] + self.get_parent_categories(db, category_id)

        # Получаем ID скидочных матриц для сегмента пользователя
        discount_matrices_ids = db.query(Segment.discount_matrix_id).filter(Segment.id == user_segment_id).all()
        discount_matrices_ids = [dm[0] for dm in discount_matrices_ids]  # Преобразование в список ID

        for loc_id in locations_to_check:
            for cat_id in categories_to_check:
                # Проверяем скидочную матрицу для сегмента пользователя
                discount_matrix_price = db.query(DiscountPriceMatrix).filter(
                    DiscountPriceMatrix.id.in_(discount_matrices_ids),
                    DiscountPriceMatrix.location_id == loc_id,
                    DiscountPriceMatrix.category_id == cat_id
                ).first()
                if discount_matrix_price:
                    return {
                        "price": discount_matrix_price.price,
                        "location_id": loc_id,
                        "category_id": cat_id,
                        "matrix_id": discount_matrix_price.id,
                        "user_segment_id": user_segment_id
                    }

                # Если в скидочной нет, то ищем в базовой
                base_matrix_price = db.query(PriceMatrix).filter(
                    PriceMatrix.location_id == loc_id,
                    PriceMatrix.category_id == cat_id
                ).first()
                if base_matrix_price:
                    return {
                        "price": base_matrix_price.price,
                        "location_id": loc_id,
                        "category_id": cat_id,
                        "matrix_id": base_matrix_price.id,
                        "user_segment_id": user_segment_id
                    }

        return None
