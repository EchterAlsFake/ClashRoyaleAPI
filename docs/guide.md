# User guide

## Authentication and lifecycle

Generate a token in the official Clash Royale developer dashboard and allowlist your outgoing public IP. Pass the token explicitly; examples read `CLASH_ROYALE_API_TOKEN`. Never embed credentials in code. Use the client within one asyncio event loop and close it before that loop ends.

## Configuration

`Client(api_token, *, timeout=20, proxy=None, verify=True, max_clients=10, base_url="https://api.clashroyale.com/v1", max_attempts=3, cache_ttl=0, cache_size=256)`

Timeout is in seconds; `max_clients` bounds pooled curl handles. `proxy` accepts a proxy URL. TLS certificate verification defaults to enabled. A custom base URL allows a caller-selected API proxy or local testing; your bearer token is sent to that URL. Redirects are disabled. There is no browser impersonation requirement.

`max_attempts` is 1–3. Retried failures are network errors, HTTP 429, and HTTP 5xx. Backoff starts at 0.5 seconds. Retry-After supports seconds and HTTP dates, capped at 30 seconds. Cancellation propagates immediately.

`cache_ttl=0` disables caching. Positive TTL enables a bounded per-client LRU cache. Keys include path and query parameters. Only successful JSON results are cached; empty results are valid cache entries. Cached data is copied before conversion to prevent mutation of later responses.

## Responses and pagination

Models use snake_case attributes; missing optional fields are None. Unknown fields survive `to_dict()`. Known nested resources are typed; unresolved or undocumented structures remain JSON values. This export included nine expanded object schemas; conservative convenience fields supplement collapsed nested schemas. This is endpoint-complete coverage, not a claim of an exhaustive upstream schema.

Paginated methods return `Page[T]`. Access `.items`, `.paging.cursors.after` and `.paging.cursors.before`. Additional envelope fields, such as card catalog `supportItems`, remain accessible as retained extras and through `to_dict()`.

Call `iter_get_clan_members(clan_tag, limit=100)` or the corresponding `iter_` method to traverse pages. `limit` is the upstream page size, not a total item limit. Passing `before` traverses backwards; otherwise iterators follow `after`. Iteration stops at an empty page or missing cursor. A repeated cursor raises InvalidResponse to prevent an endless loop. Do not pass both cursors.

Tags accept `ABC`, `#ABC`, or `%23ABC` and are encoded once. Query parameters use Python snake_case and are serialized with official camelCase names. Clan search requires at least one filter; name searches require at least three characters. Search ordering is unspecified upstream.

## Errors

All library request exceptions inherit APIError, with `.status`, `.reason`, and `.detail`. Catch AuthenticationError for 401/403, InvalidParameter for 400, NotFound for 404, RateLimitExceeded for 429, ServerError for 5xx, NetworkError for transfer failures, and InvalidResponse for malformed JSON or response shapes. Other non-200 responses raise APIError. Invalid local arguments raise ValueError. Closed clients raise RuntimeError.

```python
from clashroyaleapi import Client, AuthenticationError, RateLimitExceeded

async def lookup(token, tag):
    async with Client(token) as client:
        try:
            return await client.get_player(tag)
        except AuthenticationError:
            print("Check the token and your public IP allowlist")
        except RateLimitExceeded:
            print("The API remains rate limited after retries")
```

## Upstream limitations

The reference is the user-provided rendered official Swagger UI export, identified by SHA-256 in api-reference.json. Its leaderboard models reference a missing `List` definition. Those fields retain raw data. Location Trophy Road player rankings are deprecated and documented to always return an empty list; use Path of Legend endpoints instead. Legacy clan-war endpoints may be unavailable upstream. Related models such as VerifyTokenRequest or RegisterMatchRequest do not establish public routes; no speculative endpoints are implemented. There is no standalone challenges operation in this snapshot.
