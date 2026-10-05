import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import SessionDep, get_current_superuser
from app.api.schemas import Message
from app.tags import repository, service
from app.tags.schemas import TagCreate, TagPublic, TagsPublic, TagUpdate

router = APIRouter(prefix="/tags", tags=["tags"])
admin_router = APIRouter(dependencies=[Depends(get_current_superuser)])


@router.get("/", response_model=TagsPublic)
def list_tags(
    session: SessionDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> TagsPublic:
    tags, count = repository.list_all(session, skip, limit)
    return TagsPublic(
        data=[TagPublic.model_validate(tag) for tag in tags],
        count=count,
    )


@admin_router.post("/", response_model=TagPublic, status_code=status.HTTP_201_CREATED)
def create_tag(session: SessionDep, data: TagCreate) -> TagPublic:
    return TagPublic.model_validate(service.create_tag(session, data))


@admin_router.patch("/{tag_id}", response_model=TagPublic)
def update_tag(tag_id: uuid.UUID, session: SessionDep, data: TagUpdate) -> TagPublic:
    return TagPublic.model_validate(service.update_tag(session, tag_id, data))


@admin_router.delete("/{tag_id}", response_model=Message)
def delete_tag(tag_id: uuid.UUID, session: SessionDep) -> Message:
    service.delete_tag(session, tag_id)
    return Message(message="Tag deleted")


router.include_router(admin_router)
