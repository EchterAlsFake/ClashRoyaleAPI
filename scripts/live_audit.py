"""Exercise every public endpoint against Supercell without logging credentials.

Run: uv run python scripts/live_audit.py --token-file token
Raw public responses stay in ignored .live/. Reports distinguish upstream errors,
client failures, and unavailable discovery data; a 404 alone never proves an outage.
"""

from __future__ import annotations

import argparse
import asyncio
import inspect
import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from clashroyaleapi import APIError, APIModel, Client, Page

REFERENCE = Path(__file__).resolve().parents[1] / "docs/api-reference.json"


def normalize(value: Any) -> Any:
    """Compare round trips while allowing documented timestamp normalization."""
    if isinstance(value, dict):
        return {k: normalize(v) for k, v in value.items()}
    if isinstance(value, list):
        return [normalize(v) for v in value]
    if isinstance(value, str):
        if re.fullmatch(r"\d{8}T\d{6}\.\d+Z", value):
            return datetime.strptime(value, "%Y%m%dT%H%M%S.%fZ").replace(tzinfo=UTC).isoformat()
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}T.*(?:Z|\+00:00)", value):
            return datetime.fromisoformat(value).isoformat()
    return value


def export(result: Any) -> Any:
    return [item.to_dict() for item in result] if isinstance(result, list) else result.to_dict()


class Audit:
    def __init__(self, client: Client, output: Path):
        self.client = client
        self.output = output
        self.records: list[dict[str, Any]] = []
        self.captured: dict[str, Any] = {}
        self.request_count = 0
        self.battle_modes: set[str] = set()
        original = client._session.get

        async def capture(*args: Any, **kwargs: Any):
            response = await original(*args, **kwargs)
            self.request_count += 1
            self.captured["http_status"] = response.status_code
            try:
                self.captured["data"] = response.json()
            except ValueError:
                self.captured["data"] = None
            return response

        client._session.get = capture

    async def call(self, method: str, **kwargs: Any) -> Any:
        self.captured = {}
        record: dict[str, Any] = {"method": method, "arguments": kwargs}
        result = None
        try:
            result = await getattr(self.client, method)(**kwargs)
            raw = self.captured["data"]
            if method == "get_player_battle_log" and isinstance(raw, list):
                self.battle_modes.update(row.get("type", "unknown") for row in raw)
            dumped = export(result)
            # Array-returning endpoints may have an upstream items envelope.
            if isinstance(result, list) and isinstance(raw, dict):
                raw = raw["items"]
            if isinstance(result, Page) and isinstance(raw, list):
                raw = {"items": raw}
            if normalize(raw) != normalize(dumped):
                raise AssertionError("Response data changed during model round trip")
            record["outcome"] = "passed"
            record["items"] = (
                len(result.items)
                if isinstance(result, Page)
                else len(result)
                if isinstance(result, list)
                else 1
            )
        except APIError as error:
            message = str(error)
            explicitly_disabled = error.status in (404, 410) and (
                "temporarily disabled" in message or "permanently removed" in message
            )
            status = self.captured.get("http_status")
            record.update(
                outcome="upstream_disabled"
                if explicitly_disabled
                else "upstream_error"
                if status and status >= 500
                else "unresolved_resource"
                if status == 404
                else "failed",
                error=type(error).__name__,
                message=message,
                reason=error.reason,
            )
        except Exception as error:
            record.update(outcome="failed", error=type(error).__name__, message=str(error))
        record["http_status"] = self.captured.get("http_status")
        self.records.append(record)
        filename = f"{len(self.records):03d}-{method}.json"
        (self.output / filename).write_text(
            json.dumps(
                {"record": record, "response": self.captured.get("data")},
                ensure_ascii=False,
                indent=2,
            )
            + "\n"
        )
        print(f"{method}: {record['outcome']} (HTTP {record['http_status']})", flush=True)
        return result if record["outcome"] == "passed" else None

    async def pages(self, method: str, kwargs: dict[str, Any], first: Page) -> None:
        after = first.paging.cursors.after
        if not after:
            return
        second = await self.call(method, **kwargs, after=after)
        if second is None:
            return
        before = second.paging.cursors.before
        if before:
            await self.call(method, **kwargs, before=before)
        # Exercise the public async iterator, including fetching page two.
        self.captured = {}
        count = 0
        iterator = getattr(self.client, "iter_" + method)(**kwargs)
        try:
            async for item in iterator:
                assert isinstance(item, APIModel)
                count += 1
                if count >= len(first.items) + 1:
                    break
            self.records.append(
                {
                    "method": "iter_" + method,
                    "outcome": "passed",
                    "items": count,
                    "http_status": self.captured.get("http_status"),
                }
            )
        except Exception as error:
            self.records.append(
                {"method": "iter_" + method, "outcome": "failed", "error": type(error).__name__}
            )
        finally:
            await iterator.aclose()


