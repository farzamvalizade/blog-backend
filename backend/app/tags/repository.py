import uuid

from sqlmodel import Session, col, func, select

from app.tags.models import Tag


def list_all(session: Session, skip: int, limit: int) -> tuple[list[Tag], int]:
    count = session.exec(select(func.count()).select_from(Tag)).one()
    tags = session.exec(
        select(Tag).order_by(Tag.name).offset(skip).limit(limit)
    ).all()
    return list(tags), count


def get_by_id(session: Session, tag_id: uuid.UUID) -> Tag | None:
    return session.get(Tag, tag_id)


def get_by_ids(session: Session, tag_ids: list[uuid.UUID]) -> list[Tag]:
    if not tag_ids:
        return []
    return list(session.exec(select(Tag).where(col(Tag.id).in_(tag_ids))).all())


def get_by_slug(session: Session, slug: str) -> Tag | None:
    return session.exec(select(Tag).where(Tag.slug == slug)).first()


def save(session: Session, tag: Tag) -> Tag:
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag


def delete(session: Session, tag: Tag) -> None:
    session.delete(tag)
    session.commit()
