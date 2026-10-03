from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import User, UserCreate, UserUpdate


def get_user(
    *,
    session: Session,
    user_id: Any,
) -> User | None:
    """
    Get a user by ID.
    """
    return session.get(User, user_id)


def get_user_by_email(
    *,
    session: Session,
    email: str,
) -> User | None:
    """
    Get a user by email address.
    """
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def get_users(
    *,
    session: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[User]:
    """
    Get a paginated list of users.
    """
    statement = select(User).offset(skip).limit(limit)

    return list(session.exec(statement).all())


def create_user(
    *,
    session: Session,
    user_create: UserCreate,
) -> User:
    """
    Create a new user with a hashed password.
    """
    db_user = User.model_validate(
        user_create,
        update={
            "hashed_password": get_password_hash(user_create.password),
        },
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def update_user(
    *,
    session: Session,
    db_user: User,
    user_in: UserUpdate,
) -> User:
    """
    Update an existing user.

    If a new password is provided, it is hashed before being
    stored in the database.
    """
    user_data = user_in.model_dump(
        exclude_unset=True,
    )

    extra_data: dict[str, Any] = {}

    if "password" in user_data:
        password = user_data.pop("password")
        extra_data["hashed_password"] = get_password_hash(password)

    db_user.sqlmodel_update(
        user_data,
        update=extra_data,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def authenticate(
    *,
    session: Session,
    email: str,
    password: str,
) -> User | None:
    """
    Authenticate a user using their email and password.
    """
    user = get_user_by_email(
        session=session,
        email=email,
    )

    if not user:
        return None

    verified, updated_password_hash = verify_password(
        password,
        user.hashed_password,
    )

    if not verified:
        return None

    if updated_password_hash:
        user.hashed_password = updated_password_hash
        session.add(user)
        session.commit()
        session.refresh(user)

    return user
