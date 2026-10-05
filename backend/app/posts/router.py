import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import CurrentSuperuser, SessionDep, get_current_superuser
from app.core.exceptions import ResourceNotFoundError
from app.models import Message
from app.posts import repository, service
from app.posts.schemas import PostCreate, PostPublic, PostsPublic, PostUpdate

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=PostsPublic)
def list_published_posts(
    session: SessionDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> PostsPublic:
    posts, count = repository.list_published(session, skip, limit)
    return PostsPublic(
        data=[PostPublic.model_validate(post) for post in posts],
        count=count,
    )


@router.get(
    "/admin",
    response_model=PostsPublic,
    dependencies=[Depends(get_current_superuser)],
)
def list_all_posts(
    session: SessionDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> PostsPublic:
    posts, count = repository.list_all(session, skip, limit)
    return PostsPublic(
        data=[PostPublic.model_validate(post) for post in posts],
        count=count,
    )


@router.get("/{slug}", response_model=PostPublic)
def read_published_post(slug: str, session: SessionDep) -> PostPublic:
    post = repository.get_by_slug(session, slug, published_only=True)
    if post is None:
        raise ResourceNotFoundError("Post not found")
    return PostPublic.model_validate(post)


@router.post("/", response_model=PostPublic, status_code=status.HTTP_201_CREATED)
def create_post(
    session: SessionDep,
    current_user: CurrentSuperuser,
    data: PostCreate,
) -> PostPublic:
    return PostPublic.model_validate(
        service.create_post(session, data, current_user)
    )


@router.patch(
    "/{post_id}",
    response_model=PostPublic,
    dependencies=[Depends(get_current_superuser)],
)
def update_post(
    post_id: uuid.UUID,
    session: SessionDep,
    data: PostUpdate,
) -> PostPublic:
    return PostPublic.model_validate(service.update_post(session, post_id, data))


@router.delete(
    "/{post_id}",
    response_model=Message,
    dependencies=[Depends(get_current_superuser)],
)
def delete_post(post_id: uuid.UUID, session: SessionDep) -> Message:
    service.delete_post(session, post_id)
    return Message(message="Post deleted")
