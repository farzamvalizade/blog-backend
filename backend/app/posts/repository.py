import uuid
from typing import Any, cast

from sqlalchemy.orm import QueryableAttribute, selectinload
from sqlmodel import Session, col, func, select

from app.posts.models import Post, PostStatus


def _with_relations():
    category = cast(QueryableAttribute[Any], Post.category)
    tags = cast(QueryableAttribute[Any], Post.tags)
    return (selectinload(category), selectinload(tags))


def list_published(
    session: Session,
    skip: int,
    limit: int,
) -> tuple[list[Post], int]:
    predicate = Post.status == PostStatus.PUBLISHED
    count = session.exec(
        select(func.count()).select_from(Post).where(predicate)
    ).one()
    statement = (
        select(Post)
        .where(predicate)
        .options(*_with_relations())
        .order_by(col(Post.published_at).desc(), col(Post.created_at).desc())
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all()), count


def list_all(session: Session, skip: int, limit: int) -> tuple[list[Post], int]:
    count = session.exec(select(func.count()).select_from(Post)).one()
    statement = (
        select(Post)
        .options(*_with_relations())
        .order_by(col(Post.created_at).desc())
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all()), count


def get_by_id(session: Session, post_id: uuid.UUID) -> Post | None:
    return session.exec(
        select(Post).where(Post.id == post_id).options(*_with_relations())
    ).first()


def get_by_slug(
    session: Session,
    slug: str,
    *,
    published_only: bool = False,
) -> Post | None:
    statement = select(Post).where(Post.slug == slug).options(*_with_relations())
    if published_only:
        statement = statement.where(Post.status == PostStatus.PUBLISHED)
    return session.exec(statement).first()


def save(session: Session, post: Post) -> Post:
    session.add(post)
    session.commit()
    session.refresh(post)
    return get_by_id(session, post.id) or post


def delete(session: Session, post: Post) -> None:
    session.delete(post)
    session.commit()
