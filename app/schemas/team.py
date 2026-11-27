
import uuid
from pydantic import BaseModel, Field
from app.schemas.common import TimestampSchema


class TeamCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    manager_id: uuid.UUID | None = None


class TeamUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    manager_id: uuid.UUID | None = None


class TeamMemberAdd(BaseModel):
    user_id: uuid.UUID


class TeamResponse(TimestampSchema):
    id: uuid.UUID
    name: str
    manager_id: uuid.UUID | None


class TeamMemberResponse(BaseModel):
    team_id: uuid.UUID
    user_id: uuid.UUID
