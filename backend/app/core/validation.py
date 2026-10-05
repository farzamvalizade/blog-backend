import re

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def validate_slug(value: str | None) -> str | None:
    if value is not None and not SLUG_PATTERN.fullmatch(value):
        raise ValueError(
            "Slug must contain lowercase letters, numbers, and single hyphens only"
        )
    return value
