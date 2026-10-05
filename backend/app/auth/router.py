from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import CurrentSuperuser, SessionDep
from app.auth.schemas import Token, UserPublic
from app.auth.service import authenticate_superuser
from app.core import security
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=Token)
def login(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_superuser(
        session,
        email=form_data.username,
        password=form_data.password,
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect administrator credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(
        access_token=security.create_access_token(
            user.id,
            expires_delta=timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            ),
        )
    )


@router.get("/me", response_model=UserPublic)
def read_current_superuser(current_user: CurrentSuperuser) -> UserPublic:
    return UserPublic.model_validate(current_user)
