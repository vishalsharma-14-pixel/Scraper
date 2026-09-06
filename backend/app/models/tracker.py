import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Tracker(Base):
    __tablename__ = "trackers"

    id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    extraction_config: Mapped[dict] = mapped_column(postgresql.JSONB, nullable=False)
    requires_js: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=None)
    poll_interval_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=3600)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    next_run_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    last_run_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    snapshots: Mapped[list["Snapshot"]] = relationship(
        back_populates="tracker", cascade="all, delete-orphan"
    )
    change_events: Mapped[list["ChangeEvent"]] = relationship(
        back_populates="tracker", cascade="all, delete-orphan"
    )
    job_runs: Mapped[list["JobRun"]] = relationship(
        back_populates="tracker", cascade="all, delete-orphan"
    )
