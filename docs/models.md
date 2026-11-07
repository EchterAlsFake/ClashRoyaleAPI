# Response models

All fields are optional unless stated otherwise. Unknown fields are retained.

## APIModel

```text

```

## Cursors

```text
before: str | None
after: str | None
```

## Paging

```text
cursors: <class 'clashroyaleapi.models.Cursors'>
```

## Page

```text
items: list[~T]
paging: <class 'clashroyaleapi.models.Paging'>
```

## Arena

```text
id: int | None
name: str | None
```

## Battle

```text
type: str | None
battle_time: datetime.datetime | None
is_ladder_tournament: bool | None
is_hosted_match: bool | None
deck_selection: str | None
league_number: int | None
game_mode: ForwardRef('GameMode | None')
arena: clashroyaleapi.models.Arena | None
team: ForwardRef('list[PlayerBattleData] | None')
opponent: ForwardRef('list[PlayerBattleData] | None')
```

## Chest

```text
index: int | None
name: str | None
```

## Clan

```text
badge_id: int | None
member_list: ForwardRef('list[ClanMember] | None')
clan_chest_status: str | None
clan_chest_level: int | None
clan_chest_max_level: int | None
clan_score: int | None
clan_war_trophies: int | None
required_trophies: int | None
donations_per_week: int | None
members: int | None
name: str | None
location: ForwardRef('Location | None')
type: str | None
tag: str | None
description: str | None
clan_chest_points: int | None
badge_urls: typing.Any | None
```

## ClanMember

```text
tag: str | None
name: str | None
role: str | None
last_seen: datetime.datetime | None
exp_level: int | None
trophies: int | None
clan_rank: int | None
previous_clan_rank: int | None
donations: int | None
donations_received: int | None
arena: clashroyaleapi.models.Arena | None
```

## ClanRanking

```text
tag: str | None
name: str | None
rank: int | None
previous_rank: int | None
clan_score: int | None
members: int | None
location: ForwardRef('Location | None')
```

## ClanWarClan

```text
tag: str | None
name: str | None
badge_id: int | None
clan_score: int | None
```

## ClanWarLogEntry

```text
created_date: datetime.datetime | None
standings: ForwardRef('list[ClanWarStanding] | None')
participants: ForwardRef('list[ClanWarParticipant] | None')
```

## ClanWarParticipant

```text
tag: str | None
name: str | None
wins: int | None
battles_played: int | None
```

## ClanWarStanding

```text
rank: int | None
trophy_change: int | None
clan: clashroyaleapi.models.ClanWarClan | None
```

## CurrentClanWar

```text
state: str | None
clan: clashroyaleapi.models.ClanWarClan | None
participants: list[clashroyaleapi.models.ClanWarParticipant] | None
clans: list[clashroyaleapi.models.ClanWarClan] | None
collection_end_time: datetime.datetime | None
war_end_time: datetime.datetime | None
```

## CurrentRiverRace

```text
state: str | None
clan: ForwardRef('RiverRaceClan | None')
clans: ForwardRef('list[RiverRaceClan] | None')
collection_end_time: datetime.datetime | None
war_end_time: datetime.datetime | None
section_index: int | None
period_index: int | None
period_type: str | None
period_logs: ForwardRef('list[PeriodLog] | None')
```

## GameMode

```text
id: int | None
name: str | None
```

## Item

```text
id: int | None
name: str | None
max_level: int | None
max_evolution_level: int | None
rarity: str | None
elixir_cost: int | None
icon_urls: typing.Any | None
```

## Items

```text
items: list[clashroyaleapi.models.Item] | None
support_items: list[clashroyaleapi.models.Item] | None
```

## LadderTournament

```text
id: int | None
title: str | None
game_mode: clashroyaleapi.models.GameMode | None
start_time: datetime.datetime | None
end_time: datetime.datetime | None
```

## LadderTournamentRanking

```text
tag: str | None
name: str | None
rank: int | None
score: int | None
clan: ForwardRef('PlayerRankingClan | None')
```

## Leaderboard

```text
id: int | None
name: typing.Any | None
leagues: typing.Any | None
```

## LeaderboardEntry

```text
tag: str | None
name: str | None
rank: int | None
score: int | None
clan: ForwardRef('PlayerClan | None')
```

## LeagueSeason

```text
id: str | None
```

## LeagueSeasonResult

```text
id: str | None
trophies: int | None
best_trophies: int | None
rank: int | None
```

## LeagueSeasonV2

```text
code: str | None
unique_id: int | None
end_time: datetime.datetime | None
```

## Location

```text
localized_name: str | None
id: int | None
name: str | None
is_country: bool | None
country_code: str | None
```

## PathOfLegendSeasonResult

```text
league_number: int | None
trophies: int | None
rank: int | None
```

## PeriodLog

```text
period_index: int | None
items: ForwardRef('list[PeriodLogEntry] | None')
```

## PeriodLogEntry

```text
clan: ForwardRef('PeriodLogEntryClan | None')
points_earned: int | None
```

## PeriodLogEntryClan

```text
tag: str | None
name: str | None
```

