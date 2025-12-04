from datetime import date
from typing import List, Optional
from sqlalchemy import Integer, String, Text, Date, Column, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship, Session, validates
from .database import engine, SessionLocal

Base = declarative_base()


class Activity(Base):
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)

    farmers = relationship('Farmer', back_populates='activity', cascade='all, delete-orphan')

    @validates('name')
    def validate_name(self, key, value):
        value = (value or '').strip()
        if not value:
            raise ValueError('Activity name cannot be empty')
        return value

    @classmethod
    def create(cls, session: Session, **kwargs) -> 'Activity':
        a = cls(**kwargs)
        session.add(a)
        session.commit()
        return a

    @classmethod
    def get_all(cls, session: Session) -> List['Activity']:
        return session.query(cls).order_by(cls.id).all()

    @classmethod
    def find_by_id(cls, session: Session, id_: int) -> Optional['Activity']:
        return session.get(cls, id_)

    def delete(self, session: Session):
        session.delete(self)
        session.commit()


class Farmer(Base):
    __tablename__ = 'farmers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    farm_name = Column(String(50))
    national_id = Column(String(50), unique=True, nullable=False)
    phone = Column(String(30))
    email = Column(String(50))
    address = Column(Text)
    activity_id = Column(Integer, ForeignKey('activities.id'))
    registration_date = Column(Date, default=date.today)

    activity = relationship('Activity', back_populates='farmers')
    sales = relationship('Sale', back_populates='farmer', cascade='all, delete-orphan')

    @validates('national_id')
    def validate_national_id(self, key, value):
        if not value or not value.strip():
            raise ValueError('national_id is required')
        return value.strip()

    @classmethod
    def create(cls, session: Session, **kwargs) -> 'Farmer':
        f = cls(**kwargs)
        session.add(f)
        session.commit()
        return f

    @classmethod
    def get_all(cls, session: Session) -> List['Farmer']:
        return session.query(cls).order_by(cls.id).all()

    @classmethod
    def find_by_id(cls, session: Session, id_: int) -> Optional['Farmer']:
        return session.get(cls, id_)

    @classmethod
    def find_by_name(cls, session: Session, name: str) -> List['Farmer']:
        return session.query(cls).filter(cls.name.ilike(f"%{name}%")).all()

    def delete(self, session: Session):
        session.delete(self)
        session.commit()


class Buyer(Base):
    __tablename__ = 'buyers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    organization = Column(String(50))
    contact_phone = Column(String(30))
    contact_email = Column(String(50))
    address = Column(Text)
    preferred_payment_method = Column(String(50))

    sales = relationship('Sale', back_populates='buyer', cascade='all, delete-orphan')

    @classmethod
    def create(cls, session: Session, **kwargs) -> 'Buyer':
        b = cls(**kwargs)
        session.add(b)
        session.commit()
        return b

    @classmethod
    def get_all(cls, session: Session) -> List['Buyer']:
        return session.query(cls).order_by(cls.id).all()

    @classmethod
    def find_by_id(cls, session: Session, id_: int) -> Optional['Buyer']:
        return session.get(cls, id_)

    def delete(self, session: Session):
        session.delete(self)
        session.commit()


class ProductType(Base):
    __tablename__ = 'product_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    category = Column(String(50))
    typical_unit = Column(String(50))
    description = Column(Text)

    sales = relationship('Sale', back_populates='product_type')

    @classmethod
    def create(cls, session: Session, **kwargs) -> 'ProductType':
        p = cls(**kwargs)
        session.add(p)
        session.commit()
        return p

    @classmethod
    def get_all(cls, session: Session) -> List['ProductType']:
        return session.query(cls).order_by(cls.id).all()

    @classmethod
    def find_by_id(cls, session: Session, id_: int) -> Optional['ProductType']:
        return session.get(cls, id_)

    def delete(self, session: Session):
        session.delete(self)
        session.commit()


class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    farmer_id = Column(Integer, ForeignKey('farmers.id'))
    buyer_id = Column(Integer, ForeignKey('buyers.id'))
    product_type_id = Column(Integer, ForeignKey('product_types.id'), nullable=True)
    quantity = Column(Float, default=0.0)
    price = Column(Float, default=0.0)
    created_at = Column(Date, default=date.today)

    farmer = relationship('Farmer', back_populates='sales')
    buyer = relationship('Buyer', back_populates='sales')
    product_type = relationship('ProductType', back_populates='sales')

    @classmethod
    def create(cls, session: Session, farmer: Farmer, buyer: Buyer,
               product_type: Optional[ProductType] = None,
               quantity: float = 0.0, price: float = 0.0) -> 'Sale':
        s = cls(farmer=farmer, buyer=buyer, product_type=product_type, quantity=quantity, price=price)
        session.add(s)
        session.commit()
        return s

    @classmethod
    def get_all(cls, session: Session) -> List['Sale']:
        return session.query(cls).order_by(cls.id).all()

    @classmethod
    def find_by_id(cls, session: Session, id_: int) -> Optional['Sale']:
        return session.get(cls, id_)

    def delete(self, session: Session):
        session.delete(self)
        session.commit()


# --- Helper function to create tables ---
def init_db():
    Base.metadata.create_all(engine)
