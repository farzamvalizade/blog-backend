import uuid

from sqlmodel import Session

from app.core.exceptions import ResourceConflictError, ResourceNotFoundError
from app.tags import repository
from app.tags.models import Tag
from app.tags.schemas import TagCreate, TagUpdate


def create_tag(session: Session, data: TagCreate) -> Tag:
    if repository.get_by_slug(session, data.slug):
        raise ResourceConflictError("A tag with this slug already exists")
    return repository.save(session, Tag.model_validate(data))


def update_tag(session: Session, tag_id: uuid.UUID, data: TagUpdate) -> Tag:
    tag = repository.get_by_id(session, tag_id)
    if tag is None:
        raise ResourceNotFoundError("Tag not found")
    if data.slug:
        existing = repository.get_by_slug(session, data.slug)
        if existing and existing.id != tag_id:
            raise ResourceConflictError("A tag with this slug already exists")
    tag.sqlmodel_update(data.model_dump(exclude_unset=True))
    return repository.save(session, tag)


def delete_tag(session: Session, tag_id: uuid.UUID) -> None:
    tag = repository.get_by_id(session, tag_id)
    if tag is None:
        raise ResourceNotFoundError("Tag not found")
    repository.delete(session, tag)
