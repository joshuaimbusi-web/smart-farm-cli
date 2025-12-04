# models/sale.py
from datetime import date
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Column, Integer, ForeignKey, Float, Date
from sqlalchemy.orm import relationship, Session

from .base import Base

if TYPE_CHECKING:
    from .farmer import Farmer
    from .buyer import Buyer
    from .product_type import ProductType

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
    def create(cls, session: Session, farmer: 'Farmer', buyer: 'Buyer',
               product_type: Optional['ProductType'] = None,
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
