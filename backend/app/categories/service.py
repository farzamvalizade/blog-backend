import uuid

from sqlmodel import Session

from app.categories import repository
from app.categories.models import Category
from app.categories.schemas import CategoryCreate, CategoryUpdate
from app.core.exceptions import ResourceConflictError, ResourceNotFoundError
from app.core.time import utc_now


def create_category(session: Session, data: CategoryCreate) -> Category:
    if repository.get_by_slug(session, data.slug):
        raise ResourceConflictError("A category with this slug already exists")
    return repository.save(session, Category.model_validate(data))


def update_category(
    session: Session,
    category_id: uuid.UUID,
    data: CategoryUpdate,
) -> Category:
    category = repository.get_by_id(session, category_id)
    if category is None:
        raise ResourceNotFoundError("Category not found")
    if data.slug:
        existing = repository.get_by_slug(session, data.slug)
        if existing and existing.id != category_id:
            raise ResourceConflictError("A category with this slug already exists")
    category.sqlmodel_update(data.model_dump(exclude_unset=True))
    category.updated_at = utc_now()
    return repository.save(session, category)


def delete_category(session: Session, category_id: uuid.UUID) -> None:
    category = repository.get_by_id(session, category_id)
    if category is None:
        raise ResourceNotFoundError("Category not found")
    repository.delete(session, category)
