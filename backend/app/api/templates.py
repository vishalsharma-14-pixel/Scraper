from fastapi import APIRouter

from app.schemas.template import TemplateResponse
from app.services.templates import get_templates

router = APIRouter(prefix="/api/templates", tags=["templates"])


@router.get("", response_model=list[TemplateResponse])
def list_templates():
    return get_templates()
