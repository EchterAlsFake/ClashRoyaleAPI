"""All documented REST operations, generated from docs/api-reference.json."""

from collections.abc import AsyncIterator

from . import models
from .transport import Transport


class Client(Transport):
    """Async client for all 30 documented official Clash Royale API operations."""

    async def get_clan_war_log(
        self,
        clan_tag: str,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> models.Page[models.ClanWarLogEntry]:
        """Retrieve clan's clan war log. See endpoint reference for parameters and limitations."""
        data = await self._get(
            "/clans/{clanTag}/warlog",
            {"clanTag": clan_tag},
            {"limit": limit, "after": after, "before": before},
        )
        return self._page(data, models.ClanWarLogEntry)

    async def iter_get_clan_war_log(
        self,
        clan_tag: str,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> AsyncIterator[models.ClanWarLogEntry]:
        """Iterate get_clan_war_log across pages until the server has no next cursor."""
        async for item in self._iterate(
            "/clans/{clanTag}/warlog",
            {"clanTag": clan_tag},
            {"limit": limit, "after": after, "before": before},
            models.ClanWarLogEntry,
        ):
            yield item

    async def search_clans(
        self,
        *,
        name: str | None = None,
        location_id: int | None = None,
        min_members: int | None = None,
        max_members: int | None = None,
        min_score: int | None = None,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> models.Page[models.Clan]:
        """Search clans. See endpoint reference for parameters and limitations."""
        data = await self._get(
            "/clans",
            {},
            {
                "name": name,
                "locationId": location_id,
                "minMembers": min_members,
                "maxMembers": max_members,
                "minScore": min_score,
                "limit": limit,
                "after": after,
                "before": before,
            },
        )
        return self._page(data, models.Clan)

    async def iter_search_clans(
        self,
        *,
        name: str | None = None,
        location_id: int | None = None,
        min_members: int | None = None,
        max_members: int | None = None,
        min_score: int | None = None,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> AsyncIterator[models.Clan]:
        """Iterate search_clans across pages until the server has no next cursor."""
        async for item in self._iterate(
            "/clans",
            {},
            {
                "name": name,
                "locationId": location_id,
                "minMembers": min_members,
                "maxMembers": max_members,
                "minScore": min_score,
                "limit": limit,
                "after": after,
                "before": before,
            },
            models.Clan,
        ):
            yield item

    async def get_clan_river_race_log(
        self,
        clan_tag: str,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> models.Page[models.RiverRaceLogEntry]:
        """Retrieve clan's river race log. See endpoint reference for parameters and limitations."""
        data = await self._get(
            "/clans/{clanTag}/riverracelog",
            {"clanTag": clan_tag},
            {"limit": limit, "after": after, "before": before},
        )
        return self._page(data, models.RiverRaceLogEntry)

    async def iter_get_clan_river_race_log(
        self,
        clan_tag: str,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> AsyncIterator[models.RiverRaceLogEntry]:
        """Iterate get_clan_river_race_log across pages until the server has no next cursor."""
        async for item in self._iterate(
            "/clans/{clanTag}/riverracelog",
            {"clanTag": clan_tag},
            {"limit": limit, "after": after, "before": before},
            models.RiverRaceLogEntry,
        ):
            yield item

    async def get_current_war(self, clan_tag: str) -> models.CurrentClanWar:
        """Retrieve information about clan's current clan war. See endpoint reference for parameters and limitations."""
        data = await self._get("/clans/{clanTag}/currentwar", {"clanTag": clan_tag}, {})
        return self._model(data, models.CurrentClanWar)

    async def get_clan(self, clan_tag: str) -> models.Clan:
        """Get clan information. See endpoint reference for parameters and limitations."""
        data = await self._get("/clans/{clanTag}", {"clanTag": clan_tag}, {})
        return self._model(data, models.Clan)

    async def get_clan_members(
        self,
        clan_tag: str,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> models.Page[models.ClanMember]:
        """List clan members. See endpoint reference for parameters and limitations."""
        data = await self._get(
            "/clans/{clanTag}/members",
            {"clanTag": clan_tag},
            {"limit": limit, "after": after, "before": before},
        )
        return self._page(data, models.ClanMember)

    async def iter_get_clan_members(
        self,
        clan_tag: str,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> AsyncIterator[models.ClanMember]:
        """Iterate get_clan_members across pages until the server has no next cursor."""
        async for item in self._iterate(
            "/clans/{clanTag}/members",
            {"clanTag": clan_tag},
            {"limit": limit, "after": after, "before": before},
            models.ClanMember,
        ):
            yield item

    async def get_current_river_race(self, clan_tag: str) -> models.CurrentRiverRace:
        """Retrieve information about clan's current river race. See endpoint reference for parameters and limitations."""
        data = await self._get("/clans/{clanTag}/currentriverrace", {"clanTag": clan_tag}, {})
        return self._model(data, models.CurrentRiverRace)

    async def get_player(self, player_tag: str) -> models.Player:
        """Get player information. See endpoint reference for parameters and limitations."""
        data = await self._get("/players/{playerTag}", {"playerTag": player_tag}, {})
        return self._model(data, models.Player)

    async def get_player_upcoming_chests(self, player_tag: str) -> models.UpcomingChests:
        """Get information about player's upcoming chests. See endpoint reference for parameters and limitations."""
        data = await self._get("/players/{playerTag}/upcomingchests", {"playerTag": player_tag}, {})
        return self._model(data, models.UpcomingChests)

    async def get_player_battle_log(self, player_tag: str) -> list[models.Battle]:
        """Get list of recent battles for a player. See endpoint reference for parameters and limitations."""
        data = await self._get("/players/{playerTag}/battlelog", {"playerTag": player_tag}, {})
        return self._list(data, models.Battle)

    async def get_cards(
        self, *, limit: int | None = None, after: str | None = None, before: str | None = None
    ) -> models.Page[models.Item]:
        """Get list of available cards. See endpoint reference for parameters and limitations."""
        data = await self._get("/cards", {}, {"limit": limit, "after": after, "before": before})
        return self._page(data, models.Item)

    async def iter_get_cards(
        self, *, limit: int | None = None, after: str | None = None, before: str | None = None
    ) -> AsyncIterator[models.Item]:
        """Iterate get_cards across pages until the server has no next cursor."""
        async for item in self._iterate(
            "/cards", {}, {"limit": limit, "after": after, "before": before}, models.Item
        ):
            yield item

    async def search_tournaments(
        self,
        *,
        name: str | None = None,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> models.Page[models.TournamentHeader]:
        """Search tournaments. See endpoint reference for parameters and limitations."""
        data = await self._get(
            "/tournaments", {}, {"name": name, "limit": limit, "after": after, "before": before}
        )
        return self._page(data, models.TournamentHeader)

    async def iter_search_tournaments(
        self,
        *,
        name: str | None = None,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> AsyncIterator[models.TournamentHeader]:
        """Iterate search_tournaments across pages until the server has no next cursor."""
        async for item in self._iterate(
            "/tournaments",
            {},
            {"name": name, "limit": limit, "after": after, "before": before},
            models.TournamentHeader,
        ):
            yield item

    async def get_tournament(self, tournament_tag: str) -> models.Tournament:
        """Get tournament information. See endpoint reference for parameters and limitations."""
        data = await self._get(
            "/tournaments/{tournamentTag}", {"tournamentTag": tournament_tag}, {}
        )
        return self._model(data, models.Tournament)

    async def get_clan_ranking(
        self,
        location_id: str,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> models.Page[models.ClanRanking]:
        """Get clan rankings for a specific location. See endpoint reference for parameters and limitations."""
        data = await self._get(
            "/locations/{locationId}/rankings/clans",
            {"locationId": location_id},
            {"limit": limit, "after": after, "before": before},
        )
        return self._page(data, models.ClanRanking)

    async def iter_get_clan_ranking(
        self,
        location_id: str,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> AsyncIterator[models.ClanRanking]:
        """Iterate get_clan_ranking across pages until the server has no next cursor."""
        async for item in self._iterate(
            "/locations/{locationId}/rankings/clans",
            {"locationId": location_id},
            {"limit": limit, "after": after, "before": before},
            models.ClanRanking,
        ):
            yield item

    async def get_player_ranking(
        self,
        location_id: str,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> models.Page[models.PlayerRanking]:
        """Get player rankings for a specific location. See endpoint reference for parameters and limitations."""
        data = await self._get(
            "/locations/{locationId}/rankings/players",
            {"locationId": location_id},
            {"limit": limit, "after": after, "before": before},
        )
        return self._page(data, models.PlayerRanking)

    async def iter_get_player_ranking(
        self,
        location_id: str,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> AsyncIterator[models.PlayerRanking]:
        """Iterate get_player_ranking across pages until the server has no next cursor."""
        async for item in self._iterate(
            "/locations/{locationId}/rankings/players",
            {"locationId": location_id},
            {"limit": limit, "after": after, "before": before},
            models.PlayerRanking,
        ):
            yield item

    async def get_clan_wars_ranking(
        self,
        location_id: str,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> models.Page[models.ClanRanking]:
        """Get clan war rankings for a specific location. See endpoint reference for parameters and limitations."""
        data = await self._get(
            "/locations/{locationId}/rankings/clanwars",
            {"locationId": location_id},
            {"limit": limit, "after": after, "before": before},
        )
        return self._page(data, models.ClanRanking)

    async def iter_get_clan_wars_ranking(
        self,
        location_id: str,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> AsyncIterator[models.ClanRanking]:
        """Iterate get_clan_wars_ranking across pages until the server has no next cursor."""
        async for item in self._iterate(
            "/locations/{locationId}/rankings/clanwars",
            {"locationId": location_id},
            {"limit": limit, "after": after, "before": before},
            models.ClanRanking,
        ):
            yield item

    async def get_top_player_path_of_legend_season_rankings(
        self,
        season_id: str,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> models.Page[models.PlayerPathOfLegendRanking]:
        """Get top Path of Legend players for given season.. See endpoint reference for parameters and limitations."""
        data = await self._get(
            "/locations/global/pathoflegend/{seasonId}/rankings/players",
            {"seasonId": season_id},
            {"limit": limit, "after": after, "before": before},
        )
        return self._page(data, models.PlayerPathOfLegendRanking)

    async def iter_get_top_player_path_of_legend_season_rankings(
        self,
        season_id: str,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> AsyncIterator[models.PlayerPathOfLegendRanking]:
        """Iterate get_top_player_path_of_legend_season_rankings across pages until the server has no next cursor."""
        async for item in self._iterate(
            "/locations/global/pathoflegend/{seasonId}/rankings/players",
            {"seasonId": season_id},
            {"limit": limit, "after": after, "before": before},
            models.PlayerPathOfLegendRanking,
        ):
            yield item

    async def get_season(self, season_id: str) -> models.LeagueSeason:
        """Get top player league season.. See endpoint reference for parameters and limitations."""
        data = await self._get("/locations/global/seasons/{seasonId}", {"seasonId": season_id}, {})
        return self._model(data, models.LeagueSeason)

    async def get_top_player_league_season_rankings(
        self,
        season_id: str,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> models.Page[models.PlayerRanking]:
        """Get top player rankings for a season.. See endpoint reference for parameters and limitations."""
        data = await self._get(
            "/locations/global/seasons/{seasonId}/rankings/players",
            {"seasonId": season_id},
            {"limit": limit, "after": after, "before": before},
        )
        return self._page(data, models.PlayerRanking)

    async def iter_get_top_player_league_season_rankings(
        self,
        season_id: str,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> AsyncIterator[models.PlayerRanking]:
        """Iterate get_top_player_league_season_rankings across pages until the server has no next cursor."""
        async for item in self._iterate(
            "/locations/global/seasons/{seasonId}/rankings/players",
            {"seasonId": season_id},
            {"limit": limit, "after": after, "before": before},
            models.PlayerRanking,
        ):
            yield item

    async def get_seasons(self) -> list[models.LeagueSeason]:
        """Lists top player league seasons.. See endpoint reference for parameters and limitations."""
        data = await self._get("/locations/global/seasons", {}, {})
        return self._list(data, models.LeagueSeason)

    async def get_locations(
        self, *, limit: int | None = None, after: str | None = None, before: str | None = None
    ) -> models.Page[models.Location]:
        """List locations. See endpoint reference for parameters and limitations."""
        data = await self._get("/locations", {}, {"limit": limit, "after": after, "before": before})
        return self._page(data, models.Location)

    async def iter_get_locations(
        self, *, limit: int | None = None, after: str | None = None, before: str | None = None
    ) -> AsyncIterator[models.Location]:
        """Iterate get_locations across pages until the server has no next cursor."""
        async for item in self._iterate(
            "/locations", {}, {"limit": limit, "after": after, "before": before}, models.Location
        ):
            yield item

    async def get_seasons_v2(self) -> list[models.LeagueSeasonV2]:
        """Lists league seasons with more details.. See endpoint reference for parameters and limitations."""
        data = await self._get("/locations/global/seasonsV2", {}, {})
        return self._list(data, models.LeagueSeasonV2)

    async def get_location(self, location_id: str) -> models.Location:
        """Get location information. See endpoint reference for parameters and limitations."""
        data = await self._get("/locations/{locationId}", {"locationId": location_id}, {})
        return self._model(data, models.Location)

    async def get_global_tournament_ranking(
        self,
        tournament_tag: str,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> models.Page[models.LadderTournamentRanking]:
        """Get global tournament rankings. See endpoint reference for parameters and limitations."""
        data = await self._get(
            "/locations/global/rankings/tournaments/{tournamentTag}",
            {"tournamentTag": tournament_tag},
            {"limit": limit, "after": after, "before": before},
        )
        return self._page(data, models.LadderTournamentRanking)

    async def iter_get_global_tournament_ranking(
        self,
        tournament_tag: str,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> AsyncIterator[models.LadderTournamentRanking]:
        """Iterate get_global_tournament_ranking across pages until the server has no next cursor."""
        async for item in self._iterate(
            "/locations/global/rankings/tournaments/{tournamentTag}",
            {"tournamentTag": tournament_tag},
            {"limit": limit, "after": after, "before": before},
            models.LadderTournamentRanking,
        ):
            yield item

    async def get_player_path_of_legend_ranking(
        self,
        location_id: str,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> models.Page[models.PlayerPathOfLegendRanking]:
        """Get player rankings in Path of Legend for a specific location. See endpoint reference for parameters and limitations."""
        data = await self._get(
            "/locations/{locationId}/pathoflegend/players",
            {"locationId": location_id},
            {"limit": limit, "after": after, "before": before},
        )
        return self._page(data, models.PlayerPathOfLegendRanking)

    async def iter_get_player_path_of_legend_ranking(
        self,
        location_id: str,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> AsyncIterator[models.PlayerPathOfLegendRanking]:
        """Iterate get_player_path_of_legend_ranking across pages until the server has no next cursor."""
        async for item in self._iterate(
            "/locations/{locationId}/pathoflegend/players",
            {"locationId": location_id},
            {"limit": limit, "after": after, "before": before},
            models.PlayerPathOfLegendRanking,
        ):
            yield item

    async def get_events(self) -> list[models.TrailEvent]:
        """Get current events.. See endpoint reference for parameters and limitations."""
        data = await self._get("/events", {}, {})
        return self._list(data, models.TrailEvent)

    async def get_leaderboard(
        self,
        leaderboard_id: int,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> models.Page[models.LeaderboardEntry]:
        """Get players on a specific leaderboard. See endpoint reference for parameters and limitations."""
        data = await self._get(
            "/leaderboard/{leaderboardId}",
            {"leaderboardId": leaderboard_id},
            {"limit": limit, "after": after, "before": before},
        )
        return self._page(data, models.LeaderboardEntry)

    async def iter_get_leaderboard(
        self,
        leaderboard_id: int,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> AsyncIterator[models.LeaderboardEntry]:
        """Iterate get_leaderboard across pages until the server has no next cursor."""
        async for item in self._iterate(
            "/leaderboard/{leaderboardId}",
            {"leaderboardId": leaderboard_id},
            {"limit": limit, "after": after, "before": before},
            models.LeaderboardEntry,
        ):
            yield item

    async def get_leaderboards(self) -> list[models.Leaderboard]:
        """List leaderboards. See endpoint reference for parameters and limitations."""
        data = await self._get("/leaderboards", {}, {})
        return self._list(data, models.Leaderboard)

    async def get_leaderboard_league(
        self,
        leaderboard_id: int,
        league_id: int,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> models.Page[models.LeaderboardEntry]:
        """Get players on a League's board of a leaderboard. See endpoint reference for parameters and limitations."""
        data = await self._get(
            "/leaderboard/{leaderboardId}/leagues/{leagueId}",
            {"leaderboardId": leaderboard_id, "leagueId": league_id},
            {"limit": limit, "after": after, "before": before},
        )
        return self._page(data, models.LeaderboardEntry)

    async def iter_get_leaderboard_league(
        self,
        leaderboard_id: int,
        league_id: int,
        *,
        limit: int | None = None,
        after: str | None = None,
        before: str | None = None,
    ) -> AsyncIterator[models.LeaderboardEntry]:
        """Iterate get_leaderboard_league across pages until the server has no next cursor."""
        async for item in self._iterate(
            "/leaderboard/{leaderboardId}/leagues/{leagueId}",
            {"leaderboardId": leaderboard_id, "leagueId": league_id},
            {"limit": limit, "after": after, "before": before},
            models.LeaderboardEntry,
        ):
            yield item

    async def get_global_tournaments(self) -> list[models.LadderTournament]:
        """Get list of global tournaments. See endpoint reference for parameters and limitations."""
        data = await self._get("/globaltournaments", {}, {})
        return self._list(data, models.LadderTournament)
