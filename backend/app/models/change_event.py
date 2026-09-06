import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, pg_enum


class ChangeEventType(str, enum.Enum):
    FIRST_SEEN = "first_seen"
    VALUE_CHANGED = "value_changed"


class ChangeEvent(Base):
    __tablename__ = "change_events"
    __table_args__ = (Index("ix_change_events_tracker_detected_at", "tracker_id", "detected_at"),)

    id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tracker_id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), ForeignKey("trackers.id"), nullable=False, index=True
    )
    snapshot_id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), ForeignKey("snapshots.id"), nullable=False
    )
    previous_snapshot_id: Mapped[uuid.UUID | None] = mapped_column(
        postgresql.UUID(as_uuid=True), ForeignKey("snapshots.id"), nullable=True
    )
    field_name: Mapped[str] = mapped_column(String(255), nullable=False)
    old_value: Mapped[dict | None] = mapped_column(postgresql.JSONB, nullable=True)
    new_value: Mapped[dict | None] = mapped_column(postgresql.JSONB, nullable=True)
    change_type: Mapped[ChangeEventType] = mapped_column(
        pg_enum(ChangeEventType, "change_event_type"), nullable=False
    )
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    notified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    tracker: Mapped["Tracker"] = relationship(back_populates="change_events")
