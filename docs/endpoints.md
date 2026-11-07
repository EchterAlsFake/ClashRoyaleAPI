# Endpoint reference

All 30 operations use GET. Query arguments are keyword-only.

## get_clan_war_log

`GET /clans/{clanTag}/warlog`

```python
await client.get_clan_war_log(self, clan_tag: str, *, limit: int | None = None, after: str | None = None, before: str | None = None) -> clashroyaleapi.models.Page[ClanWarLogEntry]
```

Retrieve clan's clan war log

Async iterator: `client.iter_get_clan_war_log(...)`.

## search_clans

`GET /clans`

```python
await client.search_clans(self, *, name: str | None = None, location_id: int | None = None, min_members: int | None = None, max_members: int | None = None, min_score: int | None = None, limit: int | None = None, after: str | None = None, before: str | None = None) -> clashroyaleapi.models.Page[Clan]
```

Search all clans by name and/or filtering the results using various criteria. At least one filtering criteria must be defined and if name is used as part of search, it is required to be at least three characters long It is not possible to specify ordering for results so clients should not rely on any specific ordering as that may change in the future releases of the API.

Async iterator: `client.iter_search_clans(...)`.

## get_clan_river_race_log

`GET /clans/{clanTag}/riverracelog`

```python
await client.get_clan_river_race_log(self, clan_tag: str, *, limit: int | None = None, after: str | None = None, before: str | None = None) -> clashroyaleapi.models.Page[RiverRaceLogEntry]
```

Retrieve clan's river race log

Async iterator: `client.iter_get_clan_river_race_log(...)`.

## get_current_war

`GET /clans/{clanTag}/currentwar`

```python
await client.get_current_war(self, clan_tag: str) -> clashroyaleapi.models.CurrentClanWar
```

Retrieve information about clan's current clan war

## get_clan

`GET /clans/{clanTag}`

```python
await client.get_clan(self, clan_tag: str) -> clashroyaleapi.models.Clan
```

Get information about a single clan by clan tag. Clan tags can be found using clan search operation. Note that clan tags start with hash character '#' and that needs to be URL-encoded properly to work in URL, so for example clan tag '#2ABC' would become '%232ABC' in the URL.

## get_clan_members

`GET /clans/{clanTag}/members`

```python
await client.get_clan_members(self, clan_tag: str, *, limit: int | None = None, after: str | None = None, before: str | None = None) -> clashroyaleapi.models.Page[ClanMember]
```

List clan members.

Async iterator: `client.iter_get_clan_members(...)`.

## get_current_river_race

`GET /clans/{clanTag}/currentriverrace`

```python
await client.get_current_river_race(self, clan_tag: str) -> clashroyaleapi.models.CurrentRiverRace
```

Retrieve information about clan's current river race

## get_player

`GET /players/{playerTag}`

```python
await client.get_player(self, player_tag: str) -> clashroyaleapi.models.Player
```

Get information about a single player by player tag. Player tags can be found either in game or by from clan member lists. Note that player tags start with hash character '#' and that needs to be URL-encoded properly to work in URL, so for example player tag '#2ABC' would become '%232ABC' in the URL.

## get_player_upcoming_chests

`GET /players/{playerTag}/upcomingchests`

```python
await client.get_player_upcoming_chests(self, player_tag: str) -> clashroyaleapi.models.UpcomingChests
```

Get list of reward chests that the player will receive next in the game.

## get_player_battle_log

`GET /players/{playerTag}/battlelog`

```python
await client.get_player_battle_log(self, player_tag: str) -> list[clashroyaleapi.models.Battle]
```

Get list of recent battles for a player

## get_cards

`GET /cards`

```python
await client.get_cards(self, *, limit: int | None = None, after: str | None = None, before: str | None = None) -> clashroyaleapi.models.Page[Item]
```

Get list of available cards

Async iterator: `client.iter_get_cards(...)`.

## search_tournaments

`GET /tournaments`

```python
await client.search_tournaments(self, *, name: str | None = None, limit: int | None = None, after: str | None = None, before: str | None = None) -> clashroyaleapi.models.Page[TournamentHeader]
```

Search all tournaments by name. It is not possible to specify ordering for results so clients should not rely on any specific ordering as that may change in the future releases of the API.

Async iterator: `client.iter_search_tournaments(...)`.

## get_tournament

`GET /tournaments/{tournamentTag}`

```python
await client.get_tournament(self, tournament_tag: str) -> clashroyaleapi.models.Tournament
```

Get information about a single tournament by a tournament tag.

## get_clan_ranking

`GET /locations/{locationId}/rankings/clans`

```python
await client.get_clan_ranking(self, location_id: str, *, limit: int | None = None, after: str | None = None, before: str | None = None) -> clashroyaleapi.models.Page[ClanRanking]
```

Get clan rankings for a specific location

Async iterator: `client.iter_get_clan_ranking(...)`.

## get_player_ranking

`GET /locations/{locationId}/rankings/players`

