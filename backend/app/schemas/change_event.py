from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.change_event import ChangeEventType


class ChangeEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tracker_id: UUID
    snapshot_id: UUID
    previous_snapshot_id: UUID | None
    field_name: str
    old_value: Any
    new_value: Any
    change_type: ChangeEventType
    detected_at: datetime
    notified: bool
