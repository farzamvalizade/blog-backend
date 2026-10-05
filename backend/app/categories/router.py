import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import SessionDep, get_current_superuser
from app.api.schemas import Message
from app.categories import repository, service
from app.categories.schemas import (
    CategoriesPublic,
    CategoryCreate,
    CategoryPublic,
    CategoryUpdate,
)

router = APIRouter(prefix="/categories", tags=["categories"])
admin_router = APIRouter(dependencies=[Depends(get_current_superuser)])


@router.get("/", response_model=CategoriesPublic)
def list_categories(
    session: SessionDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> CategoriesPublic:
    categories, count = repository.list_all(session, skip, limit)
    return CategoriesPublic(
        data=[CategoryPublic.model_validate(category) for category in categories],
        count=count,
    )


@admin_router.post("/", response_model=CategoryPublic, status_code=status.HTTP_201_CREATED)
def create_category(session: SessionDep, data: CategoryCreate) -> CategoryPublic:
    return CategoryPublic.model_validate(service.create_category(session, data))


@admin_router.patch("/{category_id}", response_model=CategoryPublic)
def update_category(
    category_id: uuid.UUID,
    session: SessionDep,
    data: CategoryUpdate,
) -> CategoryPublic:
    return CategoryPublic.model_validate(
        service.update_category(session, category_id, data)
    )


@admin_router.delete("/{category_id}", response_model=Message)
def delete_category(category_id: uuid.UUID, session: SessionDep) -> Message:
    service.delete_category(session, category_id)
    return Message(message="Category deleted")


router.include_router(admin_router)
