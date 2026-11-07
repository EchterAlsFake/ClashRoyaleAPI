## Installation {#installation}

ClashRoyaleAPI is a Python client for the **official Clash Royale REST API**. It fetches players, clans, cards, tournaments and rankings. All network calls are asynchronous.

Requires **Python 3.12 or newer**. Install the package from PyPI:

```bash
python -m pip install --upgrade async-royale-client
```

The package name used by pip is `async-royale-client`; the Python import is `clashroyaleapi`.

## Get an API token {#authentication}

1. Create an account at the [official developer portal](https://developer.clashroyale.com/).
2. Create an API key and allowlist the **public IP address of the machine running your code**. For a deployed bot or website, use your server's outgoing IP.
3. Copy the token into an environment variable. Keep it out of your source code and Git repository.

On Linux or macOS:

```bash
export CLASH_ROYALE_API_TOKEN="your-api-token"
```

On Windows PowerShell:

```powershell
$env:CLASH_ROYALE_API_TOKEN = "your-api-token"
```

A 403 response usually means the token or the allowed IP needs checking. Your local IP, such as `192.168.x.x`, is not your outgoing public IP.

## Your first request {#quickstart}

Save this complete example as `example.py`. Replace the player tag with one from your in-game profile, then run `python example.py` in the terminal where you set the token.

```python
import asyncio
import os

from clashroyaleapi import Client


async def main():
    token = os.environ["CLASH_ROYALE_API_TOKEN"]

    async with Client(api_token=token) as client:
        player = await client.get_player("#J92CYLP28")  # Replace with your tag
        print(f"{player.name}: {player.trophies} trophies")

        if player.clan is not None:
            print(f"Clan: {player.clan.name}")


asyncio.run(main())
```

`await` waits for the API response. `async with` opens the client and closes its connections when you finish. Reuse one client for several requests. If your bot framework or notebook already runs an event loop, call `await main()` there instead of `asyncio.run(main())`.

**Next:** try the [common tasks](#common-tasks), learn [pagination](#pagination), or jump to the [player methods](#players).

## Common tasks {#common-tasks}

The following snippets go **inside the `async with Client(...) as client:` block** from the example above.

### Find a clan and list its members

```python
clans = await client.search_clans(name="royale", limit=5)

if clans.items:
    clan = await client.get_clan(clans.items[0].tag)
    print(clan.name, clan.members)

    async for member in client.iter_get_clan_members(clan.tag, limit=50):
        print(member.name, member.trophies)
```

Clan searches need at least one filter. A name must contain at least three characters. You can also filter with `location_id`, `min_members`, `max_members` and `min_score`.

### Read a player's recent battles

```python
battles = await client.get_player_battle_log("#J92CYLP28")

for battle in battles:
    print(battle.type, battle.battle_time)
    for teammate in battle.team or []:
        print(teammate.name, teammate.crowns)
```

Battle logs return a regular Python list. Iterate it with `for`; the request itself uses `await`.

### Browse cards and current rankings

```python
cards = await client.get_cards()
for card in cards.items:
    print(card.name, card.elixir_cost)

rankings = await client.get_player_path_of_legend_ranking("global", limit=10)
for player in rankings.items:
    print(player.rank, player.name, player.elo_rating)
```

Use `"global"` for worldwide rankings, or a location ID from `get_locations()` for a supported region. For a single location's details, pass its numeric ID as a string to `get_location()`.

## Pages and async iterators {#pagination}

The client returns one of three shapes:

| Result | How to read it | Example |
| --- | --- | --- |
| A model | Access its attributes | `player.name` |
| `Page[T]` | Iterate `.items`, or use an async iterator | `clans.items` |
| A Python list | Use a normal `for` loop | `battles` |

**One page** is useful for a preview or a table:

```python
page = await client.get_clan_members("#88Q2JCVL", limit=10)
for member in page.items:
    print(member.name)

# Request the next page only when the API supplies a cursor.
if page.paging.cursors.after:
    next_page = await client.get_clan_members(
        "#88Q2JCVL",
        limit=10,
        after=page.paging.cursors.after,
    )
```

**An async iterator** follows the API's available pages for you:

```python
async for member in client.iter_get_clan_members("#88Q2JCVL", limit=10):
    print(member.name)
```

`limit` is the requested **page size**, not a total item cap. Every paginated method has an `iter_` companion. Pass `before` to traverse backwards; do not combine `before` and `after`. Some upstream endpoints return all items without supplying another cursor.

## Working with response models {#response-models}

Models expose Python-style `snake_case` fields. Optional fields can be `None`; for example, a player may have no clan. Unknown API fields are retained, so new upstream data remains accessible in exported JSON.

```python
player = await client.get_player("#J92CYLP28")
print(player.collection_level)

for card in player.cards or []:
    print(card.name, card.level)

# A JSON-compatible dictionary using the original API names.
data = player.to_dict()
print(data["collectionLevel"])

# A serialized JSON string, also using the API names.
print(player.model_dump_json(by_alias=True, exclude_unset=True))
```

Known timestamps, such as `battle.battle_time`, become timezone-aware UTC `datetime` objects. Unresolved structures retain their original JSON values. The [model reference](#models-reference) lists available attributes and their API aliases.

## Configure the client {#configuration}

Defaults suit a small script. For a long-running bot or application, reuse a client and adjust the options you need:

```python
async with Client(
    api_token=token,
    timeout=20,
    max_clients=10,
    max_attempts=3,
    cache_ttl=30,
    cache_size=256,
) as client:
    player = await client.get_player("#J92CYLP28")
```

| Option | Default | Meaning |
| --- | --- | --- |
| `api_token` | Required | Your Supercell API token |
| `timeout` | `20` | Request timeout in seconds |
| `max_clients` | `10` | Maximum concurrent curl handles |
| `max_attempts` | `3` | Total attempts per GET request, from 1 to 3 |
| `cache_ttl` | `0` | Cache lifetime in seconds; zero disables caching |
| `cache_size` | `256` | Maximum cached responses per client |
| `proxy` | `None` | Optional proxy URL |
| `verify` | `True` | TLS certificate verification |
| `base_url` | `https://api.clashroyale.com/v1` | API base URL; your token is sent here |

Retries cover network failures, HTTP 429 and HTTP 5xx, with bounded delays. Caching is opt-in and stores successful responses only. If you manage the lifecycle manually, call `await client.close()` before the event loop ends.

## Handle errors {#error-handling}

Catch specific errors where your application can recover. All request exceptions inherit from `APIError` and expose `status`, `reason` and `detail` when available.

```python
from clashroyaleapi import APIError, AuthenticationError, NotFound, RateLimitExceeded

try:
    player = await client.get_player("#J92CYLP28")
except AuthenticationError:
    print("Check your API token and public IP allowlist.")
except NotFound:
    print("The player was not found, or this upstream resource is unavailable.")
except RateLimitExceeded:
    print("The API is still rate limited after retries. Try again later.")
except APIError as error:
    print(f"API request failed: {error.status} / {error.reason}")
```

| Exception | When it is raised |
| --- | --- |
| `InvalidParameter` | HTTP 400: rejected parameters |
| `AuthenticationError` | HTTP 401 or 403: credentials or access |
| `NotFound` | HTTP 404: missing resource or unavailable route |
| `RateLimitExceeded` | HTTP 429 after retries |
| `ServerError` | HTTP 5xx after retries |
| `NetworkError` | Transport failure after retries |
| `InvalidResponse` | Invalid JSON or an unexpected response shape |
| `APIError` | Other non-200 responses, including HTTP 410 |

Invalid local arguments raise `ValueError`. Using a closed client raises `RuntimeError`. Cancellation propagates to the caller.

## Availability and compatibility {#availability}

The client wraps all **30 documented GET operations**. Live verification successfully exercised 26 operations; two are explicitly disabled or removed by Supercell, and two lacked working active resources. See the [live audit report](https://github.com/EchterAlsFake/ClashRoyaleAPI/blob/main/docs/live-testing.md) for details and reproduction instructions.

- **Clan war log:** Supercell returns an explicit temporary-disable message.
- **Current clan war:** Supercell returns HTTP 410, permanently removed. Use current river-race data for modern clan wars.
- **Trophy Road player rankings:** deprecated and documented to return an empty list. Use Path of Legend rankings for current competitive standings.
- **Global-tournament and league-specific rankings:** availability depends on upstream resources. A 404 alone does not establish that an entire route is disabled.

Moving from the unfinished client? Import `Client` from `clashroyaleapi`, await network calls, and use model fields such as `player.cards` instead of the old getter generators. `get_player_chest_cycle()` is now `get_player_upcoming_chests()`; read its `.items` list.

This is an unofficial project, independent of Supercell. Licensed under GPL-3.0-only; Clash Royale trademarks and game content belong to their respective owners.
