# Endpoint reference

These signatures describe the API. Usage snippets run inside an async Client context; see [Getting started](getting-started.md).

## get_player

`GET /players/{playerTag}`

```text
get_player(player_tag: str) -> Player
```

Get information about a single player by player tag. Player tags can be found either in game or by from clan member lists. Note that player tags start with hash character '#' and that needs to be URL-encoded properly to work in URL, so for example player tag '#2ABC' would become '%232ABC' in the URL.

```python
result = await client.get_player("#J92CYLP28")
```

## get_player_upcoming_chests

`GET /players/{playerTag}/upcomingchests`

```text
get_player_upcoming_chests(player_tag: str) -> UpcomingChests
```

Get list of reward chests that the player will receive next in the game.

```python
result = await client.get_player_upcoming_chests("#J92CYLP28")
```

## get_player_battle_log

`GET /players/{playerTag}/battlelog`

```text
get_player_battle_log(player_tag: str) -> list[Battle]
```

Get list of recent battles for a player

```python
result = await client.get_player_battle_log("#J92CYLP28")
```

## get_clan_war_log

`GET /clans/{clanTag}/warlog`

```text
get_clan_war_log(
    clan_tag: str,
    *,
    limit: int | None = None,
    after: str | None = None,
    before: str | None = None,
) -> Page[ClanWarLogEntry]
```

Retrieve clan's clan war log

```python
result = await client.get_clan_war_log("#88Q2JCVL", limit=10)
```

## search_clans

`GET /clans`

```text
search_clans(
    *,
    name: str | None = None,
    location_id: int | None = None,
    min_members: int | None = None,
    max_members: int | None = None,
    min_score: int | None = None,
    limit: int | None = None,
    after: str | None = None,
    before: str | None = None,
) -> Page[Clan]
```

Search all clans by name and/or filtering the results using various criteria. At least one filtering criteria must be defined and if name is used as part of search, it is required to be at least three characters long It is not possible to specify ordering for results so clients should not rely on any specific ordering as that may change in the future releases of the API.

```python
result = await client.search_clans(name="royale", limit=10)
```

## get_clan_river_race_log

`GET /clans/{clanTag}/riverracelog`

```text
get_clan_river_race_log(
    clan_tag: str,
    *,
    limit: int | None = None,
    after: str | None = None,
    before: str | None = None,
) -> Page[RiverRaceLogEntry]
```

Retrieve clan's river race log

```python
result = await client.get_clan_river_race_log("#88Q2JCVL", limit=10)
```

## get_current_war

`GET /clans/{clanTag}/currentwar`

```text
get_current_war(clan_tag: str) -> CurrentClanWar
```

Retrieve information about clan's current clan war

```python
result = await client.get_current_war("#88Q2JCVL")
```

## get_clan

`GET /clans/{clanTag}`

```text
get_clan(clan_tag: str) -> Clan
```

Get information about a single clan by clan tag. Clan tags can be found using clan search operation. Note that clan tags start with hash character '#' and that needs to be URL-encoded properly to work in URL, so for example clan tag '#2ABC' would become '%232ABC' in the URL.

```python
result = await client.get_clan("#88Q2JCVL")
```

## get_clan_members

`GET /clans/{clanTag}/members`

```text
get_clan_members(
    clan_tag: str,
    *,
    limit: int | None = None,
    after: str | None = None,
    before: str | None = None,
) -> Page[ClanMember]
```

List clan members.

```python
result = await client.get_clan_members("#88Q2JCVL", limit=10)
```

## get_current_river_race

`GET /clans/{clanTag}/currentriverrace`

```text
get_current_river_race(clan_tag: str) -> CurrentRiverRace
```

Retrieve information about clan's current river race

```python
result = await client.get_current_river_race("#88Q2JCVL")
```

## get_cards

`GET /cards`

```text
get_cards(
    *,
    limit: int | None = None,
    after: str | None = None,
    before: str | None = None,
) -> Page[Item]
```

Get list of available cards

```python
result = await client.get_cards(limit=10)
```

## search_tournaments

`GET /tournaments`

```text
search_tournaments(
    *,
    name: str | None = None,
    limit: int | None = None,
    after: str | None = None,
    before: str | None = None,
) -> Page[TournamentHeader]
```

Search all tournaments by name. It is not possible to specify ordering for results so clients should not rely on any specific ordering as that may change in the future releases of the API.

```python
result = await client.search_tournaments(name="royale", limit=10)
```

## get_tournament

`GET /tournaments/{tournamentTag}`

```text
get_tournament(tournament_tag: str) -> Tournament
```

Get information about a single tournament by a tournament tag.

```python
result = await client.get_tournament("#2GG80C0Q")
```

## get_clan_ranking

`GET /locations/{locationId}/rankings/clans`

```text
get_clan_ranking(
    location_id: str,
    *,
    limit: int | None = None,
    after: str | None = None,
    before: str | None = None,
) -> Page[ClanRanking]
```

Get clan rankings for a specific location

```python
result = await client.get_clan_ranking("global", limit=10)
```

## get_player_ranking

