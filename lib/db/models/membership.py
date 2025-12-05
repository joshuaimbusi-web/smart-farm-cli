# lib/db/models/membership.py
from datetime import date, datetime
from typing import Optional
from sqlalchemy import Column, Integer, ForeignKey, Date, DateTime, String, Text
from sqlalchemy.orm import relationship

from .base import Base


class Membership(Base):
    """
    Association-object linking Cooperative <-> Farmer with metadata (joined_on, role, approved_by, notes).
    """
    __tablename__ = "memberships"

    cooperative_id = Column(Integer, ForeignKey("cooperatives.id"), primary_key=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), primary_key=True)

    joined_on = Column(Date, default=date.today)
    role = Column(String(50), default="member")
    approved_by = Column(String(100), nullable=True)   # store approver name or user id string
    notes = Column(Text, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    cooperative = relationship("Cooperative", back_populates="memberships")
    farmer = relationship("Farmer", back_populates="memberships")
