from typing import Protocol

from sqlalchemy.orm import Session

from app.models.change_event import ChangeEvent, ChangeEventType


class NotificationChannel(Protocol):
    def send(self, db: Session, event: ChangeEvent) -> None: ...


class InAppNotificationChannel:
    def send(self, db: Session, event: ChangeEvent) -> None:
        event.notified = True


_CHANNELS: list[NotificationChannel] = [InAppNotificationChannel()]


def notify(db: Session, event: ChangeEvent) -> None:
    if event.change_type == ChangeEventType.FIRST_SEEN:
        return
    for channel in _CHANNELS:
        channel.send(db, event)
