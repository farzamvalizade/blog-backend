import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel

from app.core.time import utc_now


class PostTagLink(SQLModel, table=True):
    __tablename__ = "post_tag_links"

    post_id: uuid.UUID = Field(
        foreign_key="posts.id",
        primary_key=True,
        ondelete="CASCADE",
    )
    tag_id: uuid.UUID = Field(
        foreign_key="tags.id",
        primary_key=True,
        ondelete="CASCADE",
    )


class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True, max_length=50)
    slug: str = Field(unique=True, index=True, max_length=60)
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
