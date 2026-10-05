from collections.abc import Generator

from sqlmodel import Session, create_engine

from app.auth import repository
from app.auth.schemas import UserCreate
from app.core.config import settings

connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.FASTAPI_ENV == "development",
    connect_args=connect_args,
)


def get_session() -> Generator[Session]:
    with Session(engine) as session:
        yield session


def init_db(session: Session) -> None:
    """Create the configured administrator if it does not exist."""
    if repository.get_by_email(session, settings.FIRST_SUPERUSER) is None:
        repository.create(
            session,
            UserCreate(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                full_name="Administrator",
                is_superuser=True,
            ),
        )
