from enum import Enum
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.backend.models import engine, UserAvito, PriceMatrix, DiscountPriceMatrix
from src.backend.services.findPriceService import FindPriceService

app = FastAPI()
find_price_service = FindPriceService()


class PriceQuery(BaseModel):
    location_id: int
    category_id: int
    user_id: int


class PriceResponse(BaseModel):
    price: int
    location_id: int
    category_id: int
    user_segment_id: int


class MatrixType(str, Enum):
    Base = "Base"
    Discount = "Discount"



def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


@app.post("/get-price", response_model=PriceResponse)
def get_price(query: PriceQuery, db: Session = Depends(get_db)):
    user = db.query(UserAvito).filter(UserAvito.id == query.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    price_info = find_price_service.find_price(db, query.location_id, query.category_id, user.segment_id)

    if price_info:
        return PriceResponse(**price_info)

    raise HTTPException(status_code=404, detail="Price not found")


# @app.post("/post_matrix")
# def post_matrix(request: PostMatrixRequest, db: Session = Depends(get_db)):
#     # Надо реализовать добавление
#     pass


@app.get("/get_matrix")
def get_matrix(matrix_type: MatrixType, id: Optional[int] = None, db: Session = Depends(get_db)):
    if matrix_type == MatrixType.Base:
        query = db.query(PriceMatrix)
    else:  # MatrixType.Discount
        query = db.query(DiscountPriceMatrix)

    if id is not None:
        query = query.filter_by(id=id)

    result = query.all()
    return [
        {"id": matrix.id, "location_id": matrix.location_id, "category_id": matrix.category_id, "price": matrix.price}
        for matrix in result]


# @app.get("/get_locs", response_model=List[dict])
# def get_locs(request: GetLocationsRequest, db: Session = Depends(get_db)):
#     pass
#
#
# @app.get("/get_cats", response_model=List[dict])
# def get_cats(request: GetCategoriesRequest, db: Session = Depends(get_db)):
#     pass
