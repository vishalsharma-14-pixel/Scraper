from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, HttpUrl


class FieldConfig(BaseModel):
    selector: str | None = None
    xpath: str | None = None
    type: str = "text"
    attribute: str | None = None


class TrackerCreate(BaseModel):
    name: str
    url: HttpUrl
    extraction_config: dict[str, FieldConfig]
    requires_js: bool | None = None
    poll_interval_seconds: int = 3600
    is_active: bool = True
    notes: str | None = None


class TrackerUpdate(TrackerCreate):
    pass


class TrackerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    url: str
    extraction_config: dict[str, FieldConfig]
    requires_js: bool | None
    poll_interval_seconds: int
    is_active: bool
    next_run_at: datetime | None
    last_run_at: datetime | None
    notes: str | None
    created_at: datetime
    updated_at: datetime
