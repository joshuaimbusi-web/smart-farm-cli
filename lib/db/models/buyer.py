# models/buyer.py
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship, Session

from .base import Base

if TYPE_CHECKING:
    from .sale import Sale

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
