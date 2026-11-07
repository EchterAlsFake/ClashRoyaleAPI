# Response models

Fields are optional unless stated otherwise. Unknown fields are retained. See [working with models](getting-started.md#response-models).

## APIModel

| Attribute | Type | API field |
| --- | --- | --- |

## Cursors

| Attribute | Type | API field |
| --- | --- | --- |
| `before` | `str  /  None` | `before` |
| `after` | `str  /  None` | `after` |

## Paging

| Attribute | Type | API field |
| --- | --- | --- |
| `cursors` | `Cursors` | `cursors` |

## Page

| Attribute | Type | API field |
| --- | --- | --- |
| `items` | `list[T]` | `items` |
| `paging` | `Paging` | `paging` |

## Arena

| Attribute | Type | API field |
| --- | --- | --- |
| `id` | `int  /  None` | `id` |
| `name` | `str  /  None` | `name` |

## Battle

| Attribute | Type | API field |
| --- | --- | --- |
| `type` | `str  /  None` | `type` |
| `battle_time` | `datetime  /  None` | `battleTime` |
| `is_ladder_tournament` | `bool  /  None` | `isLadderTournament` |
| `is_hosted_match` | `bool  /  None` | `isHostedMatch` |
| `deck_selection` | `str  /  None` | `deckSelection` |
| `league_number` | `int  /  None` | `leagueNumber` |
| `game_mode` | `ForwardRef('GameMode  /  None')` | `gameMode` |
| `arena` | `Arena  /  None` | `arena` |
| `team` | `ForwardRef('list[PlayerBattleData]  /  None')` | `team` |
| `opponent` | `ForwardRef('list[PlayerBattleData]  /  None')` | `opponent` |

## Chest

| Attribute | Type | API field |
| --- | --- | --- |
| `index` | `int  /  None` | `index` |
| `name` | `str  /  None` | `name` |

## Clan

| Attribute | Type | API field |
| --- | --- | --- |
| `badge_id` | `int  /  None` | `badgeId` |
| `member_list` | `ForwardRef('list[ClanMember]  /  None')` | `memberList` |
| `clan_chest_status` | `str  /  None` | `clanChestStatus` |
| `clan_chest_level` | `int  /  None` | `clanChestLevel` |
| `clan_chest_max_level` | `int  /  None` | `clanChestMaxLevel` |
| `clan_score` | `int  /  None` | `clanScore` |
| `clan_war_trophies` | `int  /  None` | `clanWarTrophies` |
| `required_trophies` | `int  /  None` | `requiredTrophies` |
| `donations_per_week` | `int  /  None` | `donationsPerWeek` |
| `members` | `int  /  None` | `members` |
| `name` | `str  /  None` | `name` |
| `location` | `ForwardRef('Location  /  None')` | `location` |
| `type` | `str  /  None` | `type` |
| `tag` | `str  /  None` | `tag` |
| `description` | `str  /  None` | `description` |
| `clan_chest_points` | `int  /  None` | `clanChestPoints` |
| `badge_urls` | `Any  /  None` | `badgeUrls` |

## ClanMember

| Attribute | Type | API field |
| --- | --- | --- |
| `tag` | `str  /  None` | `tag` |
| `name` | `str  /  None` | `name` |
| `role` | `str  /  None` | `role` |
| `last_seen` | `datetime  /  None` | `lastSeen` |
| `exp_level` | `int  /  None` | `expLevel` |
| `trophies` | `int  /  None` | `trophies` |
| `clan_rank` | `int  /  None` | `clanRank` |
| `previous_clan_rank` | `int  /  None` | `previousClanRank` |
| `donations` | `int  /  None` | `donations` |
| `donations_received` | `int  /  None` | `donationsReceived` |
| `arena` | `Arena  /  None` | `arena` |

## ClanRanking

| Attribute | Type | API field |
| --- | --- | --- |
| `tag` | `str  /  None` | `tag` |
| `name` | `str  /  None` | `name` |
| `rank` | `int  /  None` | `rank` |
| `previous_rank` | `int  /  None` | `previousRank` |
| `clan_score` | `int  /  None` | `clanScore` |
| `members` | `int  /  None` | `members` |
| `location` | `ForwardRef('Location  /  None')` | `location` |

## ClanWarClan

| Attribute | Type | API field |
| --- | --- | --- |
| `tag` | `str  /  None` | `tag` |
| `name` | `str  /  None` | `name` |
| `badge_id` | `int  /  None` | `badgeId` |
| `clan_score` | `int  /  None` | `clanScore` |

## ClanWarLogEntry

| Attribute | Type | API field |
| --- | --- | --- |
| `created_date` | `datetime  /  None` | `createdDate` |
| `standings` | `ForwardRef('list[ClanWarStanding]  /  None')` | `standings` |
| `participants` | `ForwardRef('list[ClanWarParticipant]  /  None')` | `participants` |

## ClanWarParticipant

| Attribute | Type | API field |
| --- | --- | --- |
| `tag` | `str  /  None` | `tag` |
| `name` | `str  /  None` | `name` |
| `wins` | `int  /  None` | `wins` |
| `battles_played` | `int  /  None` | `battlesPlayed` |

## ClanWarStanding

| Attribute | Type | API field |
| --- | --- | --- |
| `rank` | `int  /  None` | `rank` |
| `trophy_change` | `int  /  None` | `trophyChange` |
| `clan` | `ClanWarClan  /  None` | `clan` |

## CurrentClanWar

| Attribute | Type | API field |
| --- | --- | --- |
| `state` | `str  /  None` | `state` |
| `clan` | `ClanWarClan  /  None` | `clan` |
| `participants` | `list[ClanWarParticipant]  /  None` | `participants` |
| `clans` | `list[ClanWarClan]  /  None` | `clans` |
| `collection_end_time` | `datetime  /  None` | `collectionEndTime` |
| `war_end_time` | `datetime  /  None` | `warEndTime` |

## CurrentRiverRace

| Attribute | Type | API field |
| --- | --- | --- |
| `state` | `str  /  None` | `state` |
| `clan` | `ForwardRef('RiverRaceClan  /  None')` | `clan` |
| `clans` | `ForwardRef('list[RiverRaceClan]  /  None')` | `clans` |
| `collection_end_time` | `datetime  /  None` | `collectionEndTime` |
| `war_end_time` | `datetime  /  None` | `warEndTime` |
| `section_index` | `int  /  None` | `sectionIndex` |
| `period_index` | `int  /  None` | `periodIndex` |
| `period_type` | `str  /  None` | `periodType` |
| `period_logs` | `ForwardRef('list[PeriodLog]  /  None')` | `periodLogs` |

## GameMode

| Attribute | Type | API field |
| --- | --- | --- |
| `id` | `int  /  None` | `id` |
| `name` | `str  /  None` | `name` |

## Item

| Attribute | Type | API field |
| --- | --- | --- |
| `id` | `int  /  None` | `id` |
| `name` | `str  /  None` | `name` |
| `max_level` | `int  /  None` | `maxLevel` |
| `max_evolution_level` | `int  /  None` | `maxEvolutionLevel` |
| `rarity` | `str  /  None` | `rarity` |
| `elixir_cost` | `int  /  None` | `elixirCost` |
| `icon_urls` | `Any  /  None` | `iconUrls` |

## Items

| Attribute | Type | API field |
| --- | --- | --- |
| `items` | `list[Item]  /  None` | `items` |
| `support_items` | `list[Item]  /  None` | `supportItems` |

## LadderTournament

| Attribute | Type | API field |
| --- | --- | --- |
| `id` | `int  /  None` | `id` |
| `title` | `str  /  None` | `title` |
| `game_mode` | `GameMode  /  None` | `gameMode` |
| `start_time` | `datetime  /  None` | `startTime` |
| `end_time` | `datetime  /  None` | `endTime` |

## LadderTournamentRanking

| Attribute | Type | API field |
| --- | --- | --- |
| `tag` | `str  /  None` | `tag` |
| `name` | `str  /  None` | `name` |
| `rank` | `int  /  None` | `rank` |
| `score` | `int  /  None` | `score` |
| `clan` | `ForwardRef('PlayerRankingClan  /  None')` | `clan` |

## Leaderboard

| Attribute | Type | API field |
| --- | --- | --- |
| `id` | `int  /  None` | `id` |
| `name` | `Any  /  None` | `name` |
| `leagues` | `Any  /  None` | `leagues` |

## LeaderboardEntry

| Attribute | Type | API field |
| --- | --- | --- |
| `tag` | `str  /  None` | `tag` |
| `name` | `str  /  None` | `name` |
| `rank` | `int  /  None` | `rank` |
| `score` | `int  /  None` | `score` |
| `clan` | `ForwardRef('PlayerClan  /  None')` | `clan` |

## LeagueSeason

| Attribute | Type | API field |
| --- | --- | --- |
| `id` | `str  /  None` | `id` |

## LeagueSeasonResult

| Attribute | Type | API field |
| --- | --- | --- |
| `id` | `str  /  None` | `id` |
| `trophies` | `int  /  None` | `trophies` |
| `best_trophies` | `int  /  None` | `bestTrophies` |
| `rank` | `int  /  None` | `rank` |

## LeagueSeasonV2

| Attribute | Type | API field |
| --- | --- | --- |
| `code` | `str  /  None` | `code` |
| `unique_id` | `int  /  None` | `uniqueId` |
| `end_time` | `datetime  /  None` | `endTime` |

## Location

| Attribute | Type | API field |
| --- | --- | --- |
| `localized_name` | `str  /  None` | `localizedName` |
| `id` | `int  /  None` | `id` |
| `name` | `str  /  None` | `name` |
| `is_country` | `bool  /  None` | `isCountry` |
| `country_code` | `str  /  None` | `countryCode` |

## PathOfLegendSeasonResult

| Attribute | Type | API field |
| --- | --- | --- |
| `league_number` | `int  /  None` | `leagueNumber` |
| `trophies` | `int  /  None` | `trophies` |
| `rank` | `int  /  None` | `rank` |

## PeriodLog

| Attribute | Type | API field |
| --- | --- | --- |
| `period_index` | `int  /  None` | `periodIndex` |
| `items` | `ForwardRef('list[PeriodLogEntry]  /  None')` | `items` |

## PeriodLogEntry

| Attribute | Type | API field |
| --- | --- | --- |
| `clan` | `ForwardRef('PeriodLogEntryClan  /  None')` | `clan` |
| `points_earned` | `int  /  None` | `pointsEarned` |

## PeriodLogEntryClan

| Attribute | Type | API field |
| --- | --- | --- |
| `tag` | `str  /  None` | `tag` |
| `name` | `str  /  None` | `name` |

## Player

| Attribute | Type | API field |
| --- | --- | --- |
| `clan` | `ForwardRef('PlayerClan  /  None')` | `clan` |
| `legacy_trophy_road_high_score` | `int  /  None` | `legacyTrophyRoadHighScore` |
| `current_deck` | `ForwardRef('list[PlayerItemLevel]  /  None')` | `currentDeck` |
| `current_deck_support_cards` | `ForwardRef('list[PlayerItemLevel]  /  None')` | `currentDeckSupportCards` |
| `arena` | `Arena  /  None` | `arena` |
| `role` | `str  /  None` | `role` |
| `wins` | `int  /  None` | `wins` |
| `losses` | `int  /  None` | `losses` |
| `total_donations` | `int  /  None` | `totalDonations` |
| `league_statistics` | `ForwardRef('PlayerLeagueStatistics  /  None')` | `leagueStatistics` |
| `cards` | `ForwardRef('list[PlayerItemLevel]  /  None')` | `cards` |
| `support_cards` | `ForwardRef('list[PlayerItemLevel]  /  None')` | `supportCards` |
| `current_favourite_card` | `Item  /  None` | `currentFavouriteCard` |
| `badges` | `ForwardRef('list[PlayerAchievementBadge]  /  None')` | `badges` |
| `tag` | `str  /  None` | `tag` |
| `name` | `str  /  None` | `name` |
| `collection_level` | `int  /  None` | `collectionLevel` |
| `king_tower_level` | `int  /  None` | `kingTowerLevel` |
| `exp_level` | `int  /  None` | `expLevel` |
| `trophies` | `int  /  None` | `trophies` |
| `best_trophies` | `int  /  None` | `bestTrophies` |
| `donations` | `int  /  None` | `donations` |
| `donations_received` | `int  /  None` | `donationsReceived` |
| `achievements` | `ForwardRef('list[PlayerAchievementProgress]  /  None')` | `achievements` |
| `battle_count` | `int  /  None` | `battleCount` |
| `three_crown_wins` | `int  /  None` | `threeCrownWins` |
| `challenge_cards_won` | `int  /  None` | `challengeCardsWon` |
| `challenge_max_wins` | `int  /  None` | `challengeMaxWins` |
| `tournament_cards_won` | `int  /  None` | `tournamentCardsWon` |
| `tournament_battle_count` | `int  /  None` | `tournamentBattleCount` |
| `current_win_lose_streak` | `int  /  None` | `currentWinLoseStreak` |
| `war_day_wins` | `int  /  None` | `warDayWins` |
| `clan_cards_collected` | `int  /  None` | `clanCardsCollected` |
| `star_points` | `int  /  None` | `starPoints` |
| `exp_points` | `int  /  None` | `expPoints` |
| `total_exp_points` | `int  /  None` | `totalExpPoints` |
| `current_path_of_legend_season_result` | `PathOfLegendSeasonResult  /  None` | `currentPathOfLegendSeasonResult` |
| `last_path_of_legend_season_result` | `PathOfLegendSeasonResult  /  None` | `lastPathOfLegendSeasonResult` |
| `best_path_of_legend_season_result` | `PathOfLegendSeasonResult  /  None` | `bestPathOfLegendSeasonResult` |
| `progress` | `Any  /  None` | `progress` |

## PlayerAchievementBadge

| Attribute | Type | API field |
| --- | --- | --- |
| `name` | `str  /  None` | `name` |
| `level` | `int  /  None` | `level` |
| `max_level` | `int  /  None` | `maxLevel` |
| `progress` | `int  /  None` | `progress` |
| `target` | `int  /  None` | `target` |
| `icon_urls` | `Any  /  None` | `iconUrls` |

## PlayerAchievementProgress

| Attribute | Type | API field |
| --- | --- | --- |
| `name` | `str  /  None` | `name` |
| `stars` | `int  /  None` | `stars` |
| `value` | `int  /  None` | `value` |
| `target` | `int  /  None` | `target` |
| `info` | `str  /  None` | `info` |
| `completion_info` | `str  /  None` | `completionInfo` |

## PlayerBattleData

| Attribute | Type | API field |
| --- | --- | --- |
| `tag` | `str  /  None` | `tag` |
| `name` | `str  /  None` | `name` |
| `crowns` | `int  /  None` | `crowns` |
| `king_tower_hit_points` | `int  /  None` | `kingTowerHitPoints` |
| `princess_towers_hit_points` | `Any  /  None` | `princessTowersHitPoints` |
| `clan` | `ForwardRef('PlayerClan  /  None')` | `clan` |
| `cards` | `ForwardRef('list[PlayerItemLevel]  /  None')` | `cards` |
| `trophy_change` | `int  /  None` | `trophyChange` |
| `elixir_leaked` | `float  /  None` | `elixirLeaked` |

## PlayerClan

| Attribute | Type | API field |
| --- | --- | --- |
| `tag` | `str  /  None` | `tag` |
| `name` | `str  /  None` | `name` |
| `badge_id` | `int  /  None` | `badgeId` |

## PlayerItemLevel

| Attribute | Type | API field |
| --- | --- | --- |
| `id` | `int  /  None` | `id` |
| `name` | `str  /  None` | `name` |
| `level` | `int  /  None` | `level` |
| `max_level` | `int  /  None` | `maxLevel` |
| `count` | `int  /  None` | `count` |
| `star_level` | `int  /  None` | `starLevel` |
| `evolution_level` | `int  /  None` | `evolutionLevel` |
| `rarity` | `str  /  None` | `rarity` |
| `elixir_cost` | `int  /  None` | `elixirCost` |
| `icon_urls` | `Any  /  None` | `iconUrls` |

## PlayerLeagueStatistics

| Attribute | Type | API field |
| --- | --- | --- |
| `current_season` | `LeagueSeasonResult  /  None` | `currentSeason` |
| `previous_season` | `LeagueSeasonResult  /  None` | `previousSeason` |
| `best_season` | `LeagueSeasonResult  /  None` | `bestSeason` |

## PlayerPathOfLegendRanking

| Attribute | Type | API field |
| --- | --- | --- |
| `tag` | `str  /  None` | `tag` |
| `name` | `str  /  None` | `name` |
| `rank` | `int  /  None` | `rank` |
| `trophies` | `int  /  None` | `trophies` |
| `clan` | `ForwardRef('PlayerRankingClan  /  None')` | `clan` |
| `elo_rating` | `int  /  None` | `eloRating` |

## PlayerRanking

| Attribute | Type | API field |
| --- | --- | --- |
| `tag` | `str  /  None` | `tag` |
| `name` | `str  /  None` | `name` |
| `rank` | `int  /  None` | `rank` |
| `previous_rank` | `int  /  None` | `previousRank` |
| `trophies` | `int  /  None` | `trophies` |
| `clan` | `ForwardRef('PlayerRankingClan  /  None')` | `clan` |

## PlayerRankingClan

| Attribute | Type | API field |
| --- | --- | --- |
| `tag` | `str  /  None` | `tag` |
| `name` | `str  /  None` | `name` |
| `badge_id` | `int  /  None` | `badgeId` |

## RiverRaceClan

| Attribute | Type | API field |
| --- | --- | --- |
| `tag` | `str  /  None` | `tag` |
| `name` | `str  /  None` | `name` |
| `badge_id` | `int  /  None` | `badgeId` |
| `fame` | `int  /  None` | `fame` |
| `repair_points` | `int  /  None` | `repairPoints` |
| `clan_score` | `int  /  None` | `clanScore` |
| `participants` | `ForwardRef('list[RiverRaceParticipant]  /  None')` | `participants` |

## RiverRaceLogEntry

| Attribute | Type | API field |
| --- | --- | --- |
| `season_id` | `int  /  None` | `seasonId` |
| `section_index` | `int  /  None` | `sectionIndex` |
| `created_date` | `datetime  /  None` | `createdDate` |
| `standings` | `ForwardRef('list[RiverRaceStanding]  /  None')` | `standings` |

## RiverRaceParticipant

| Attribute | Type | API field |
| --- | --- | --- |
| `tag` | `str  /  None` | `tag` |
| `name` | `str  /  None` | `name` |
| `fame` | `int  /  None` | `fame` |
| `repair_points` | `int  /  None` | `repairPoints` |
| `decks_used` | `int  /  None` | `decksUsed` |
| `decks_used_today` | `int  /  None` | `decksUsedToday` |

## RiverRaceStanding

| Attribute | Type | API field |
| --- | --- | --- |
| `rank` | `int  /  None` | `rank` |
| `trophy_change` | `int  /  None` | `trophyChange` |
| `clan` | `RiverRaceClan  /  None` | `clan` |

## Tournament

| Attribute | Type | API field |
| --- | --- | --- |
| `game_mode` | `GameMode  /  None` | `gameMode` |
| `status` | `str  /  None` | `status` |
| `preparation_duration` | `int  /  None` | `preparationDuration` |
| `members_list` | `ForwardRef('list[TournamentMember]  /  None')` | `membersList` |
| `created_time` | `datetime  /  None` | `createdTime` |
| `started_time` | `datetime  /  None` | `startedTime` |
| `ended_time` | `datetime  /  None` | `endedTime` |
| `first_place_card_prize` | `int  /  None` | `firstPlaceCardPrize` |
| `type` | `str  /  None` | `type` |
| `duration` | `int  /  None` | `duration` |
| `tag` | `str  /  None` | `tag` |
| `creator_tag` | `str  /  None` | `creatorTag` |
| `name` | `str  /  None` | `name` |
| `description` | `str  /  None` | `description` |
| `capacity` | `int  /  None` | `capacity` |
| `max_capacity` | `int  /  None` | `maxCapacity` |
| `level_cap` | `int  /  None` | `levelCap` |

## TournamentHeader

| Attribute | Type | API field |
| --- | --- | --- |
| `tag` | `str  /  None` | `tag` |
| `name` | `str  /  None` | `name` |
| `status` | `str  /  None` | `status` |
| `capacity` | `int  /  None` | `capacity` |
| `max_capacity` | `int  /  None` | `maxCapacity` |

## TournamentMember

| Attribute | Type | API field |
| --- | --- | --- |
| `tag` | `str  /  None` | `tag` |
| `name` | `str  /  None` | `name` |
| `rank` | `int  /  None` | `rank` |
| `score` | `int  /  None` | `score` |

## TrailEvent

| Attribute | Type | API field |
| --- | --- | --- |
| `id` | `int  /  None` | `id` |
| `title` | `Any  /  None` | `title` |
| `description` | `Any  /  None` | `description` |
| `event_tag` | `str  /  None` | `eventTag` |

## UpcomingChests

| Attribute | Type | API field |
| --- | --- | --- |
| `items` | `list[Chest]  /  None` | `items` |
