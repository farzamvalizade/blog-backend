from sqlmodel import Session

from app.core.config import settings as app_settings
from app.core.time import utc_now
from app.site_settings import repository
from app.site_settings.models import SiteSettings
from app.site_settings.schemas import SiteSettingsUpdate


def get_or_create(session: Session) -> SiteSettings:
    settings = repository.get(session)
    if settings is None:
        settings = repository.save(
            session,
            SiteSettings(site_name=app_settings.PROJECT_NAME),
        )
    return settings


def update(session: Session, data: SiteSettingsUpdate) -> SiteSettings:
    settings = get_or_create(session)
    settings.sqlmodel_update(data.model_dump(exclude_unset=True))
    settings.updated_at = utc_now()
    return repository.save(session, settings)
