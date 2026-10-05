import uuid

from sqlmodel import Session

from app.auth.models import User
from app.categories import repository as category_repository
from app.core.exceptions import ResourceConflictError, ResourceNotFoundError
from app.core.time import utc_now
from app.posts import repository
from app.posts.models import Post, PostStatus
from app.posts.schemas import PostCreate, PostUpdate
from app.tags import repository as tag_repository
from app.tags.models import Tag


def _get_tags(session: Session, tag_ids: list[uuid.UUID]) -> list[Tag]:
    unique_ids = set(tag_ids)
    tags = tag_repository.get_by_ids(session, list(unique_ids))
    if len(tags) != len(unique_ids):
        raise ResourceNotFoundError("One or more tags were not found")
    return tags


def _validate_category(session: Session, category_id: uuid.UUID | None) -> None:
    if category_id and category_repository.get_by_id(session, category_id) is None:
        raise ResourceNotFoundError("Category not found")


def create_post(session: Session, data: PostCreate, author: User) -> Post:
    if repository.get_by_slug(session, data.slug):
        raise ResourceConflictError("A post with this slug already exists")
    _validate_category(session, data.category_id)
    tags = _get_tags(session, data.tag_ids)
    values = data.model_dump(exclude={"tag_ids"})
    post = Post.model_validate(values, update={"author_id": author.id})
    post.tags = tags
    if post.status == PostStatus.PUBLISHED:
        post.published_at = utc_now()
    return repository.save(session, post)


def update_post(session: Session, post_id: uuid.UUID, data: PostUpdate) -> Post:
    post = repository.get_by_id(session, post_id)
    if post is None:
        raise ResourceNotFoundError("Post not found")

    changes = data.model_dump(exclude_unset=True)
    tag_ids = changes.pop("tag_ids", None)
    if data.slug:
        existing = repository.get_by_slug(session, data.slug)
        if existing and existing.id != post_id:
            raise ResourceConflictError("A post with this slug already exists")
    if "category_id" in changes:
        _validate_category(session, changes["category_id"])
    if tag_ids is not None:
        post.tags = _get_tags(session, tag_ids)

    was_published = post.status == PostStatus.PUBLISHED
    post.sqlmodel_update(changes)
    post.updated_at = utc_now()
    if not was_published and post.status == PostStatus.PUBLISHED:
        post.published_at = utc_now()
    elif post.status == PostStatus.DRAFT:
        post.published_at = None
    return repository.save(session, post)


def delete_post(session: Session, post_id: uuid.UUID) -> None:
    post = repository.get_by_id(session, post_id)
    if post is None:
        raise ResourceNotFoundError("Post not found")
    repository.delete(session, post)
