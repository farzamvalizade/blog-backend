class DomainError(Exception):
    """Base exception for expected domain failures."""


class ResourceNotFoundError(DomainError):
    pass


class ResourceConflictError(DomainError):
    pass