`GET /locations/{locationId}/rankings/players`

```text
get_player_ranking(
    location_id: str,
    *,
    limit: int | None = None,
    after: str | None = None,
    before: str | None = None,
) -> Page[PlayerRanking]
```

Deprecated: this endpoint always returns an empty list and will be removed in a future version. Trophy road player rankings no longer exist; use the Path of Legend ranking endpoints instead.

```python
result = await client.get_player_ranking("global", limit=10)
```

## get_clan_wars_ranking

`GET /locations/{locationId}/rankings/clanwars`

```text
get_clan_wars_ranking(
    location_id: str,
    *,
    limit: int | None = None,
    after: str | None = None,
    before: str | None = None,
) -> Page[ClanRanking]
```

Get clan war rankings for a specific location

```python
result = await client.get_clan_wars_ranking("global", limit=10)
```

## get_top_player_path_of_legend_season_rankings

`GET /locations/global/pathoflegend/{seasonId}/rankings/players`

```text
get_top_player_path_of_legend_season_rankings(
    season_id: str,
    *,
    limit: int | None = None,
    after: str | None = None,
    before: str | None = None,
) -> Page[PlayerPathOfLegendRanking]
```

Get top Path of Legend players for given season.

```python
result = await client.get_top_player_path_of_legend_season_rankings("2026-10", limit=10)
```

## get_season

`GET /locations/global/seasons/{seasonId}`

```text
get_season(season_id: str) -> LeagueSeason
```

Get top player league season.

```python
result = await client.get_season("2026-10")
```

## get_top_player_league_season_rankings

`GET /locations/global/seasons/{seasonId}/rankings/players`

```text
get_top_player_league_season_rankings(
    season_id: str,
    *,
    limit: int | None = None,
    after: str | None = None,
    before: str | None = None,
) -> Page[PlayerRanking]
```

Get top player rankings for a season.

```python
result = await client.get_top_player_league_season_rankings("2022-09", limit=10)
```

## get_seasons

`GET /locations/global/seasons`

```text
get_seasons() -> list[LeagueSeason]
```

Lists top player league seasons.

```python
result = await client.get_seasons()
```

## get_locations

`GET /locations`

```text
get_locations(
    *,
    limit: int | None = None,
    after: str | None = None,
    before: str | None = None,
) -> Page[Location]
```

List locations

```python
result = await client.get_locations(limit=10)
```

## get_seasons_v2

`GET /locations/global/seasonsV2`

```text
get_seasons_v2() -> list[LeagueSeasonV2]
```

Lists league seasons with unique season IDs and season end times.

```python
result = await client.get_seasons_v2()
```

## get_location

`GET /locations/{locationId}`

```text
get_location(location_id: str) -> Location
```

Get information about specific location

```python
result = await client.get_location("57000094")
```

## get_global_tournament_ranking

`GET /locations/global/rankings/tournaments/{tournamentTag}`

```text
get_global_tournament_ranking(
    tournament_tag: str,
    *,
    limit: int | None = None,
    after: str | None = None,
    before: str | None = None,
) -> Page[LadderTournamentRanking]
```

Get global tournament rankings

```python
result = await client.get_global_tournament_ranking("#758209", limit=10)
```

## get_player_path_of_legend_ranking

`GET /locations/{locationId}/pathoflegend/players`

```text
get_player_path_of_legend_ranking(
    location_id: str,
    *,
    limit: int | None = None,
    after: str | None = None,
    before: str | None = None,
) -> Page[PlayerPathOfLegendRanking]
```

Get player rankings in Path of Legend for a specific location

```python
result = await client.get_player_path_of_legend_ranking("global", limit=10)
```

## get_events

`GET /events`

```text
get_events() -> list[TrailEvent]
```

Get current events. Returns a list of ongoing events with its Title and Description localized.

```python
result = await client.get_events()
```

## get_leaderboard

`GET /leaderboard/{leaderboardId}`

```text
get_leaderboard(
    leaderboard_id: int,
    *,
    limit: int | None = None,
    after: str | None = None,
    before: str | None = None,
) -> Page[LeaderboardEntry]
```

Get players on a specific leaderboard

```python
result = await client.get_leaderboard(170000019, limit=10)
```

## get_leaderboards

`GET /leaderboards`

```text
get_leaderboards() -> list[Leaderboard]
```

List leaderboards for different trophy roads. A leaderboard with a board per competitive League lists its Leagues in leagues.

```python
result = await client.get_leaderboards()
```

## get_leaderboard_league

`GET /leaderboard/{leaderboardId}/leagues/{leagueId}`

```text
get_leaderboard_league(
    leaderboard_id: int,
    league_id: int,
    *,
    limit: int | None = None,
    after: str | None = None,
    before: str | None = None,
) -> Page[LeaderboardEntry]
```

Get players on the board of one competitive League of a leaderboard

```python
result = await client.get_leaderboard_league(170000019, 1, limit=10)
```

## get_global_tournaments

`GET /globaltournaments`

```text
get_global_tournaments() -> list[LadderTournament]
```

Get list of global tournaments

```python
result = await client.get_global_tournaments()
```
