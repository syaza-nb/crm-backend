
import uuid
from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field
from app.schemas.common import TimestampSchema


class PipelineCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class PipelineResponse(TimestampSchema):
    id: uuid.UUID
    name: str


class DealStageCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    position: int = Field(ge=0)
    probability: Decimal = Field(default=0, ge=0, le=100)


class DealStageResponse(TimestampSchema):
    id: uuid.UUID
    pipeline_id: uuid.UUID
    name: str
    position: int
    probability: Decimal


class DealCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    company_id: uuid.UUID | None = None
    stage_id: uuid.UUID
    amount: Decimal = Field(default=0, ge=0)
    expected_close_date: date | None = None
    contact_ids: list[uuid.UUID] = Field(default_factory=list)


class DealUpdate(BaseModel):
    title: str | None = None
    company_id: uuid.UUID | None = None
    stage_id: uuid.UUID | None = None
    amount: Decimal | None = Field(default=None, ge=0)
    expected_close_date: date | None = None
    contact_ids: list[uuid.UUID] | None = None


class DealResponse(TimestampSchema):
    id: uuid.UUID
    owner_id: uuid.UUID
    company_id: uuid.UUID | None
    stage_id: uuid.UUID
    title: str
    amount: Decimal
    expected_close_date: date | None
