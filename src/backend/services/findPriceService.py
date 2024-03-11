from typing import Optional

from src.backend.models import PriceMatrix, Category, Location, DiscountPriceMatrix, Segment
from sqlalchemy.orm import Session


class FindPriceService:

    @staticmethod
    def get_parent_location(db: Session, location_id: int) -> Optional[int]:
        return db.query(Location.parent_id).filter(Location.id == location_id).scalar()
    
    @staticmethod
    def get_parent_category(db: Session, category_id: int) -> Optional[int]:
        return db.query(Category.parent_id).filter(Category.id == category_id).scalar()

    def find_price(self, db: Session, location_id: int, category_id: int, user_segment_id: int) -> Optional[dict]:
        # Получаем ID скидочных матриц для сегмента пользователя
        discount_matrices_ids = db.query(Segment.discount_matrix_id).filter(Segment.id == user_segment_id).order_by(Segment.discount_matrix_id.desc()).all()
        discount_matrices_ids = [dm[0] for dm in discount_matrices_ids]  # Преобразование в список ID

        for discount_matrix_id in discount_matrices_ids:
            location_to_check = location_id
            category_to_check = category_id
            
            while location_to_check:
                while category_to_check:
                    # Проверяем скидочную матрицу для сегмента пользователя
                    discount_matrix_price = db.query(DiscountPriceMatrix).filter(
                        DiscountPriceMatrix.id == discount_matrix_id,
                        DiscountPriceMatrix.location_id == location_to_check,
                        DiscountPriceMatrix.category_id == category_to_check
                    ).first()
                    if discount_matrix_price:
                        return {
                            "price": discount_matrix_price.price,
                            "location_id": location_to_check,
                            "category_id": category_to_check,
                            "matrix_id": discount_matrix_price.id,
                            "user_segment_id": user_segment_id
                        }
                    category_to_check = self.get_parent_category(db, category_to_check)
                location_to_check = self.get_parent_location(db, location_to_check)

        # Если в скидочных нет, то ищем в базовой
        base_matrix_price = db.query(PriceMatrix).filter(
            PriceMatrix.location_id == location_id,
            PriceMatrix.category_id == category_id
        ).first()
        if base_matrix_price:
            return {
                "price": base_matrix_price.price,
                "location_id": location_id,
                "category_id": category_id,
                "matrix_id": base_matrix_price.id,
                "user_segment_id": user_segment_id
            }

        # Если в базовой, вдруг, нет, то возвращаем None
        return None
