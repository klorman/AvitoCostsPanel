from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
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


class PriceMatrix(Base):
    __tablename__ = 'price_matrix'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    price = Column(Integer)


class DiscountPriceMatrix(Base):
    __tablename__ = 'discount_price_matrix'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    price = Column(Integer)


class UserAvito(Base):
    __tablename__ = 'user_avito'
    id = Column(Integer, primary_key=True)
    segment_id = Column(Integer, ForeignKey('segments.id'))
    segment = relationship('Segment', backref='users')


class Segment(Base):
    __tablename__ = 'segments'
    id = Column(Integer, primary_key=True)
    discount_matrix_id = Column(Integer, ForeignKey('discount_price_matrix.id'))
    discount_matrix = relationship('DiscountPriceMatrix', backref='segment')



engine = create_engine('postgresql://postgres:123456@localhost:2345/postgres')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
