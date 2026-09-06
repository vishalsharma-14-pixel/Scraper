from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.snapshot import FetchMethod


class SnapshotResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tracker_id: UUID
    raw_values: dict
    normalized_values: dict
    fetch_method: FetchMethod
    scraped_at: datetime
