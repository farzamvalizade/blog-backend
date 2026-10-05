from sqlmodel import Session

from app.auth import repository
from app.auth.models import User
from app.core.security import verify_password


def authenticate_superuser(
    session: Session,
    email: str,
    password: str,
) -> User | None:
    user = repository.get_by_email(session, email)
    if user is None or not user.is_active or not user.is_superuser:
        return None

    verified, updated_hash = verify_password(password, user.hashed_password)
    if not verified:
        return None

    if updated_hash:
        user.hashed_password = updated_hash
        session.add(user)
        session.commit()
        session.refresh(user)

    return user
