import uuid

from sqlmodel import Session, select

from app.auth.models import User
from app.auth.schemas import UserCreate
from app.core.security import get_password_hash


def get_by_id(session: Session, user_id: uuid.UUID) -> User | None:
    return session.get(User, user_id)


def get_by_email(session: Session, email: str) -> User | None:
    return session.exec(select(User).where(User.email == email)).first()


def create(session: Session, user_in: UserCreate) -> User:
    user = User.model_validate(
        user_in,
        update={"hashed_password": get_password_hash(user_in.password)},
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
