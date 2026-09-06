import enum

from sqlalchemy import create_engine
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def pg_enum(enum_cls: type[enum.Enum], name: str) -> SAEnum:
    """Enum column bound to a str-Enum's lowercase .value (not .name), matching
    the Postgres enum types created in the Alembic migration."""
    return SAEnum(enum_cls, name=name, values_callable=lambda obj: [e.value for e in obj])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
