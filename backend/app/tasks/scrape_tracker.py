import logging
from datetime import datetime, timezone

from app.database import SessionLocal
from app.models.change_event import ChangeEvent
from app.models.job_run import JobRun, JobStatus
from app.models.snapshot import Snapshot
from app.models.tracker import Tracker
from app.services import differ, normalizer, notifier, scraper
from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="scrape_tracker_task")
def scrape_tracker_task(tracker_id: str, job_run_id: str) -> None:
    db = SessionLocal()
    try:
        tracker = db.get(Tracker, tracker_id)
        job_run = db.get(JobRun, job_run_id)
        if tracker is None or job_run is None:
            return

        job_run.status = JobStatus.RUNNING
        job_run.started_at = datetime.now(timezone.utc)
        db.commit()

        try:
            field_types = {
                field_name: field_config.get("type", "text")
                for field_name, field_config in tracker.extraction_config.items()
            }

            outcome = scraper.fetch_and_extract(tracker)
            normalized_values = {
                field_name: normalizer.normalize_value(raw, field_types.get(field_name, "text"))
                for field_name, raw in outcome.raw_values.items()
            }

            previous_snapshot = (
                db.query(Snapshot)
                .filter(Snapshot.tracker_id == tracker.id)
                .order_by(Snapshot.scraped_at.desc())
                .first()
            )
            previous_values = previous_snapshot.normalized_values if previous_snapshot else None

            snapshot = Snapshot(
                tracker_id=tracker.id,
                raw_values=outcome.raw_values,
                normalized_values=normalized_values,
                fetch_method=outcome.fetch_method,
            )
            db.add(snapshot)
            db.flush()

            field_changes = differ.diff_snapshots(previous_values, normalized_values, field_types)
            for change in field_changes:
                event = ChangeEvent(
                    tracker_id=tracker.id,
                    snapshot_id=snapshot.id,
                    previous_snapshot_id=previous_snapshot.id if previous_snapshot else None,
                    field_name=change.field_name,
                    old_value=change.old_value,
                    new_value=change.new_value,
                    change_type=change.change_type,
                )
                db.add(event)
                notifier.notify(db, event)

            job_run.status = JobStatus.SUCCESS
            job_run.fetch_method_used = outcome.fetch_method
            job_run.snapshot_id = snapshot.id
            job_run.finished_at = datetime.now(timezone.utc)
            tracker.last_run_at = job_run.finished_at
            db.commit()
        except Exception as exc:
            logger.exception("Scrape failed for tracker %s", tracker_id)
            db.rollback()
            job_run.status = JobStatus.FAILED
            job_run.error_message = str(exc)
            job_run.finished_at = datetime.now(timezone.utc)
            db.commit()
    finally:
        db.close()
