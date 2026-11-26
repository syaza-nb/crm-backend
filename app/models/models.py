
import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Numeric,
    String,
    Table,
    Text,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# --------------------------------------------------
# BASE
# --------------------------------------------------

class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


# --------------------------------------------------
# ASSOCIATION TABLES
# --------------------------------------------------

team_members = Table(
    "team_members",
    Base.metadata,
    Column("team_id", Uuid(as_uuid=True), ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)

contact_companies = Table(
    "contact_companies",
    Base.metadata,
    Column("contact_id", Uuid(as_uuid=True), ForeignKey("contacts.id", ondelete="CASCADE"), primary_key=True),
    Column("company_id", Uuid(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), primary_key=True),
)

deal_contacts = Table(
    "deal_contacts",
    Base.metadata,
    Column("deal_id", Uuid(as_uuid=True), ForeignKey("deals.id", ondelete="CASCADE"), primary_key=True),
    Column("contact_id", Uuid(as_uuid=True), ForeignKey("contacts.id", ondelete="CASCADE"), primary_key=True),
)

activity_contacts = Table(
    "activity_contacts",
    Base.metadata,
    Column("activity_id", Uuid(as_uuid=True), ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True),
    Column("contact_id", Uuid(as_uuid=True), ForeignKey("contacts.id", ondelete="CASCADE"), primary_key=True),
)

activity_companies = Table(
    "activity_companies",
    Base.metadata,
    Column("activity_id", Uuid(as_uuid=True), ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True),
    Column("company_id", Uuid(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), primary_key=True),
)

activity_deals = Table(
    "activity_deals",
    Base.metadata,
    Column("activity_id", Uuid(as_uuid=True), ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True),
    Column("deal_id", Uuid(as_uuid=True), ForeignKey("deals.id", ondelete="CASCADE"), primary_key=True),
)


# --------------------------------------------------
# ROLES AND USERS
# --------------------------------------------------

class Role(Base, TimestampMixin):
    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    users: Mapped[list["User"]] = relationship(back_populates="role")


class User(Base, TimestampMixin):
    __tablename__ = "users"
    __table_args__ = (
        Index("ix_users_email", "email"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("roles.id"), nullable=False
    )
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    role: Mapped["Role"] = relationship(back_populates="users")

    memberships: Mapped[list["Team"]] = relationship(
        secondary=team_members,
        back_populates="members",
    )
    managed_teams: Mapped[list["Team"]] = relationship(
        back_populates="manager",
        foreign_keys="Team.manager_id",
    )

    companies: Mapped[list["Company"]] = relationship(back_populates="owner")
    contacts: Mapped[list["Contact"]] = relationship(back_populates="owner")
    deals: Mapped[list["Deal"]] = relationship(back_populates="owner")
    assigned_tasks: Mapped[list["Task"]] = relationship(
        back_populates="assignee",
        foreign_keys="Task.assigned_to",
    )
    created_tasks: Mapped[list["Task"]] = relationship(
        back_populates="creator",
        foreign_keys="Task.created_by",
    )
    activities: Mapped[list["Activity"]] = relationship(back_populates="creator")
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        back_populates="user"
    )


# --------------------------------------------------
# TEAMS
# --------------------------------------------------

class Team(Base, TimestampMixin):
    __tablename__ = "teams"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    manager_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    manager: Mapped["User | None"] = relationship(
        back_populates="managed_teams",
        foreign_keys=[manager_id],
    )
    members: Mapped[list["User"]] = relationship(
        secondary=team_members,
        back_populates="memberships",
    )


# --------------------------------------------------
# COMPANIES AND CONTACTS
# --------------------------------------------------

class Company(Base, TimestampMixin):
    __tablename__ = "companies"
    __table_args__ = (
        Index("ix_companies_owner_id", "owner_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    website: Mapped[str | None] = mapped_column(String(255))
    industry: Mapped[str | None] = mapped_column(String(100))
    phone: Mapped[str | None] = mapped_column(String(30))
    address: Mapped[str | None] = mapped_column(Text)

    owner: Mapped["User"] = relationship(back_populates="companies")
    contacts: Mapped[list["Contact"]] = relationship(
        secondary=contact_companies,
        back_populates="companies",
    )
    deals: Mapped[list["Deal"]] = relationship(back_populates="company")
    activities: Mapped[list["Activity"]] = relationship(
        secondary=activity_companies,
        back_populates="companies",
    )


class Contact(Base, TimestampMixin):
    __tablename__ = "contacts"
    __table_args__ = (
        Index("ix_contacts_owner_id", "owner_id"),
        Index("ix_contacts_email", "email"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(30))
    job_title: Mapped[str | None] = mapped_column(String(150))

    owner: Mapped["User"] = relationship(back_populates="contacts")
    companies: Mapped[list["Company"]] = relationship(
        secondary=contact_companies,
        back_populates="contacts",
    )
    deals: Mapped[list["Deal"]] = relationship(
        secondary=deal_contacts,
        back_populates="contacts",
    )
    activities: Mapped[list["Activity"]] = relationship(
        secondary=activity_contacts,
        back_populates="contacts",
    )


# --------------------------------------------------
# SALES PIPELINES AND DEALS
# --------------------------------------------------

class Pipeline(Base, TimestampMixin):
    __tablename__ = "pipelines"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    stages: Mapped[list["DealStage"]] = relationship(
        back_populates="pipeline",
        cascade="all, delete-orphan",
        order_by="DealStage.position",
    )


class DealStage(Base, TimestampMixin):
    __tablename__ = "deal_stages"
    __table_args__ = (
        UniqueConstraint("pipeline_id", "position", name="uq_stage_position"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    pipeline_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("pipelines.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    position: Mapped[int] = mapped_column(nullable=False)
    probability: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), default=0, nullable=False
    )

    pipeline: Mapped["Pipeline"] = relationship(back_populates="stages")
    deals: Mapped[list["Deal"]] = relationship(back_populates="stage")


class Deal(Base, TimestampMixin):
    __tablename__ = "deals"
    __table_args__ = (
        Index("ix_deals_owner_id", "owner_id"),
        Index("ix_deals_stage_id", "stage_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    company_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("companies.id", ondelete="SET NULL")
    )
    stage_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("deal_stages.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), default=0, nullable=False
    )
    expected_close_date: Mapped[date | None] = mapped_column(Date)

    owner: Mapped["User"] = relationship(back_populates="deals")
    company: Mapped["Company | None"] = relationship(back_populates="deals")
    stage: Mapped["DealStage"] = relationship(back_populates="deals")
    contacts: Mapped[list["Contact"]] = relationship(
        secondary=deal_contacts,
        back_populates="deals",
    )
    activities: Mapped[list["Activity"]] = relationship(
        secondary=activity_deals,
        back_populates="deals",
    )


# --------------------------------------------------
# TASKS
# --------------------------------------------------

class Task(Base, TimestampMixin):
    __tablename__ = "tasks"
    __table_args__ = (
        Index("ix_tasks_assigned_to", "assigned_to"),
        Index("ix_tasks_due_date", "due_date"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    assigned_to: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    created_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        Enum("pending", "in_progress", "completed", "cancelled", name="task_status"),
        default="pending",
        nullable=False,
    )
    priority: Mapped[str] = mapped_column(
        Enum("low", "medium", "high", "urgent", name="task_priority"),
        default="medium",
        nullable=False,
    )
    due_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )

    assignee: Mapped["User"] = relationship(
        back_populates="assigned_tasks",
        foreign_keys=[assigned_to],
    )
    creator: Mapped["User"] = relationship(
        back_populates="created_tasks",
        foreign_keys=[created_by],
    )


# --------------------------------------------------
# ACTIVITIES
# --------------------------------------------------

class Activity(Base, TimestampMixin):
    __tablename__ = "activities"
    __table_args__ = (
        Index("ix_activities_created_by", "created_by"),
        Index("ix_activities_activity_date", "activity_date"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    activity_type: Mapped[str] = mapped_column(
        Enum(
            "call",
            "email",
            "meeting",
            "note",
            "other",
            name="activity_type",
        ),
        nullable=False,
    )
    subject: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    activity_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    creator: Mapped["User"] = relationship(back_populates="activities")
    contacts: Mapped[list["Contact"]] = relationship(
        secondary=activity_contacts,
        back_populates="activities",
    )
    companies: Mapped[list["Company"]] = relationship(
        secondary=activity_companies,
        back_populates="activities",
    )
    deals: Mapped[list["Deal"]] = relationship(
        secondary=activity_deals,
        back_populates="activities",
    )


# --------------------------------------------------
# REFRESH TOKENS
# --------------------------------------------------

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    __table_args__ = (
        Index("ix_refresh_tokens_user_id", "user_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    token_hash: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")
