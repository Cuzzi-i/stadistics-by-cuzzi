from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime, timezone
from database import Base

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    event_type = Column(String, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    event_metadata = Column("metadata", JSON)