from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.job_run import JobStatus, JobTrigger
from app.models.snapshot import FetchMethod


class JobRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tracker_id: UUID
    celery_task_id: str | None
    status: JobStatus
    trigger: JobTrigger
    fetch_method_used: FetchMethod | None
    snapshot_id: UUID | None
    started_at: datetime | None
    finished_at: datetime | None
    error_message: str | None
    created_at: datetime
