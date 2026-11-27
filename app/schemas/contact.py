
import uuid
from pydantic import BaseModel, EmailStr, Field
from app.schemas.common import TimestampSchema


class ContactCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=30)
    job_title: str | None = Field(default=None, max_length=150)
    company_ids: list[uuid.UUID] = Field(default_factory=list)


class ContactUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    job_title: str | None = None
    company_ids: list[uuid.UUID] | None = None


class ContactResponse(TimestampSchema):
    id: uuid.UUID
    owner_id: uuid.UUID
    first_name: str
    last_name: str
    email: EmailStr | None
    phone: str | None
    job_title: str | None
