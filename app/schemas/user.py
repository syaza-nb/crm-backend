
import uuid
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.schemas.common import TimestampSchema


class UserCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role_id: uuid.UUID


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=150)
    email: EmailStr | None = None
    role_id: uuid.UUID | None = None
    is_active: bool | None = None


class UserResponse(TimestampSchema):
    id: uuid.UUID
    role_id: uuid.UUID
    full_name: str
    email: EmailStr
    is_active: bool


class RoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