## Player

```text
clan: ForwardRef('PlayerClan | None')
legacy_trophy_road_high_score: int | None
current_deck: ForwardRef('list[PlayerItemLevel] | None')
current_deck_support_cards: ForwardRef('list[PlayerItemLevel] | None')
arena: clashroyaleapi.models.Arena | None
role: str | None
wins: int | None
losses: int | None
total_donations: int | None
league_statistics: ForwardRef('PlayerLeagueStatistics | None')
cards: ForwardRef('list[PlayerItemLevel] | None')
support_cards: ForwardRef('list[PlayerItemLevel] | None')
current_favourite_card: clashroyaleapi.models.Item | None
badges: ForwardRef('list[PlayerAchievementBadge] | None')
tag: str | None
name: str | None
collection_level: int | None
king_tower_level: int | None
exp_level: int | None
trophies: int | None
best_trophies: int | None
donations: int | None
donations_received: int | None
achievements: ForwardRef('list[PlayerAchievementProgress] | None')
battle_count: int | None
three_crown_wins: int | None
challenge_cards_won: int | None
challenge_max_wins: int | None
tournament_cards_won: int | None
tournament_battle_count: int | None
current_win_lose_streak: int | None
war_day_wins: int | None
clan_cards_collected: int | None
star_points: int | None
exp_points: int | None
total_exp_points: int | None
current_path_of_legend_season_result: clashroyaleapi.models.PathOfLegendSeasonResult | None
last_path_of_legend_season_result: clashroyaleapi.models.PathOfLegendSeasonResult | None
best_path_of_legend_season_result: clashroyaleapi.models.PathOfLegendSeasonResult | None
progress: typing.Any | None
```

## PlayerAchievementBadge

```text
name: str | None
level: int | None
max_level: int | None
progress: int | None
target: int | None
icon_urls: typing.Any | None
```

## PlayerAchievementProgress

```text
name: str | None
stars: int | None
value: int | None
target: int | None
info: str | None
completion_info: str | None
```

## PlayerBattleData

```text
tag: str | None
name: str | None
crowns: int | None
king_tower_hit_points: int | None
princess_towers_hit_points: typing.Any | None
clan: ForwardRef('PlayerClan | None')
cards: ForwardRef('list[PlayerItemLevel] | None')
trophy_change: int | None
elixir_leaked: float | None
```

## PlayerClan

```text
tag: str | None
name: str | None
badge_id: int | None
```

## PlayerItemLevel

```text
id: int | None
name: str | None
level: int | None
max_level: int | None
count: int | None
star_level: int | None
evolution_level: int | None
rarity: str | None
elixir_cost: int | None
icon_urls: typing.Any | None
```

## PlayerLeagueStatistics

```text
current_season: clashroyaleapi.models.LeagueSeasonResult | None
previous_season: clashroyaleapi.models.LeagueSeasonResult | None
best_season: clashroyaleapi.models.LeagueSeasonResult | None
```

## PlayerPathOfLegendRanking

```text
tag: str | None
name: str | None
rank: int | None
trophies: int | None
clan: ForwardRef('PlayerRankingClan | None')
elo_rating: int | None
```

## PlayerRanking

```text
tag: str | None
name: str | None
rank: int | None
previous_rank: int | None
trophies: int | None
clan: ForwardRef('PlayerRankingClan | None')
```

## PlayerRankingClan

```text
tag: str | None
name: str | None
badge_id: int | None
```

## RiverRaceClan

```text
tag: str | None
name: str | None
badge_id: int | None
fame: int | None
repair_points: int | None
clan_score: int | None
participants: ForwardRef('list[RiverRaceParticipant] | None')
```

## RiverRaceLogEntry

```text
season_id: int | None
section_index: int | None
created_date: datetime.datetime | None
standings: ForwardRef('list[RiverRaceStanding] | None')
```

## RiverRaceParticipant

```text
tag: str | None
name: str | None
fame: int | None
repair_points: int | None
decks_used: int | None
decks_used_today: int | None
```

## RiverRaceStanding

```text
rank: int | None
trophy_change: int | None
clan: clashroyaleapi.models.RiverRaceClan | None
```

## Tournament

```text
game_mode: clashroyaleapi.models.GameMode | None
status: str | None
preparation_duration: int | None
members_list: ForwardRef('list[TournamentMember] | None')
created_time: datetime.datetime | None
started_time: datetime.datetime | None
ended_time: datetime.datetime | None
first_place_card_prize: int | None
type: str | None
duration: int | None
tag: str | None
creator_tag: str | None
name: str | None
description: str | None
capacity: int | None
max_capacity: int | None
level_cap: int | None
```

## TournamentHeader

```text
tag: str | None
name: str | None
status: str | None
capacity: int | None
max_capacity: int | None
```

## TournamentMember

```text
tag: str | None
name: str | None
rank: int | None
score: int | None
```

## TrailEvent

```text
id: int | None
title: typing.Any | None
description: typing.Any | None
event_tag: str | None
```

## UpcomingChests

```text
items: list[clashroyaleapi.models.Chest] | None
```
