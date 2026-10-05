import uuid
from datetime import datetime

from pydantic import field_validator
from sqlmodel import Field, SQLModel

from app.categories.schemas import CategoryPublic
from app.core.validation import validate_slug
from app.posts.models import PostStatus
from app.tags.schemas import TagPublic


class PostFields(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    slug: str = Field(min_length=1, max_length=255)
    excerpt: str | None = Field(default=None, max_length=500)
    content: str = Field(min_length=1)
    featured_image_url: str | None = Field(default=None, max_length=2048)
    status: PostStatus = PostStatus.DRAFT
    category_id: uuid.UUID | None = None

    _validate_slug = field_validator("slug")(validate_slug)


class PostCreate(PostFields):
    tag_ids: list[uuid.UUID] = Field(default_factory=list)


class PostUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    slug: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    excerpt: str | None = Field(default=None, max_length=500)
    content: str | None = Field(default=None, min_length=1)
    featured_image_url: str | None = Field(default=None, max_length=2048)
    status: PostStatus | None = None
    category_id: uuid.UUID | None = None
    tag_ids: list[uuid.UUID] | None = None

    _validate_slug = field_validator("slug")(validate_slug)


class PostPublic(SQLModel):
    id: uuid.UUID
    title: str
    slug: str
    excerpt: str | None
    content: str
    featured_image_url: str | None
    status: PostStatus
    author_id: uuid.UUID
    category_id: uuid.UUID | None
    category: CategoryPublic | None
    tags: list[TagPublic]
    created_at: datetime
    updated_at: datetime
    published_at: datetime | None


class PostsPublic(SQLModel):
    data: list[PostPublic]
    count: int
