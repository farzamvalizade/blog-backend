import uuid

from sqlmodel import Session, func, select

from app.categories.models import Category


def list_all(session: Session, skip: int, limit: int) -> tuple[list[Category], int]:
    count = session.exec(select(func.count()).select_from(Category)).one()
    categories = session.exec(
        select(Category).order_by(Category.name).offset(skip).limit(limit)
    ).all()
    return list(categories), count


def get_by_id(session: Session, category_id: uuid.UUID) -> Category | None:
    return session.get(Category, category_id)


def get_by_slug(session: Session, slug: str) -> Category | None:
    return session.exec(select(Category).where(Category.slug == slug)).first()


def save(session: Session, category: Category) -> Category:
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


def delete(session: Session, category: Category) -> None:
    session.delete(category)
    session.commit()
