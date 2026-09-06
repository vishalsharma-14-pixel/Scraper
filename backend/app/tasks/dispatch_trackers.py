from datetime import datetime, timedelta, timezone

from sqlalchemy import and_, exists

from app.database import SessionLocal
from app.models.job_run import JobRun, JobStatus, JobTrigger
from app.models.tracker import Tracker
from app.tasks.celery_app import celery_app


@celery_app.task(name="dispatch_due_trackers")
def dispatch_due_trackers() -> None:
    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc)

        in_flight = exists().where(
            and_(
                JobRun.tracker_id == Tracker.id,
                JobRun.status.in_([JobStatus.PENDING, JobStatus.RUNNING]),
            )
        )

        due_trackers = (
            db.query(Tracker)
            .filter(Tracker.is_active.is_(True))
            .filter(Tracker.next_run_at.isnot(None))
            .filter(Tracker.next_run_at <= now)
            .filter(~in_flight)
            .all()
        )

        for tracker in due_trackers:
            job_run = JobRun(tracker_id=tracker.id, status=JobStatus.PENDING, trigger=JobTrigger.SCHEDULED)
            db.add(job_run)
            tracker.next_run_at = now + timedelta(seconds=tracker.poll_interval_seconds)
            db.commit()
            db.refresh(job_run)

            from app.tasks.scrape_tracker import scrape_tracker_task

            scrape_tracker_task.delay(str(tracker.id), str(job_run.id))
    finally:
        db.close()
