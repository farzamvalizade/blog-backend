import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import Column, DateTime, Text
from sqlmodel import Field, Relationship, SQLModel

from app.auth.models import User
from app.categories.models import Category
from app.core.time import utc_now
from app.tags.models import PostTagLink, Tag


class PostStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"


class Post(SQLModel, table=True):
    __tablename__ = "posts"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(index=True, max_length=255)
    slug: str = Field(unique=True, index=True, max_length=255)
    excerpt: str | None = Field(default=None, max_length=500)
    content: str = Field(sa_type=Text)
    featured_image_url: str | None = Field(default=None, max_length=2048)
    status: PostStatus = Field(default=PostStatus.DRAFT, index=True)
    author_id: uuid.UUID = Field(
        foreign_key="users.id",
        index=True,
        nullable=False,
        ondelete="RESTRICT",
    )
    category_id: uuid.UUID | None = Field(
        default=None,
        foreign_key="categories.id",
        index=True,
        ondelete="SET NULL",
    )
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    published_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
    author: User = Relationship()
    category: Category = Relationship()
    tags: list[Tag] = Relationship(
        link_model=PostTagLink,
    )
