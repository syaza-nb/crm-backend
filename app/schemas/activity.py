
import uuid
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from app.schemas.common import TimestampSchema


class ActivityType(str, Enum):
    CALL = "call"
    EMAIL = "email"
    MEETING = "meeting"
    NOTE = "note"
    OTHER = "other"


class ActivityCreate(BaseModel):
    activity_type: ActivityType
    subject: str = Field(min_length=1, max_length=200)
    description: str | None = None
    activity_date: datetime
    contact_ids: list[uuid.UUID] = Field(default_factory=list)
    company_ids: list[uuid.UUID] = Field(default_factory=list)
    deal_ids: list[uuid.UUID] = Field(default_factory=list)


class ActivityUpdate(BaseModel):
    activity_type: ActivityType | None = None
    subject: str | None = None
    description: str | None = None
    activity_date: datetime | None = None
    contact_ids: list[uuid.UUID] | None = None
    company_ids: list[uuid.UUID] | None = None
    deal_ids: list[uuid.UUID] | None = None


class ActivityResponse(TimestampSchema):
    id: uuid.UUID
    created_by: uuid.UUID
    activity_type: ActivityType
    subject: str
    description: str | None
    activity_date: datetime
