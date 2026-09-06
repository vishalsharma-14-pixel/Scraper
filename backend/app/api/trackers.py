from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.change_event import ChangeEvent
from app.models.job_run import JobRun, JobStatus, JobTrigger
from app.models.snapshot import Snapshot
from app.models.tracker import Tracker
from app.schemas.change_event import ChangeEventResponse
from app.schemas.job_run import JobRunResponse
from app.schemas.snapshot import SnapshotResponse
from app.schemas.tracker import TrackerCreate, TrackerResponse, TrackerUpdate
from app.tasks.scrape_tracker import scrape_tracker_task

router = APIRouter(prefix="/api/trackers", tags=["trackers"])


def _get_tracker_or_404(db: Session, tracker_id: UUID) -> Tracker:
    tracker = db.get(Tracker, tracker_id)
    if tracker is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tracker not found")
    return tracker


def _validate_poll_interval(poll_interval_seconds: int) -> None:
    if poll_interval_seconds < settings.min_poll_interval_seconds:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"poll_interval_seconds must be >= {settings.min_poll_interval_seconds}",
        )


def _extraction_config_dict(payload: TrackerCreate) -> dict:
    return {name: field.model_dump() for name, field in payload.extraction_config.items()}


@router.post("", response_model=TrackerResponse, status_code=status.HTTP_201_CREATED)
def create_tracker(payload: TrackerCreate, db: Session = Depends(get_db)):
    _validate_poll_interval(payload.poll_interval_seconds)

    tracker = Tracker(
        name=payload.name,
        url=str(payload.url),
        extraction_config=_extraction_config_dict(payload),
        requires_js=payload.requires_js,
        poll_interval_seconds=payload.poll_interval_seconds,
        is_active=payload.is_active,
        notes=payload.notes,
        next_run_at=datetime.now(timezone.utc) if payload.is_active else None,
    )
    db.add(tracker)
    db.commit()
    db.refresh(tracker)
    return tracker


@router.get("", response_model=list[TrackerResponse])
def list_trackers(db: Session = Depends(get_db)):
    return db.query(Tracker).order_by(Tracker.created_at.desc()).all()


@router.get("/{tracker_id}", response_model=TrackerResponse)
def get_tracker(tracker_id: UUID, db: Session = Depends(get_db)):
    return _get_tracker_or_404(db, tracker_id)


@router.put("/{tracker_id}", response_model=TrackerResponse)
def update_tracker(tracker_id: UUID, payload: TrackerUpdate, db: Session = Depends(get_db)):
    tracker = _get_tracker_or_404(db, tracker_id)
    _validate_poll_interval(payload.poll_interval_seconds)

    reactivating = payload.is_active and not tracker.is_active

    tracker.name = payload.name
    tracker.url = str(payload.url)
    tracker.extraction_config = _extraction_config_dict(payload)
    tracker.requires_js = payload.requires_js
    tracker.poll_interval_seconds = payload.poll_interval_seconds
    tracker.is_active = payload.is_active
    tracker.notes = payload.notes

    if reactivating or (payload.is_active and tracker.next_run_at is None):
        tracker.next_run_at = datetime.now(timezone.utc)
    if not payload.is_active:
        tracker.next_run_at = None

    db.commit()
    db.refresh(tracker)
    return tracker


@router.delete("/{tracker_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tracker(tracker_id: UUID, db: Session = Depends(get_db)):
    tracker = _get_tracker_or_404(db, tracker_id)
    db.delete(tracker)
    db.commit()


@router.post("/{tracker_id}/run", response_model=JobRunResponse, status_code=status.HTTP_201_CREATED)
def run_tracker_now(tracker_id: UUID, db: Session = Depends(get_db)):
    tracker = _get_tracker_or_404(db, tracker_id)

    job_run = JobRun(tracker_id=tracker.id, status=JobStatus.PENDING, trigger=JobTrigger.MANUAL)
    db.add(job_run)
    db.commit()
    db.refresh(job_run)

    scrape_tracker_task.delay(str(tracker.id), str(job_run.id))
    return job_run


@router.get("/{tracker_id}/snapshots", response_model=list[SnapshotResponse])
def list_tracker_snapshots(
    tracker_id: UUID, limit: int = Query(default=50, le=500), db: Session = Depends(get_db)
):
    _get_tracker_or_404(db, tracker_id)
    return (
        db.query(Snapshot)
        .filter(Snapshot.tracker_id == tracker_id)
        .order_by(Snapshot.scraped_at.desc())
        .limit(limit)
        .all()
    )


@router.get("/{tracker_id}/snapshots/latest", response_model=SnapshotResponse)
def get_latest_snapshot(tracker_id: UUID, db: Session = Depends(get_db)):
    _get_tracker_or_404(db, tracker_id)
    snapshot = (
        db.query(Snapshot)
        .filter(Snapshot.tracker_id == tracker_id)
        .order_by(Snapshot.scraped_at.desc())
        .first()
    )
    if snapshot is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No snapshots yet")
    return snapshot


@router.get("/{tracker_id}/changes", response_model=list[ChangeEventResponse])
def list_tracker_changes(
    tracker_id: UUID, limit: int = Query(default=50, le=500), db: Session = Depends(get_db)
):
    _get_tracker_or_404(db, tracker_id)
    return (
        db.query(ChangeEvent)
        .filter(ChangeEvent.tracker_id == tracker_id)
        .order_by(ChangeEvent.detected_at.desc())
        .limit(limit)
        .all()
    )


@router.get("/{tracker_id}/jobs", response_model=list[JobRunResponse])
def list_tracker_jobs(
    tracker_id: UUID, limit: int = Query(default=50, le=500), db: Session = Depends(get_db)
):
    _get_tracker_or_404(db, tracker_id)
    return (
        db.query(JobRun)
        .filter(JobRun.tracker_id == tracker_id)
        .order_by(JobRun.created_at.desc())
        .limit(limit)
        .all()
    )
