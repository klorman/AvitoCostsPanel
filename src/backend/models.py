from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey('locations.id'))
    parent = relationship('Location', remote_side=[id], backref='children')


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey('categories.id'))
    parent = relationship('Category', remote_side=[id], backref='children')


class BaselineMatrices(Base):
    __tablename__ = 'baseline_matrices'
    id = Column(Integer, primary_key=True)
    matrix_id = Column(Integer)
    location_id = Column(Integer, ForeignKey('locations.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    price = Column(Integer)
    __table_args__ = (
        UniqueConstraint('matrix_id', 'location_id', 'category_id', name='unique_matrix_location_category'),
    )


class DiscountMatrices(Base):
    __tablename__ = 'discount_matrices'
    id = Column(Integer, primary_key=True)
    matrix_id = Column(Integer)
    location_id = Column(Integer, ForeignKey('locations.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    price = Column(Integer)
    __table_args__ = (
        UniqueConstraint('matrix_id', 'location_id', 'category_id',
                         name='unique_matrix_location_category_for_discount_matrix'),
    )


class CalculatedPrices(Base):
    __tablename__ = 'calculated_prices'
    id = Column(Integer, primary_key=True)
    discount_matrix_id = Column(Integer, ForeignKey('segments.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    price = Column(Integer)
    __table_args__ = (
        UniqueConstraint('discount_matrix_id', 'location_id', 'category_id', name='unique_discount_location_category'),
    )


class UserAvito(Base):
    __tablename__ = 'user_avito'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    segment_id = Column(Integer, ForeignKey('segments.id'))  # может быть несколько сегментов


class Segment(Base):
    __tablename__ = 'segments'
    id = Column(Integer, primary_key=True)
    discount_matrix_id = Column(Integer)  # один сегмент - одна матрица


engine = create_engine('postgresql://postgres:123456@localhost:2345/postgres')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
