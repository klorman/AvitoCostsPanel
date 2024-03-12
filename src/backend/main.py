from enum import Enum
from typing import Optional, List

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from models import engine, UserAvito, BaselineMatrices, DiscountMatrices, Location
from services.findPriceService import FindPriceService
from services.price_crud_service import PriceCRUDService

app = FastAPI()
find_price_service = FindPriceService()
crud_service = PriceCRUDService()


CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PATCH',
    'PUT',
    'DELETE'
]

CORS_ALLOW_HEADERS = [
    'Content-Type',
    'Set-Cookie',
    'Access-Control-Allow-Headers',
    'Access-Control-Allow-Origin',
    'Authorization'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)


class PriceQuery(BaseModel):
    location_id: int
    category_id: int
    user_id: int


class PriceResponse(BaseModel):
    price: int
    location_id: int
    category_id: int
    user_segment_id: int


class MatrixResponse(BaseModel):
    matrix_id: int
    matrix_type: str


class LocationResponse(BaseModel):
    loc_id: int
    loc_name: str


# Заменить на цифры
class MatrixType(str, Enum):
    Base = 0
    Discount = 1


def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


@app.get("/get-price", response_model=PriceResponse)
def get_price(query: PriceQuery, db: Session = Depends(get_db)):
    user = db.query(UserAvito).filter(UserAvito.user_id == query.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    max_matrix_id = db.query(func.max(BaselineMatrices.matrix_id)).scalar()
    price_info = find_price_service.find_price(db, query.location_id, query.category_id, user.user_id, max_matrix_id)

    if price_info:
        return PriceResponse(**price_info)

    raise HTTPException(status_code=404, detail="Price not found")


@app.get("/get_matrix")
def get_matrix(matrix_type: MatrixType, id: Optional[int] = None, db: Session = Depends(get_db)):
    if matrix_type == MatrixType.Base:
        query = db.query(BaselineMatrices)
    else:  # MatrixType.Discount
        query = db.query(DiscountMatrices)

    if id is not None:
        query = query.filter_by(matrix_id=id)

    result = query.all()
    return [
        {"id": matrix.id, "location_id": matrix.location_id, "category_id": matrix.category_id, "price": matrix.price}
        for matrix in result]


@app.get("/count_prices_test")
def count_prices(db: Session = Depends(get_db), id: Optional[int] = None):
    crud_service.init_calculated_prices(db, id)


@app.get("/get_new_price_func_test")
def get_new_price_func(db: Session = Depends(get_db), location: Optional[int] = None, category: Optional[int] = None,
                       user_id: Optional[int] = None):
    price = crud_service.get_price(db, location, category, user_id)
    return [
        {
            "price": price
        }
    ]


@app.get("/matrix", response_model=List[MatrixResponse])
def get_matrix(db: Session = Depends(get_db)):
    baseline_matrices = db.query(BaselineMatrices.matrix_id).distinct().all()
    discount_matrices = db.query(DiscountMatrices.matrix_id).distinct().all()
    result = [{"id": m[0], "matrix_type": "Base"} for m in baseline_matrices] + \
             [{"id": m[0], "matrix_type": "Discount"} for m in discount_matrices]
    return result


@app.get("/location", response_model=List[LocationResponse])
def get_location(matrix_id: int, matrix_type: int, db: Session = Depends(get_db)):
    if matrix_type == 0:
        matrix_model = BaselineMatrices
    elif matrix_type == 1:
        matrix_model = DiscountMatrices
    else:
        raise HTTPException(status_code=400, detail="Invalid matrix type")

    locations = db.query(matrix_model.location_id, Location.name).join(Location,
                                                                       matrix_model.location_id == Location.id).filter(
        matrix_model.matrix_id == matrix_id).distinct().all()

    return [{"id": loc[0], "name": loc[1]} for loc in locations]

# @app.get("/get_locs", response_model=List[dict])
# def get_locs(request: GetLocationsRequest, db: Session = Depends(get_db)):
#     pass
#
#
# @app.get("/get_cats", response_model=List[dict])
# def get_cats(request: GetCategoriesRequest, db: Session = Depends(get_db)):
#     pass
