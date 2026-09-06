import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Index
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, pg_enum


class FetchMethod(str, enum.Enum):
    HTTP = "http"
    HEADLESS = "headless"


class Snapshot(Base):
    __tablename__ = "snapshots"
    __table_args__ = (Index("ix_snapshots_tracker_scraped_at", "tracker_id", "scraped_at"),)

    id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tracker_id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), ForeignKey("trackers.id"), nullable=False, index=True
    )
    raw_values: Mapped[dict] = mapped_column(postgresql.JSONB, nullable=False)
    normalized_values: Mapped[dict] = mapped_column(postgresql.JSONB, nullable=False)
    fetch_method: Mapped[FetchMethod] = mapped_column(pg_enum(FetchMethod, "fetch_method"), nullable=False)
    scraped_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    tracker: Mapped["Tracker"] = relationship(back_populates="snapshots")
