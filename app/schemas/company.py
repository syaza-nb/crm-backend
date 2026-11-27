
import uuid
from pydantic import BaseModel, Field, HttpUrl
from app.schemas.common import TimestampSchema


class CompanyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    website: HttpUrl | None = None
    industry: str | None = Field(default=None, max_length=100)
    phone: str | None = Field(default=None, max_length=30)
    address: str | None = None


class CompanyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    website: HttpUrl | None = None
    industry: str | None = None
    phone: str | None = None
    address: str | None = None


class CompanyResponse(TimestampSchema):
    id: uuid.UUID
    owner_id: uuid.UUID
    name: str
    website: HttpUrl | None
    industry: str | None
    phone: str | None
    address: str | None
