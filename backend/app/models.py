"""Table-model registry used by Alembic metadata discovery."""

from app.auth.models import User
from app.categories.models import Category
from app.posts.models import Post
from app.site_settings.models import SiteSettings
from app.tags.models import PostTagLink, Tag

__all__ = [
    "Category",
    "Post",
    "PostTagLink",
    "SiteSettings",
    "Tag",
    "User",
]
