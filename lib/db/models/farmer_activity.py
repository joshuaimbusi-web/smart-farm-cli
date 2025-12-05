# lib/db/models/farmer_activity.py
from datetime import date, datetime
from typing import Optional
from sqlalchemy import Column, Integer, ForeignKey, Date, DateTime, String, Text, Float
from sqlalchemy.orm import relationship, Session

from .base import Base


class FarmerActivity(Base):
    """
    Association-object linking Farmer <-> Activity with metadata.
    """
    __tablename__ = "farmer_activities"

    id = Column(Integer, primary_key=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)

    # metadata fields
    joined_on = Column(Date, default=date.today)
    role = Column(String(50), default="participant")   # e.g., leader, participant
    progress_percent = Column(Float, default=0.0)      # 0.0 - 100.0
    notes = Column(Text, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships back to parent objects
    farmer = relationship("Farmer", back_populates="farmer_activities")
    activity = relationship("Activity", back_populates="farmer_activities")

    @classmethod
    def create(cls, session: Session, farmer, activity,
               joined_on: Optional[date] = None,
               role: Optional[str] = None,
               progress_percent: float = 0.0,
               notes: Optional[str] = None) -> "FarmerActivity":
        fa = cls(
            farmer=farmer,
            activity=activity,
            joined_on=(joined_on or date.today()),
            role=(role or "participant"),
            progress_percent=progress_percent,
            notes=notes,
        )
        session.add(fa)
        session.commit()
        return fa

    @classmethod
    def find_by_id(cls, session: Session, id_: int):
        return session.get(cls, id_)

    @classmethod
    def list_for_farmer(cls, session: Session, farmer_id: int):
        return session.query(cls).filter(cls.farmer_id == farmer_id).all()

    @classmethod
    def list_for_activity(cls, session: Session, activity_id: int):
        return session.query(cls).filter(cls.activity_id == activity_id).all()

    def delete(self, session: Session):
        session.delete(self)
        session.commit()

    def update_progress(self, session: Session, new_percent: float, notes: Optional[str] = None):
        self.progress_percent = float(new_percent)
        if notes is not None:
            self.notes = notes
        self.last_updated = datetime.utcnow()
        session.add(self)
        session.commit()
        return self
