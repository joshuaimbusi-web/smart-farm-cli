from datetime import date
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship, validates, Session

from .base import Base

if TYPE_CHECKING:
    from .activity import Activity
    from .sale import Sale
    from .farmer_activity import FarmerActivity
    from .cooperative import Cooperative
    from .membership import Membership


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

    # One-to-many: existing activity FK
    activity = relationship('Activity', back_populates='farmers')

    # One-to-many sales
    sales = relationship('Sale', back_populates='farmer', cascade='all, delete-orphan')

    # --- Many-to-many dashboard via FarmerActivity ---
    farmer_activities = relationship("FarmerActivity", back_populates="farmer", cascade="all, delete-orphan")
    activities = relationship("Activity", secondary="farmer_activities", viewonly=True)

    # --- Cooperative membership (association-object) ---
    memberships = relationship("Membership", back_populates="farmer", cascade="all, delete-orphan")
    cooperatives = relationship("Cooperative", secondary="memberships", viewonly=True)

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
