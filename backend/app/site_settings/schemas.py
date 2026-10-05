from datetime import datetime

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class SiteSettingsUpdate(SQLModel):
    site_name: str | None = Field(default=None, min_length=1, max_length=120)
    tagline: str | None = Field(default=None, max_length=255)
    description: str | None = None
    contact_email: EmailStr | None = Field(default=None, max_length=255)
    logo_url: str | None = Field(default=None, max_length=2048)
    favicon_url: str | None = Field(default=None, max_length=2048)
    footer_text: str | None = Field(default=None, max_length=500)
    seo_title: str | None = Field(default=None, max_length=70)
    seo_description: str | None = Field(default=None, max_length=160)


class SiteSettingsPublic(SiteSettingsUpdate):
    site_name: str
    updated_at: datetime
