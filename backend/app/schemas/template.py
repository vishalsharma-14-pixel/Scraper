from pydantic import BaseModel

from app.schemas.tracker import FieldConfig


class TemplateResponse(BaseModel):
    key: str
    name: str
    description: str
    extraction_config: dict[str, FieldConfig]
