from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.job_run import JobRun, JobStatus
from app.schemas.job_run import JobRunResponse

router = APIRouter(prefix="/api/job-runs", tags=["job-runs"])


@router.get("", response_model=list[JobRunResponse])
def list_job_runs(
    tracker_id: UUID | None = None,
    status_filter: JobStatus | None = Query(default=None, alias="status"),
    limit: int = Query(default=50, le=500),
    db: Session = Depends(get_db),
):
    query = db.query(JobRun)
    if tracker_id is not None:
        query = query.filter(JobRun.tracker_id == tracker_id)
    if status_filter is not None:
        query = query.filter(JobRun.status == status_filter)
    return query.order_by(JobRun.created_at.desc()).limit(limit).all()


@router.get("/{job_run_id}", response_model=JobRunResponse)
def get_job_run(job_run_id: UUID, db: Session = Depends(get_db)):
    job_run = db.get(JobRun, job_run_id)
    if job_run is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job run not found")
    return job_run
