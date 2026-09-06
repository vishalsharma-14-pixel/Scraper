"""initial schema

Revision ID: a1b2c3d4e5f6
Revises:
Create Date: 2026-09-04 00:00:00

"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()

    fetch_method = postgresql.ENUM("http", "headless", name="fetch_method")
    change_event_type = postgresql.ENUM("first_seen", "value_changed", name="change_event_type")
    job_status = postgresql.ENUM("pending", "running", "success", "failed", name="job_status")
    job_trigger = postgresql.ENUM("scheduled", "manual", name="job_trigger")

    fetch_method.create(bind, checkfirst=True)
    change_event_type.create(bind, checkfirst=True)
    job_status.create(bind, checkfirst=True)
    job_trigger.create(bind, checkfirst=True)

    op.create_table(
        "trackers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("url", sa.String(2048), nullable=False),
        sa.Column("extraction_config", postgresql.JSONB, nullable=False),
        sa.Column("requires_js", sa.Boolean, nullable=True),
        sa.Column("poll_interval_seconds", sa.Integer, nullable=False, server_default="3600"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("next_run_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_run_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_trackers_next_run_at", "trackers", ["next_run_at"])

    op.create_table(
        "snapshots",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column(
            "tracker_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("trackers.id"),
            nullable=False,
        ),
        sa.Column("raw_values", postgresql.JSONB, nullable=False),
        sa.Column("normalized_values", postgresql.JSONB, nullable=False),
        sa.Column(
            "fetch_method",
            postgresql.ENUM("http", "headless", name="fetch_method", create_type=False),
            nullable=False,
        ),
        sa.Column("scraped_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_snapshots_tracker_id", "snapshots", ["tracker_id"])
    op.create_index("ix_snapshots_tracker_scraped_at", "snapshots", ["tracker_id", "scraped_at"])

    op.create_table(
        "change_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column(
            "tracker_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("trackers.id"),
            nullable=False,
        ),
        sa.Column(
            "snapshot_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("snapshots.id"),
            nullable=False,
        ),
        sa.Column(
            "previous_snapshot_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("snapshots.id"),
            nullable=True,
        ),
        sa.Column("field_name", sa.String(255), nullable=False),
        sa.Column("old_value", postgresql.JSONB, nullable=True),
        sa.Column("new_value", postgresql.JSONB, nullable=True),
        sa.Column(
            "change_type",
            postgresql.ENUM(
                "first_seen", "value_changed", name="change_event_type", create_type=False
            ),
            nullable=False,
        ),
        sa.Column("detected_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("notified", sa.Boolean, nullable=False, server_default=sa.false()),
    )
    op.create_index("ix_change_events_tracker_id", "change_events", ["tracker_id"])
    op.create_index(
        "ix_change_events_tracker_detected_at", "change_events", ["tracker_id", "detected_at"]
    )

    op.create_table(
        "job_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column(
            "tracker_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("trackers.id"),
            nullable=False,
        ),
        sa.Column("celery_task_id", sa.String(255), nullable=True),
        sa.Column(
            "status",
            postgresql.ENUM(
                "pending", "running", "success", "failed", name="job_status", create_type=False
            ),
            nullable=False,
            server_default="pending",
        ),
        sa.Column(
            "trigger",
            postgresql.ENUM("scheduled", "manual", name="job_trigger", create_type=False),
            nullable=False,
        ),
        sa.Column(
            "fetch_method_used",
            postgresql.ENUM("http", "headless", name="fetch_method", create_type=False),
            nullable=True,
        ),
        sa.Column(
            "snapshot_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("snapshots.id"),
            nullable=True,
        ),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_job_runs_tracker_id", "job_runs", ["tracker_id"])
    op.create_index("ix_job_runs_tracker_created_at", "job_runs", ["tracker_id", "created_at"])


def downgrade() -> None:
    op.drop_table("job_runs")
    op.drop_table("change_events")
    op.drop_table("snapshots")
    op.drop_table("trackers")

    bind = op.get_bind()
    postgresql.ENUM(name="job_trigger").drop(bind, checkfirst=True)
    postgresql.ENUM(name="job_status").drop(bind, checkfirst=True)
    postgresql.ENUM(name="change_event_type").drop(bind, checkfirst=True)
    postgresql.ENUM(name="fetch_method").drop(bind, checkfirst=True)
