from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import Column, DateTime, Text
from sqlmodel import Field, SQLModel

from app.core.time import utc_now


class SiteSettings(SQLModel, table=True):
    __tablename__ = "site_settings"

    id: int = Field(default=1, primary_key=True)
    site_name: str = Field(max_length=120)
    tagline: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, sa_type=Text)
    contact_email: EmailStr | None = Field(default=None, max_length=255)
    logo_url: str | None = Field(default=None, max_length=2048)
    favicon_url: str | None = Field(default=None, max_length=2048)
    footer_text: str | None = Field(default=None, max_length=500)
    seo_title: str | None = Field(default=None, max_length=70)
    seo_description: str | None = Field(default=None, max_length=160)
    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
