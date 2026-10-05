import uuid

from pydantic import field_validator
from sqlmodel import Field, SQLModel

from app.core.validation import validate_slug


class TagBase(SQLModel):
    name: str = Field(min_length=1, max_length=50)
    slug: str = Field(min_length=1, max_length=60)

    _validate_slug = field_validator("slug")(validate_slug)


class TagCreate(TagBase):
    pass


class TagUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    slug: str | None = Field(
        default=None,
        min_length=1,
        max_length=60,
    )

    _validate_slug = field_validator("slug")(validate_slug)


class TagPublic(TagBase):
    id: uuid.UUID


class TagsPublic(SQLModel):
    data: list[TagPublic]
    count: int
