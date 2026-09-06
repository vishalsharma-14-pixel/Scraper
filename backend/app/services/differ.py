from dataclasses import dataclass
from typing import Any

from app.models.change_event import ChangeEventType

_PRICE_EPSILON = 0.01


@dataclass
class FieldChange:
    field_name: str
    old_value: Any
    new_value: Any
    change_type: ChangeEventType


def _is_meaningful_change(old_value: Any, new_value: Any, field_type: str) -> bool:
    if new_value is None:
        return False
    if field_type in ("price", "number"):
        if old_value is None:
            return True
        try:
            return abs(float(new_value) - float(old_value)) > _PRICE_EPSILON
        except (TypeError, ValueError):
            return new_value != old_value
    return new_value != old_value


def diff_snapshots(
    previous: dict[str, Any] | None,
    current: dict[str, Any],
    field_types: dict[str, str],
) -> list[FieldChange]:
    changes: list[FieldChange] = []

    if previous is None:
        for field_name, new_value in current.items():
            changes.append(
                FieldChange(
                    field_name=field_name,
                    old_value=None,
                    new_value=new_value,
                    change_type=ChangeEventType.FIRST_SEEN,
                )
            )
        return changes

    for field_name, new_value in current.items():
        old_value = previous.get(field_name)
        field_type = field_types.get(field_name, "text")
        if _is_meaningful_change(old_value, new_value, field_type):
            changes.append(
                FieldChange(
                    field_name=field_name,
                    old_value=old_value,
                    new_value=new_value,
                    change_type=ChangeEventType.VALUE_CHANGED,
                )
            )

    return changes
