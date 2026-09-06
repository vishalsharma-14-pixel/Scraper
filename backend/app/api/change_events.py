from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.change_event import ChangeEvent
from app.schemas.change_event import ChangeEventResponse

router = APIRouter(prefix="/api/change-events", tags=["change-events"])


@router.get("", response_model=list[ChangeEventResponse])
def list_change_events(
    tracker_id: UUID | None = None,
    limit: int = Query(default=50, le=500),
    db: Session = Depends(get_db),
):
    query = db.query(ChangeEvent)
    if tracker_id is not None:
        query = query.filter(ChangeEvent.tracker_id == tracker_id)
    return query.order_by(ChangeEvent.detected_at.desc()).limit(limit).all()
