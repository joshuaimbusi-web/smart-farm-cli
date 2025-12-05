from datetime import date
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Column, Integer, String, Text, Date
from sqlalchemy.orm import relationship, validates, Session
from .base import Base

if TYPE_CHECKING:
    from .farmer import Farmer
    from .farmer_activity import FarmerActivity

class Activity(Base):
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)

    farmers = relationship('Farmer', back_populates='activity', cascade='all, delete-orphan')
    farmer_activities = relationship("FarmerActivity", back_populates="activity", cascade="all, delete-orphan")
    farmers_list = relationship("Farmer", secondary="farmer_activities", viewonly=True)

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