```python
await client.get_player_ranking(self, location_id: str, *, limit: int | None = None, after: str | None = None, before: str | None = None) -> clashroyaleapi.models.Page[PlayerRanking]
```

Deprecated: this endpoint always returns an empty list and will be removed in a future version. Trophy road player rankings no longer exist; use the Path of Legend ranking endpoints instead.

Async iterator: `client.iter_get_player_ranking(...)`.

## get_clan_wars_ranking

`GET /locations/{locationId}/rankings/clanwars`

```python
await client.get_clan_wars_ranking(self, location_id: str, *, limit: int | None = None, after: str | None = None, before: str | None = None) -> clashroyaleapi.models.Page[ClanRanking]
```

Get clan war rankings for a specific location

Async iterator: `client.iter_get_clan_wars_ranking(...)`.

## get_top_player_path_of_legend_season_rankings

`GET /locations/global/pathoflegend/{seasonId}/rankings/players`

```python
await client.get_top_player_path_of_legend_season_rankings(self, season_id: str, *, limit: int | None = None, after: str | None = None, before: str | None = None) -> clashroyaleapi.models.Page[PlayerPathOfLegendRanking]
```

Get top Path of Legend players for given season.

Async iterator: `client.iter_get_top_player_path_of_legend_season_rankings(...)`.

## get_season

`GET /locations/global/seasons/{seasonId}`

```python
await client.get_season(self, season_id: str) -> clashroyaleapi.models.LeagueSeason
```

Get top player league season.

## get_top_player_league_season_rankings

`GET /locations/global/seasons/{seasonId}/rankings/players`

```python
await client.get_top_player_league_season_rankings(self, season_id: str, *, limit: int | None = None, after: str | None = None, before: str | None = None) -> clashroyaleapi.models.Page[PlayerRanking]
```

Get top player rankings for a season.

Async iterator: `client.iter_get_top_player_league_season_rankings(...)`.

## get_seasons

`GET /locations/global/seasons`

```python
await client.get_seasons(self) -> list[clashroyaleapi.models.LeagueSeason]
```

Lists top player league seasons.

## get_locations

`GET /locations`

```python
await client.get_locations(self, *, limit: int | None = None, after: str | None = None, before: str | None = None) -> clashroyaleapi.models.Page[Location]
```

List locations

Async iterator: `client.iter_get_locations(...)`.

## get_seasons_v2

`GET /locations/global/seasonsV2`

```python
await client.get_seasons_v2(self) -> list[clashroyaleapi.models.LeagueSeason]
```

Lists league seasons with unique season IDs and season end times.

## get_location

`GET /locations/{locationId}`

```python
await client.get_location(self, location_id: str) -> clashroyaleapi.models.Location
```

Get information about specific location

## get_global_tournament_ranking

`GET /locations/global/rankings/tournaments/{tournamentTag}`

```python
await client.get_global_tournament_ranking(self, tournament_tag: str, *, limit: int | None = None, after: str | None = None, before: str | None = None) -> clashroyaleapi.models.Page[LadderTournamentRanking]
```

Get global tournament rankings

Async iterator: `client.iter_get_global_tournament_ranking(...)`.

## get_player_path_of_legend_ranking

`GET /locations/{locationId}/pathoflegend/players`

```python
await client.get_player_path_of_legend_ranking(self, location_id: str, *, limit: int | None = None, after: str | None = None, before: str | None = None) -> clashroyaleapi.models.Page[PlayerPathOfLegendRanking]
```

Get player rankings in Path of Legend for a specific location

Async iterator: `client.iter_get_player_path_of_legend_ranking(...)`.

## get_events

`GET /events`

```python
await client.get_events(self) -> list[clashroyaleapi.models.TrailEvent]
```

Get current events. Returns a list of ongoing events with its Title and Description localized.

## get_leaderboard

`GET /leaderboard/{leaderboardId}`

```python
await client.get_leaderboard(self, leaderboard_id: int, *, limit: int | None = None, after: str | None = None, before: str | None = None) -> clashroyaleapi.models.Page[Leaderboard]
```

Get players on a specific leaderboard

Async iterator: `client.iter_get_leaderboard(...)`.

## get_leaderboards

`GET /leaderboards`

```python
await client.get_leaderboards(self) -> list[clashroyaleapi.models.Leaderboard]
```

List leaderboards for different trophy roads. A leaderboard with a board per competitive League lists its Leagues in leagues.

## get_leaderboard_league

`GET /leaderboard/{leaderboardId}/leagues/{leagueId}`

```python
await client.get_leaderboard_league(self, leaderboard_id: int, league_id: int, *, limit: int | None = None, after: str | None = None, before: str | None = None) -> clashroyaleapi.models.Page[LeaderboardEntry]
```

Get players on the board of one competitive League of a leaderboard

Async iterator: `client.iter_get_leaderboard_league(...)`.

## get_global_tournaments

`GET /globaltournaments`

```python
await client.get_global_tournaments(self) -> list[clashroyaleapi.models.LadderTournament]
```

Get list of global tournaments
