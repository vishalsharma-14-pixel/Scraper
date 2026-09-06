from celery import Celery

from app.config import settings

celery_app = Celery("scrapetrack", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    task_track_started=True,
    broker_connection_retry_on_startup=True,
)
celery_app.conf.beat_schedule = {
    "dispatch-due-trackers": {
        "task": "dispatch_due_trackers",
        "schedule": settings.dispatch_interval_seconds,
    },
}

# Explicit imports (not autodiscover) so task modules register with celery_app at import time.
from app.tasks import dispatch_trackers, scrape_tracker  # noqa: E402,F401
