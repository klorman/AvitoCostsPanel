from typing import Optional

from src.backend.models import BaselineMatrices, Category, Location, DiscountMatrices, Segment, UserAvito
from sqlalchemy.orm import Session


class FindPriceService:

    @staticmethod
    def get_parent_location(db: Session, location_id: int) -> Optional[int]:
        return db.query(Location.parent_id).filter(Location.id == location_id).scalar()

    @staticmethod
    def get_parent_category(db: Session, category_id: int) -> Optional[int]:
        return db.query(Category.parent_id).filter(Category.id == category_id).scalar()

    def find_price(self, db: Session, location_id: int, category_id: int, user_id: int, baseline_matrix_id: int) -> \
    Optional[dict]:
        # Получаем ID сегментов пользователя
        user_segments_ids = [us[0] for us in db.query(UserAvito.segment_id).filter(UserAvito.user_id == user_id).all()]

        # Получаем ID скидочных матриц для сегмента пользователя
        discount_matrices_ids = db.query(Segment.discount_matrix_id).filter(Segment.id.in_(user_segments_ids)).order_by(
            Segment.id.desc()).all()
        discount_matrices_ids = [dm[0] for dm in discount_matrices_ids]  # Преобразование в список ID

        for discount_matrix_id in discount_matrices_ids:
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
                        segment = db.query(Segment).filter(Segment.discount_matrix_id == discount_matrix_id).first()
                        return {
                            "price": discount_matrix.price,
                            "location_id": location_to_check,
                            "category_id": category_to_check,
                            "matrix_id": discount_matrix.matrix_id,
                            "user_segment_id": segment.id
                        }
                    category_to_check = self.get_parent_category(db, category_to_check)
                location_to_check = self.get_parent_location(db, location_to_check)

        # Если в скидочных нет, то ищем в базовой
        baseline_matrix = db.query(BaselineMatrices).filter(
            BaselineMatrices.matrix_id == baseline_matrix_id,
            BaselineMatrices.location_id == location_id,
            BaselineMatrices.category_id == category_id
        ).first()
        if baseline_matrix:
            segment = db.query(Segment).filter(Segment.discount_matrix_id == discount_matrix_id).first()
            return {
                "price": baseline_matrix.price,
                "location_id": location_id,
                "category_id": category_id,
                "matrix_id": baseline_matrix.matrix_id,
                "user_segment_id": segment.id
            }

        # Если в базовой, вдруг, нет, то возвращаем None
        return None
