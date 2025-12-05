from typing import List, Optional
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship, Session
from .base import Base

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
