"""Import every table model so Alembic can discover complete metadata."""

from sqlmodel import SQLModel

from app.auth.models import User
from app.auth.schemas import Token, TokenPayload, UserCreate, UserPublic
from app.categories.models import Category
from app.posts.models import Post
from app.site_settings.models import SiteSettings
from app.tags.models import PostTagLink, Tag


class Message(SQLModel):
    message: str


__all__ = [
    "Category",
    "Message",
    "Post",
    "PostTagLink",
    "SQLModel",
    "SiteSettings",
    "Tag",
    "Token",
    "TokenPayload",
    "User",
    "UserCreate",
    "UserPublic",
]
