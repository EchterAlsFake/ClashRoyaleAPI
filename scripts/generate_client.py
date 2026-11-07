"""Generate explicit typed endpoint methods and models from the audited reference."""

import json
import re
from pathlib import Path


def snake(s):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()


def main():
    ref = json.loads(Path("docs/api-reference.json").read_text())
    names = {
        "getRiverRaceWarLog": "get_clan_river_race_log",
        "getPlayerBattles": "get_player_battle_log",
        "getTopPlayerLeagueSeasonHandler": "get_season",
        "listTopPlayerLeagueSeasonsHandler": "get_seasons",
        "listTopPlayerLeagueSeasonsV2Handler": "get_seasons_v2",
        "getTrailEvents": "get_events",
    }
    # Fields omitted by collapsed Swagger models: conservative, optional convenience fields.
    extra = {
        "Item": {
            "id": "integer",
            "name": "string",
            "maxLevel": "integer",
            "maxEvolutionLevel": "integer",
            "rarity": "string",
            "elixirCost": "integer",
            "iconUrls": "object",
        },
        "PlayerItemLevel": {
            "id": "integer",
            "name": "string",
            "level": "integer",
            "maxLevel": "integer",
            "count": "integer",
            "starLevel": "integer",
            "evolutionLevel": "integer",
            "rarity": "string",
            "elixirCost": "integer",
            "iconUrls": "object",
        },
        "PlayerClan": {"tag": "string", "name": "string", "badgeId": "integer"},
        "PlayerRankingClan": {"tag": "string", "name": "string", "badgeId": "integer"},
        "Arena": {"id": "integer", "name": "string"},
        "ClanMember": {
            "tag": "string",
            "name": "string",
            "role": "string",
            "lastSeen": "string",
            "expLevel": "integer",
            "trophies": "integer",
            "clanRank": "integer",
            "previousClanRank": "integer",
            "donations": "integer",
            "donationsReceived": "integer",
            "arena": "Arena",
        },
        "Battle": {
            "type": "string",
            "battleTime": "string",
            "isLadderTournament": "boolean",
            "isHostedMatch": "boolean",
            "deckSelection": "string",
            "leagueNumber": "integer",
            "gameMode": "GameMode",
            "arena": "Arena",
            "team": "PlayerBattleDataList",
            "opponent": "PlayerBattleDataList",
        },
        "PlayerBattleData": {
            "tag": "string",
            "name": "string",
            "crowns": "integer",
            "kingTowerHitPoints": "integer",
            "princessTowersHitPoints": "object",
            "clan": "PlayerClan",
            "cards": "PlayerItemLevelList",
            "trophyChange": "integer",
            "elixirLeaked": "number",
        },
        "Chest": {"index": "integer", "name": "string"},
        "PlayerLeagueStatistics": {
            "currentSeason": "LeagueSeasonResult",
            "previousSeason": "LeagueSeasonResult",
            "bestSeason": "LeagueSeasonResult",
        },
        "LeagueSeasonResult": {
            "id": "string",
            "trophies": "integer",
            "bestTrophies": "integer",
            "rank": "integer",
        },
        "PathOfLegendSeasonResult": {
            "leagueNumber": "integer",
            "trophies": "integer",
            "rank": "integer",
        },
        "PlayerAchievementProgress": {
            "name": "string",
            "stars": "integer",
            "value": "integer",
            "target": "integer",
            "info": "string",
            "completionInfo": "string",
        },
        "PlayerAchievementBadge": {
            "name": "string",
            "level": "integer",
            "maxLevel": "integer",
            "progress": "integer",
            "target": "integer",
            "iconUrls": "object",
        },
        "GameMode": {"id": "integer", "name": "string"},
        "RiverRaceClan": {
            "tag": "string",
            "name": "string",
            "badgeId": "integer",
            "fame": "integer",
            "repairPoints": "integer",
            "clanScore": "integer",
            "participants": "RiverRaceParticipantList",
        },
        "RiverRaceParticipant": {
            "tag": "string",
            "name": "string",
            "fame": "integer",
            "repairPoints": "integer",
            "decksUsed": "integer",
            "decksUsedToday": "integer",
        },
        "RiverRaceLogEntry": {
            "seasonId": "integer",
            "sectionIndex": "integer",
            "createdDate": "string",
            "standings": "RiverRaceStandingList",
        },
        "RiverRaceStanding": {
            "rank": "integer",
            "trophyChange": "integer",
            "clan": "RiverRaceClan",
        },
        "ClanWarLogEntry": {
            "createdDate": "string",
            "standings": "ClanWarStandingList",
            "participants": "ClanWarParticipantList",
        },
        "ClanWarStanding": {"rank": "integer", "trophyChange": "integer", "clan": "ClanWarClan"},
        "ClanWarClan": {
            "tag": "string",
            "name": "string",
            "badgeId": "integer",
            "clanScore": "integer",
        },
        "ClanWarParticipant": {
            "tag": "string",
            "name": "string",
            "wins": "integer",
            "battlesPlayed": "integer",
        },
        "PeriodLog": {"periodIndex": "integer", "items": "PeriodLogEntryList"},
        "PeriodLogEntry": {"clan": "PeriodLogEntryClan", "pointsEarned": "integer"},
        "PeriodLogEntryClan": {"tag": "string", "name": "string"},
        "TournamentHeader": {
            "tag": "string",
            "name": "string",
            "status": "string",
            "capacity": "integer",
            "maxCapacity": "integer",
        },
        "TournamentMember": {
            "tag": "string",
            "name": "string",
            "rank": "integer",
            "score": "integer",
        },
        "ClanRanking": {
            "tag": "string",
            "name": "string",
            "rank": "integer",
            "previousRank": "integer",
            "clanScore": "integer",
            "members": "integer",
            "location": "Location",
        },
        "PlayerRanking": {
            "tag": "string",
            "name": "string",
            "rank": "integer",
            "previousRank": "integer",
            "trophies": "integer",
            "clan": "PlayerRankingClan",
        },
        "PlayerPathOfLegendRanking": {
            "tag": "string",
            "name": "string",
            "rank": "integer",
            "trophies": "integer",
            "clan": "PlayerRankingClan",
        },
        "LadderTournamentRanking": {
            "tag": "string",
            "name": "string",
            "rank": "integer",
            "score": "integer",
            "clan": "PlayerRankingClan",
        },
        "LadderTournament": {
            "id": "integer",
            "title": "string",
            "gameMode": "GameMode",
            "startTime": "string",
            "endTime": "string",
        },
        "Leaderboard": {"id": "integer", "name": "object", "leagues": "object"},
        "LeaderboardEntry": {
            "tag": "string",
            "name": "string",
            "rank": "integer",
            "score": "integer",
        },
        "TrailEvent": {"id": "integer", "title": "object", "description": "object"},
    }
    extra["LeagueSeasonV2"] = {"code": "string", "uniqueId": "integer", "endTime": "string"}
    extra["LeaderboardEntry"]["clan"] = "PlayerClan"
    extra["PlayerPathOfLegendRanking"]["eloRating"] = "integer"
    extra["TrailEvent"]["eventTag"] = "string"
    schemas = extra | ref["schemas"]
    primitives = {
        "integer": "int",
        "number": "float",
        "string": "str",
        "boolean": "bool",
        "object": "Any",
    }

    def element(name):
        return {
            "ClanWarLog": "ClanWarLogEntry",
            "RiverRaceLog": "RiverRaceLogEntry",
            "Items": "Item",
        }.get(name, name.removesuffix("List"))

    for schema in list(schemas.values()):
        for typ in schema.values():
            if typ not in primitives:
                schemas.setdefault(element(typ), {})
    for op in ref["operations"]:
        schemas.setdefault(element(op.get("client_response", op["response"])), {})
    lines = [
        '"""Typed response models; unknown API fields are retained."""',
        "from __future__ import annotations",
        "from datetime import datetime, timezone",
        "from typing import Any, Generic, TypeVar",
        "from pydantic import BaseModel, ConfigDict, Field, field_validator",
        "from pydantic.alias_generators import to_camel",
        "",
        "class APIModel(BaseModel):",
        '    model_config = ConfigDict(extra="allow", populate_by_name=True, alias_generator=to_camel)',
        "",
        "    def to_dict(self) -> dict[str, Any]:",
        '        """Export JSON-compatible data with original API field names."""',
        '        return self.model_dump(mode="json", by_alias=True, exclude_unset=True)',
        "",
    ]
    times = {
        "battleTime",
        "lastSeen",
        "createdTime",
        "startedTime",
        "endedTime",
        "collectionEndTime",
        "warEndTime",
        "createdDate",
        "startTime",
        "endTime",
    }
    for name, fields in sorted(schemas.items()):
        lines += [
            f"class {name}(APIModel):",
            f'    """{name} response; omitted fields remain None."""',
        ]
        datefields = []
        for field, typ in fields.items():
            t = primitives.get(typ, f"list[{element(typ)}]" if typ.endswith("List") else typ)
            if field in times:
                t = "datetime"
                datefields.append(snake(field))
            lines.append(f"    {snake(field)}: {t} | None = Field(default=None, alias={field!r})")
        if datefields:
            lines += [
                "",
                f'    @field_validator({", ".join(repr(x) for x in datefields)}, mode="before")',
                "    @classmethod",
                "    def parse_time(cls, value: Any) -> Any:",
                "        if isinstance(value, str):",
                "            try:",
                '                return datetime.strptime(value, "%Y%m%dT%H%M%S.%fZ").replace(tzinfo=timezone.utc)',
                "            except ValueError:",
                '                return datetime.fromisoformat(value.replace("Z", "+00:00"))',
                "        return value",
            ]
        lines.append("")
    lines += [
        'T = TypeVar("T", bound=APIModel)',
        "class Cursors(APIModel):",
        "    before: str | None = None",
        "    after: str | None = None",
        "",
        "class Paging(APIModel):",
        "    cursors: Cursors = Field(default_factory=Cursors)",
        "",
        "class Page(APIModel, Generic[T]):",
        "    items: list[T] = Field(default_factory=list)",
        "    paging: Paging = Field(default_factory=Paging)",
        "",
        "__all__ = " + repr(["APIModel", "Cursors", "Paging", "Page"] + sorted(schemas)),
    ]
    Path("src/clashroyaleapi/models.py").write_text("\n".join(lines) + "\n")
    lines = [
        '"""All documented REST operations, generated from docs/api-reference.json."""',
        "from collections.abc import AsyncIterator",
        "from . import models",
        "from .transport import Transport",
        "",
        "class Client(Transport):",
        '    """Async client for all 30 documented official Clash Royale API operations."""',
    ]
    for op in ref["operations"]:
        op["python_method"] = names.get(op["operation_id"], op["python_method"])
        params = op["parameters"]
        paths = [p for p in params if p["in"] == "path"]
        queries = [p for p in params if p["in"] == "query"]
        paginated = any(p["name"] == "after" for p in queries)
        response = op.get("client_response", op["response"])
        item = element(response)
        islist = response.endswith("List") or response in ("ClanWarLog", "RiverRaceLog")
        result = (
            f"models.Page[models.{item}]"
            if paginated
            else f"list[models.{item}]"
            if islist
            else f"models.{response}"
        )
        args = ["self"] + [
            f"{snake(p['name'])}: " + ("int" if p["type"] == "integer" else "str") for p in paths
        ]
        if queries:
            args += ["*"] + [
                f"{snake(p['name'])}: "
                + ("int" if p["type"] == "integer" else "str")
                + " | None = None"
                for p in queries
            ]
        method = op["python_method"]
        lines += [
            "",
            f"    async def {method}({', '.join(args)}) -> {result}:",
            f'        """{op["summary"]}. See endpoint reference for parameters and limitations."""',
        ]
        mapping = "{" + ", ".join(f"{p['name']!r}: {snake(p['name'])}" for p in paths) + "}"
        query = "{" + ", ".join(f"{p['name']!r}: {snake(p['name'])}" for p in queries) + "}"
        lines += [f"        data = await self._get({op['path']!r}, {mapping}, {query})"]
        if paginated:
            lines += [f"        return self._page(data, models.{item})"]
        elif islist:
            lines += [f"        return self._list(data, models.{item})"]
        else:
            lines += [f"        return self._model(data, models.{response})"]
        if paginated:
            lines += [
                "",
                f"    async def iter_{method}({', '.join(args)}) -> AsyncIterator[models.{item}]:",
                f'        """Iterate {method} across pages until the server has no next cursor."""',
                f"        async for item in self._iterate({op['path']!r}, {mapping}, {query}, models.{item}):",
                "            yield item",
            ]
    Path("src/clashroyaleapi/client.py").write_text("\n".join(lines) + "\n")
    Path("docs/api-reference.json").write_text(json.dumps(ref, indent=2) + "\n")


if __name__ == "__main__":
    main()
