from typing import List, Optional
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship, Session
from .base import Base

class Cooperative(Base):
    __tablename__ = "cooperatives"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    memberships = relationship("Membership", back_populates="cooperative", cascade="all, delete-orphan")
    farmers = relationship("Farmer", secondary="memberships", viewonly=True)

    @classmethod
    def create(cls, session: Session, **kwargs) -> "Cooperative":
        c = cls(**kwargs)
        session.add(c)
        session.commit()
        return c

    @classmethod
    def get_all(cls, session: Session) -> List["Cooperative"]:
        return session.query(cls).order_by(cls.id).all()

    @classmethod
    def find_by_id(cls, session: Session, id_: int) -> Optional["Cooperative"]:
        return session.get(cls, id_)

    def delete(self, session: Session):
        session.delete(self)
        session.commit()
