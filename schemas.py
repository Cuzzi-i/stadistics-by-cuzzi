from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Dict
from datetime import datetime

class EventBase(BaseModel):
    """
    Base schema for events
    """
    user_id: str
    event_type: str
    event_metadata: Optional[Dict] = Field(default=None, alias="metadata")

class EventCreate(EventBase):
    model_config = ConfigDict(populate_by_name=True)

class Event(EventBase):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)