async def run(args):
    args.output.mkdir(parents=True, exist_ok=True)
    async with Client(args.token_file.read_text().strip(), max_attempts=1) as client:
        audit = Audit(client, args.output)
        clans = await audit.call("search_clans", name="royale", limit=3)
        clan_tag = args.clan_tag or (clans.items[0].tag if clans and clans.items else "#88Q2JCVL")
        clan = await audit.call("get_clan", clan_tag=clan_tag)
        player_tag = args.player_tag or (
            clan.member_list[0].tag if clan and clan.member_list else "#J92CYLP28"
        )
        seasons = await audit.call("get_seasons")
        season_id = seasons[-1].id if seasons else "2026-10"
        boards = await audit.call("get_leaderboards")
        board_id = args.leaderboard_id or next((b.id for b in boards or [] if b.name), 170000019)
        tournaments = await audit.call("search_tournaments", name="royale", limit=3)
        tournament_tag = args.tournament_tag or (
            tournaments.items[0].tag if tournaments and tournaments.items else "#2GG80C0Q"
        )
        globals_ = await audit.call("get_global_tournaments")
        global_tag = args.global_tournament_tag or (str(globals_[0].id) if globals_ else "#758209")
        leagues = [
            (b.id, league.get("id"))
            for b in boards or []
            for league in (b.leagues or [])
            if isinstance(league, dict) and league.get("id") is not None
        ]
        league_board, league_id = (
            (board_id, args.league_id)
            if args.league_id is not None
            else leagues[0]
            if leagues
            else (board_id, 1)
        )
        seeds = {
            "clan_tag": clan_tag,
            "player_tag": player_tag,
            "tournament_tag": tournament_tag,
            "location_id": "global",
            "season_id": season_id,
            "leaderboard_id": board_id,
            "league_id": league_id,
        }
        for operation in json.loads(REFERENCE.read_text())["operations"]:
            method = operation["python_method"]
            kwargs = {
                key: seeds[key]
                for key in inspect.signature(getattr(client, method)).parameters
                if key in seeds
            }
            if "limit" in inspect.signature(getattr(client, method)).parameters:
                kwargs["limit"] = 3
            if method.startswith("search_"):
                kwargs["name"] = "royale"
            if method in ("get_location", "search_clans"):
                kwargs["location_id"] = 57000094 if method == "search_clans" else "57000094"
            if method == "get_top_player_league_season_rankings":
                kwargs["season_id"] = "2022-09"  # Last Trophy Road era, still served.
            if method == "get_global_tournament_ranking":
                kwargs["tournament_tag"] = global_tag
            if method == "get_leaderboard_league":
                kwargs.update(leaderboard_id=league_board, league_id=league_id)
            result = await audit.call(method, **kwargs)
            if isinstance(result, Page):
                await audit.pages(method, kwargs, result)
        # Exercise distinct players and all battle modes present in their logs.
        if clan and clan.member_list:
            for member in clan.member_list[1:4]:
                await audit.call("get_player", player_tag=member.tag)
                await audit.call("get_player_battle_log", player_tag=member.tag)
        await audit.call(
            "search_clans",
            name="royale",
            location_id=57000094,
            min_members=10,
            max_members=50,
            min_score=1000,
            limit=3,
        )
        await audit.call("get_player", player_tag=player_tag.lstrip("#"))
        await audit.call("get_player", player_tag=player_tag.replace("#", "%23"))
        await audit.call("get_leaderboard", leaderboard_id=758209, limit=3)
        report = {
            "network_requests": audit.request_count,
            "battle_modes": sorted(audit.battle_modes),
            "checked_at": datetime.now(UTC).isoformat(),
            "discovery": {
                "active_global_tournaments": len(globals_ or []),
                "advertised_leagues": len(leagues),
            },
            "historical_global_tournament_source": "https://royaleapi.com/players/gt/leaderboard/758209",
            "summary": dict(Counter(r["outcome"] for r in audit.records)),
            "records": audit.records,
        }
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps(report["summary"]), flush=True)
        return (
            1
            if any(r["outcome"] == "failed" for r in audit.records)
            else 2
            if args.require_all
            and any(r["outcome"] == "unresolved_resource" for r in audit.records)
            else 0
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--token-file", type=Path, default=Path("token"))
    parser.add_argument("--output", type=Path, default=Path(".live/audit"))
    parser.add_argument("--report", type=Path, default=Path(".live/report.json"))
    parser.add_argument(
        "--require-all", action="store_true", help="Also fail on unresolved resources"
    )
    parser.add_argument("--clan-tag", default=None)
    parser.add_argument("--player-tag", default=None)
    parser.add_argument("--tournament-tag", default=None)
    parser.add_argument("--global-tournament-tag", default=None)
    parser.add_argument("--leaderboard-id", type=int, default=None)
    parser.add_argument("--league-id", type=int, default=None)
    raise SystemExit(asyncio.run(run(parser.parse_args())))


if __name__ == "__main__":
    main()
