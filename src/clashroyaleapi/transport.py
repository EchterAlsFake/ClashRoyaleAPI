"""Shared async curl transport, cache and pagination."""

from __future__ import annotations

import asyncio
import time
from collections import OrderedDict
from collections.abc import AsyncIterator
from copy import deepcopy
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from typing import Any, TypeVar
from urllib.parse import quote, unquote, urlsplit

from curl_cffi.requests import AsyncSession
from curl_cffi.requests.exceptions import RequestException
from pydantic import ValidationError

from .errors import (
    APIError,
    AuthenticationError,
    InvalidParameter,
    InvalidResponse,
    NetworkError,
    NotFound,
    RateLimitExceeded,
    ServerError,
)
from .models import APIModel, Page

T = TypeVar("T", bound=APIModel)


class Transport:
    def __init__(
        self,
        api_token: str,
        *,
        timeout: float = 20,
        proxy: str | None = None,
        verify: bool = True,
        max_clients: int = 10,
        base_url: str = "https://api.clashroyale.com/v1",
        max_attempts: int = 3,
        cache_ttl: float = 0,
        cache_size: int = 256,
    ):
        if not api_token.strip():
            raise ValueError("api_token must not be empty")
        if timeout <= 0 or max_clients < 1 or not 1 <= max_attempts <= 3:
            raise ValueError("timeout/concurrency must be positive; max_attempts must be 1–3")
        if cache_ttl < 0 or cache_size < 1:
            raise ValueError("cache_ttl must be nonnegative and cache_size positive")
        url = urlsplit(base_url)
        if url.scheme not in ("http", "https") or not url.netloc or url.query or url.fragment:
            raise ValueError("base_url must be an HTTP(S) URL without query or fragment")
        self._base_url = base_url.rstrip("/")
        self._session: AsyncSession = AsyncSession(
            headers={"Authorization": f"Bearer {api_token}", "Accept": "application/json"},
            timeout=timeout,
            proxy=proxy,
            verify=verify,
            max_clients=max_clients,
            allow_redirects=False,
        )
        self._max_attempts = max_attempts
        self._cache_ttl = cache_ttl
        self._cache_size = cache_size
        self._cache: OrderedDict[str, tuple[float, Any]] = OrderedDict()
        self._closed = False

    async def __aenter__(self):
        if self._closed:
            raise RuntimeError("Client is closed")
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.close()

    async def close(self) -> None:
        """Close pooled connections. Safe to call repeatedly."""
        if not self._closed:
            await self._session.close()
            self._cache.clear()
            self._closed = True

    @staticmethod
    def _delay(headers: Any, attempt: int) -> float:
        value = headers.get("Retry-After")
        if value:
            try:
                return min(30.0, max(0.0, float(value)))
            except ValueError:
                try:
                    date = parsedate_to_datetime(value)
                    if date.tzinfo is None:
                        date = date.replace(tzinfo=UTC)
                    return min(30.0, max(0.0, (date - datetime.now(UTC)).total_seconds()))
                except (ValueError, TypeError, OverflowError):
                    pass
        return min(8.0, 0.5 * 2**attempt)

    async def _get(self, path: str, path_params: dict[str, Any], params: dict[str, Any]) -> Any:
        if self._closed:
            raise RuntimeError("Client is closed")
        params = {k: v for k, v in params.items() if v is not None}
        if "before" in params and "after" in params:
            raise ValueError("Specify before or after, not both")
        if "limit" in params and params["limit"] <= 0:
            raise ValueError("limit must be positive")
        if path in ("/clans", "/tournaments"):
            filters = set(params) - {"limit", "after", "before"}
            if not filters or (path == "/tournaments" and not params.get("name")):
                raise ValueError("Search requires a filter")
            if "name" in params and len(params["name"]) < 3:
                raise ValueError("Search name must contain at least three characters")
        if params.get("minMembers", 0) > params.get("maxMembers", float("inf")):
            raise ValueError("min_members must not exceed max_members")
        for key, value in path_params.items():
            value = unquote(str(value)).strip()
            if key.endswith("Tag"):
                value = "#" + value.lstrip("#").upper()
                if len(value) == 1:
                    raise ValueError("Tag must not be empty")
            path = path.replace("{" + key + "}", quote(value, safe=""))
        key = repr((path, sorted(params.items())))
        cached = self._cache.get(key)
        if cached is not None:
            if cached[0] > time.monotonic():
                self._cache.move_to_end(key)
                return deepcopy(cached[1])
            del self._cache[key]
        for attempt in range(self._max_attempts):
            try:
                response = await self._session.get(self._base_url + path, params=params)
            except RequestException:
                if attempt + 1 < self._max_attempts:
                    await asyncio.sleep(self._delay({}, attempt))
                    continue
                raise NetworkError("API network request failed") from None
            status = response.status_code
            if (status == 429 or 500 <= status < 600) and attempt + 1 < self._max_attempts:
                await asyncio.sleep(self._delay(response.headers, attempt))
                continue
            try:
                data = response.json()
            except (ValueError, UnicodeDecodeError):
                if status == 200:
                    raise InvalidResponse("API returned invalid JSON", status=status) from None
                data = {}
            if status != 200:
                error = {
                    400: InvalidParameter,
                    401: AuthenticationError,
                    403: AuthenticationError,
                    404: NotFound,
                    429: RateLimitExceeded,
                }.get(status, ServerError if status >= 500 else APIError)
                payload = data if isinstance(data, dict) else {}
                raise error(
                    str(payload.get("message") or f"API request failed (HTTP {status})"),
                    status=status,
                    reason=payload.get("reason"),
                    detail=payload.get("detail"),
                )
            if not isinstance(data, (dict, list)):
                raise InvalidResponse("Expected an API JSON object or array", status=status)
            if self._cache_ttl:
                self._cache[key] = (time.monotonic() + self._cache_ttl, deepcopy(data))
                self._cache.move_to_end(key)
                while len(self._cache) > self._cache_size:
                    self._cache.popitem(last=False)
            return data
        raise AssertionError("Unreachable retry state")

    @staticmethod
    def _model(data: Any, model: type[T]) -> T:
        try:
            return model.model_validate(data)
        except ValidationError:
            raise InvalidResponse(f"Unexpected {model.__name__} response shape") from None

    @classmethod
    def _list(cls, data: Any, model: type[T]) -> list[T]:
        items = data.get("items") if isinstance(data, dict) else data
        if not isinstance(items, list):
            raise InvalidResponse("Expected a JSON array or an items array")
        return [cls._model(item, model) for item in items]

    @classmethod
    def _page(cls, data: Any, model: type[T]) -> Page[T]:
        if isinstance(data, list):
            data = {"items": data}
        if not isinstance(data, dict) or not isinstance(data.get("items"), list):
            raise InvalidResponse("Expected a paginated items array")
        return cls._model(data, Page[model])  # type: ignore[valid-type]

    async def _iterate(
        self, path: str, paths: dict[str, Any], params: dict[str, Any], model: type[T]
    ) -> AsyncIterator[T]:
        params = params.copy()
        backwards = params.get("before") is not None
        direction = "before" if backwards else "after"
        seen = {params[direction]} if params.get(direction) else set()
        while True:
            page = self._page(await self._get(path, paths, params), model)
            for item in page.items:
                yield item
            cursor = getattr(page.paging.cursors, direction)
            if not page.items or not cursor:
                return
            if cursor in seen:
                raise InvalidResponse("API repeated a pagination cursor")
            seen.add(cursor)
            params[direction] = cursor
