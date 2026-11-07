"""Public exceptions with structured upstream error details."""

from typing import Any


class APIError(Exception):
    def __init__(
        self,
        message: str,
        *,
        status: int | None = None,
        reason: str | None = None,
        detail: Any = None,
    ):
        super().__init__(message)
        self.status = status
        self.reason = reason
        self.detail = detail


class InvalidParameter(APIError):
    """The API rejected request parameters."""


class AuthenticationError(APIError):
    """Missing credentials, insufficient access, or an IP allowlist mismatch."""


class NotFound(APIError):
    """Resource or upstream endpoint unavailable."""


class RateLimitExceeded(APIError):
    """Request throttled after retry attempts."""


class ServerError(APIError):
    """Upstream server error or maintenance."""


class NetworkError(APIError):
    """Connection or transfer failure."""


class InvalidResponse(APIError):
    """Malformed JSON or an unexpected response shape."""


__all__ = [
    "APIError",
    "AuthenticationError",
    "InvalidParameter",
    "InvalidResponse",
    "NetworkError",
    "NotFound",
    "RateLimitExceeded",
    "ServerError",
]
