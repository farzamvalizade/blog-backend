from sqlmodel import Session

from app.site_settings.models import SiteSettings


def get(session: Session) -> SiteSettings | None:
    return session.get(SiteSettings, 1)


def save(session: Session, settings: SiteSettings) -> SiteSettings:
    session.add(settings)
    session.commit()
    session.refresh(settings)
    return settings
