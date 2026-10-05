from fastapi import APIRouter, Depends

from app.api.deps import SessionDep, get_current_superuser
from app.site_settings import service
from app.site_settings.schemas import SiteSettingsPublic, SiteSettingsUpdate

router = APIRouter(prefix="/site", tags=["site"])


@router.get("/", response_model=SiteSettingsPublic)
def read_site_settings(session: SessionDep) -> SiteSettingsPublic:
    return SiteSettingsPublic.model_validate(service.get_or_create(session))


@router.patch(
    "/",
    response_model=SiteSettingsPublic,
    dependencies=[Depends(get_current_superuser)],
)
def update_site_settings(
    session: SessionDep,
    data: SiteSettingsUpdate,
) -> SiteSettingsPublic:
    return SiteSettingsPublic.model_validate(service.update(session, data))
