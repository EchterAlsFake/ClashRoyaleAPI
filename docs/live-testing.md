# Live API verification

Run a real network audit with an IP-allowlisted token:

```sh
uv run python scripts/live_audit.py --token-file token
```

The command uses the public Client methods and the real curl transport, with caching disabled and one attempt per request. It discovers clans, members, players, tournaments, seasons and leaderboard IDs from API responses. It requests every one of the 30 operations, follows available forward and backward cursors, exercises public async iterators and checks response-model round trips. It also tries multiple profiles/battle logs, all clan-search filters, and three tag formats. Names and tags in the offline regression fixtures have been replaced; field structure and scalar types come from real responses.

Raw responses and the full report are written to ignored `.live/`. The token is never written into reports or committed. The report explicitly distinguishes successful checks, upstream-disabled routes, unresolved resources and client failures. A plain 404 is not automatically excused as an upstream outage. Client failures give a nonzero exit code; `--require-all` also fails on unresolved resources. Pass `--global-tournament-tag`, `--leaderboard-id` and `--league-id` to supply live resources when catalogs do not advertise them.

## Verified snapshot

See [machine-readable results](live-audit.json) for the timestamp and per-operation results. On 7 November 2026, 86 real HTTP requests produced 72 passing checks (including pagination/iterator checks), two explicitly disabled routes, and two unresolved resources. All 30 routes were attempted; 26 distinct operations returned successful, validated responses. Five battle modes were observed in the final audit. Empty global-tournament catalogs and deprecated empty player rankings count as valid empty responses, not proof of populated-model coverage.

| Operation | Live result |
|---|---|
| Clan war log | 404, explicit temporary-disable message |
| Current clan war | 410, explicit permanent-removal message |
| Global tournament rankings | 404 for a known historical tournament; no active tournaments were advertised |
| League-specific leaderboard | 404 for the fallback sample; no league IDs were advertised, so successful validation remains pending |

The historical tournament was found in [RoyaleAPI's tournament archive](https://royaleapi.com/players/gt/leaderboard/758209). Its newer `/leaderboard/758209` route succeeds, while the older global-tournament-ranking route returns 404. Both hash-prefixed and numeric forms were probed directly for the older route. The current API catalog does not provide a league ID for the league-specific route; guessing an ID cannot establish success or prove the whole route is broken.

## Corrections from live data

- `get_leaderboard` returns `Page[LeaderboardEntry]`, including typed rank, score and clan fields. The official Swagger export incorrectly described the response using leaderboard catalog objects.
- `get_seasons_v2` returns `list[LeagueSeasonV2]` with code, unique_id and end_time fields. All three fields were null in the observed upstream snapshot.
- Path of Legend rows expose `elo_rating`; events expose `event_tag`.

These checks establish endpoint and observed-payload coverage. They do not establish every game mode, future response field, or every optional-field combination. Live checks stay outside ordinary CI because API tokens are IP-restricted; deterministic regression tests run on the full CI matrix.
