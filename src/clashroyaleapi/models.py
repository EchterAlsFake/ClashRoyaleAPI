"""Typed response models; unknown API fields are retained."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel


class APIModel(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True, alias_generator=to_camel)

    def to_dict(self) -> dict[str, Any]:
        """Export JSON-compatible data with original API field names."""
        return self.model_dump(mode="json", by_alias=True, exclude_unset=True)


class Arena(APIModel):
    """Arena response; omitted fields remain None."""

    id: int | None = Field(default=None, alias="id")
    name: str | None = Field(default=None, alias="name")


class Battle(APIModel):
    """Battle response; omitted fields remain None."""

    type: str | None = Field(default=None, alias="type")
    battle_time: datetime | None = Field(default=None, alias="battleTime")
    is_ladder_tournament: bool | None = Field(default=None, alias="isLadderTournament")
    is_hosted_match: bool | None = Field(default=None, alias="isHostedMatch")
    deck_selection: str | None = Field(default=None, alias="deckSelection")
    league_number: int | None = Field(default=None, alias="leagueNumber")
    game_mode: GameMode | None = Field(default=None, alias="gameMode")
    arena: Arena | None = Field(default=None, alias="arena")
    team: list[PlayerBattleData] | None = Field(default=None, alias="team")
    opponent: list[PlayerBattleData] | None = Field(default=None, alias="opponent")

    @field_validator("battle_time", mode="before")
    @classmethod
    def parse_time(cls, value: Any) -> Any:
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y%m%dT%H%M%S.%fZ").replace(tzinfo=UTC)
            except ValueError:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
        return value


class Chest(APIModel):
    """Chest response; omitted fields remain None."""

    index: int | None = Field(default=None, alias="index")
    name: str | None = Field(default=None, alias="name")


class Clan(APIModel):
    """Clan response; omitted fields remain None."""

    badge_id: int | None = Field(default=None, alias="badgeId")
    member_list: list[ClanMember] | None = Field(default=None, alias="memberList")
    clan_chest_status: str | None = Field(default=None, alias="clanChestStatus")
    clan_chest_level: int | None = Field(default=None, alias="clanChestLevel")
    clan_chest_max_level: int | None = Field(default=None, alias="clanChestMaxLevel")
    clan_score: int | None = Field(default=None, alias="clanScore")
    clan_war_trophies: int | None = Field(default=None, alias="clanWarTrophies")
    required_trophies: int | None = Field(default=None, alias="requiredTrophies")
    donations_per_week: int | None = Field(default=None, alias="donationsPerWeek")
    members: int | None = Field(default=None, alias="members")
    name: str | None = Field(default=None, alias="name")
    location: Location | None = Field(default=None, alias="location")
    type: str | None = Field(default=None, alias="type")
    tag: str | None = Field(default=None, alias="tag")
    description: str | None = Field(default=None, alias="description")
    clan_chest_points: int | None = Field(default=None, alias="clanChestPoints")
    badge_urls: Any | None = Field(default=None, alias="badgeUrls")


class ClanMember(APIModel):
    """ClanMember response; omitted fields remain None."""

    tag: str | None = Field(default=None, alias="tag")
    name: str | None = Field(default=None, alias="name")
    role: str | None = Field(default=None, alias="role")
    last_seen: datetime | None = Field(default=None, alias="lastSeen")
    exp_level: int | None = Field(default=None, alias="expLevel")
    trophies: int | None = Field(default=None, alias="trophies")
    clan_rank: int | None = Field(default=None, alias="clanRank")
    previous_clan_rank: int | None = Field(default=None, alias="previousClanRank")
    donations: int | None = Field(default=None, alias="donations")
    donations_received: int | None = Field(default=None, alias="donationsReceived")
    arena: Arena | None = Field(default=None, alias="arena")

    @field_validator("last_seen", mode="before")
    @classmethod
    def parse_time(cls, value: Any) -> Any:
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y%m%dT%H%M%S.%fZ").replace(tzinfo=UTC)
            except ValueError:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
        return value


class ClanRanking(APIModel):
    """ClanRanking response; omitted fields remain None."""

    tag: str | None = Field(default=None, alias="tag")
    name: str | None = Field(default=None, alias="name")
    rank: int | None = Field(default=None, alias="rank")
    previous_rank: int | None = Field(default=None, alias="previousRank")
    clan_score: int | None = Field(default=None, alias="clanScore")
    members: int | None = Field(default=None, alias="members")
    location: Location | None = Field(default=None, alias="location")


class ClanWarClan(APIModel):
    """ClanWarClan response; omitted fields remain None."""

    tag: str | None = Field(default=None, alias="tag")
    name: str | None = Field(default=None, alias="name")
    badge_id: int | None = Field(default=None, alias="badgeId")
    clan_score: int | None = Field(default=None, alias="clanScore")


class ClanWarLogEntry(APIModel):
    """ClanWarLogEntry response; omitted fields remain None."""

    created_date: datetime | None = Field(default=None, alias="createdDate")
    standings: list[ClanWarStanding] | None = Field(default=None, alias="standings")
    participants: list[ClanWarParticipant] | None = Field(default=None, alias="participants")

    @field_validator("created_date", mode="before")
    @classmethod
    def parse_time(cls, value: Any) -> Any:
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y%m%dT%H%M%S.%fZ").replace(tzinfo=UTC)
            except ValueError:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
        return value


class ClanWarParticipant(APIModel):
    """ClanWarParticipant response; omitted fields remain None."""

    tag: str | None = Field(default=None, alias="tag")
    name: str | None = Field(default=None, alias="name")
    wins: int | None = Field(default=None, alias="wins")
    battles_played: int | None = Field(default=None, alias="battlesPlayed")


class ClanWarStanding(APIModel):
    """ClanWarStanding response; omitted fields remain None."""

    rank: int | None = Field(default=None, alias="rank")
    trophy_change: int | None = Field(default=None, alias="trophyChange")
    clan: ClanWarClan | None = Field(default=None, alias="clan")


class CurrentClanWar(APIModel):
    """CurrentClanWar response; omitted fields remain None."""

    state: str | None = Field(default=None, alias="state")
    clan: ClanWarClan | None = Field(default=None, alias="clan")
    participants: list[ClanWarParticipant] | None = Field(default=None, alias="participants")
    clans: list[ClanWarClan] | None = Field(default=None, alias="clans")
    collection_end_time: datetime | None = Field(default=None, alias="collectionEndTime")
    war_end_time: datetime | None = Field(default=None, alias="warEndTime")

    @field_validator("collection_end_time", "war_end_time", mode="before")
    @classmethod
    def parse_time(cls, value: Any) -> Any:
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y%m%dT%H%M%S.%fZ").replace(tzinfo=UTC)
            except ValueError:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
        return value


class CurrentRiverRace(APIModel):
    """CurrentRiverRace response; omitted fields remain None."""

    state: str | None = Field(default=None, alias="state")
    clan: RiverRaceClan | None = Field(default=None, alias="clan")
    clans: list[RiverRaceClan] | None = Field(default=None, alias="clans")
    collection_end_time: datetime | None = Field(default=None, alias="collectionEndTime")
    war_end_time: datetime | None = Field(default=None, alias="warEndTime")
    section_index: int | None = Field(default=None, alias="sectionIndex")
    period_index: int | None = Field(default=None, alias="periodIndex")
    period_type: str | None = Field(default=None, alias="periodType")
    period_logs: list[PeriodLog] | None = Field(default=None, alias="periodLogs")

    @field_validator("collection_end_time", "war_end_time", mode="before")
    @classmethod
    def parse_time(cls, value: Any) -> Any:
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y%m%dT%H%M%S.%fZ").replace(tzinfo=UTC)
            except ValueError:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
        return value


class GameMode(APIModel):
    """GameMode response; omitted fields remain None."""

    id: int | None = Field(default=None, alias="id")
    name: str | None = Field(default=None, alias="name")


class Item(APIModel):
    """Item response; omitted fields remain None."""

    id: int | None = Field(default=None, alias="id")
    name: str | None = Field(default=None, alias="name")
    max_level: int | None = Field(default=None, alias="maxLevel")
    max_evolution_level: int | None = Field(default=None, alias="maxEvolutionLevel")
    rarity: str | None = Field(default=None, alias="rarity")
    elixir_cost: int | None = Field(default=None, alias="elixirCost")
    icon_urls: Any | None = Field(default=None, alias="iconUrls")


class Items(APIModel):
    """Items response; omitted fields remain None."""

    items: list[Item] | None = Field(default=None, alias="items")
    support_items: list[Item] | None = Field(default=None, alias="supportItems")


class LadderTournament(APIModel):
    """LadderTournament response; omitted fields remain None."""

    id: int | None = Field(default=None, alias="id")
    title: str | None = Field(default=None, alias="title")
    game_mode: GameMode | None = Field(default=None, alias="gameMode")
    start_time: datetime | None = Field(default=None, alias="startTime")
    end_time: datetime | None = Field(default=None, alias="endTime")

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def parse_time(cls, value: Any) -> Any:
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y%m%dT%H%M%S.%fZ").replace(tzinfo=UTC)
            except ValueError:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
        return value


class LadderTournamentRanking(APIModel):
    """LadderTournamentRanking response; omitted fields remain None."""

    tag: str | None = Field(default=None, alias="tag")
    name: str | None = Field(default=None, alias="name")
    rank: int | None = Field(default=None, alias="rank")
    score: int | None = Field(default=None, alias="score")
    clan: PlayerRankingClan | None = Field(default=None, alias="clan")


class Leaderboard(APIModel):
    """Leaderboard response; omitted fields remain None."""

    id: int | None = Field(default=None, alias="id")
    name: Any | None = Field(default=None, alias="name")
    leagues: Any | None = Field(default=None, alias="leagues")


class LeaderboardEntry(APIModel):
    """LeaderboardEntry response; omitted fields remain None."""

    tag: str | None = Field(default=None, alias="tag")
    name: str | None = Field(default=None, alias="name")
    rank: int | None = Field(default=None, alias="rank")
    score: int | None = Field(default=None, alias="score")
    clan: PlayerClan | None = Field(default=None, alias="clan")


class LeagueSeason(APIModel):
    """LeagueSeason response; omitted fields remain None."""

    id: str | None = Field(default=None, alias="id")


class LeagueSeasonResult(APIModel):
    """LeagueSeasonResult response; omitted fields remain None."""

    id: str | None = Field(default=None, alias="id")
    trophies: int | None = Field(default=None, alias="trophies")
    best_trophies: int | None = Field(default=None, alias="bestTrophies")
    rank: int | None = Field(default=None, alias="rank")


class LeagueSeasonV2(APIModel):
    """LeagueSeasonV2 response; omitted fields remain None."""

    code: str | None = Field(default=None, alias="code")
    unique_id: int | None = Field(default=None, alias="uniqueId")
    end_time: datetime | None = Field(default=None, alias="endTime")

    @field_validator("end_time", mode="before")
    @classmethod
    def parse_time(cls, value: Any) -> Any:
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y%m%dT%H%M%S.%fZ").replace(tzinfo=UTC)
            except ValueError:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
        return value


class Location(APIModel):
    """Location response; omitted fields remain None."""

    localized_name: str | None = Field(default=None, alias="localizedName")
    id: int | None = Field(default=None, alias="id")
    name: str | None = Field(default=None, alias="name")
    is_country: bool | None = Field(default=None, alias="isCountry")
    country_code: str | None = Field(default=None, alias="countryCode")


class PathOfLegendSeasonResult(APIModel):
    """PathOfLegendSeasonResult response; omitted fields remain None."""

    league_number: int | None = Field(default=None, alias="leagueNumber")
    trophies: int | None = Field(default=None, alias="trophies")
    rank: int | None = Field(default=None, alias="rank")


class PeriodLog(APIModel):
    """PeriodLog response; omitted fields remain None."""

    period_index: int | None = Field(default=None, alias="periodIndex")
    items: list[PeriodLogEntry] | None = Field(default=None, alias="items")


class PeriodLogEntry(APIModel):
    """PeriodLogEntry response; omitted fields remain None."""

    clan: PeriodLogEntryClan | None = Field(default=None, alias="clan")
    points_earned: int | None = Field(default=None, alias="pointsEarned")


class PeriodLogEntryClan(APIModel):
    """PeriodLogEntryClan response; omitted fields remain None."""

    tag: str | None = Field(default=None, alias="tag")
    name: str | None = Field(default=None, alias="name")


class Player(APIModel):
    """Player response; omitted fields remain None."""

    clan: PlayerClan | None = Field(default=None, alias="clan")
    legacy_trophy_road_high_score: int | None = Field(
        default=None, alias="legacyTrophyRoadHighScore"
    )
    current_deck: list[PlayerItemLevel] | None = Field(default=None, alias="currentDeck")
    current_deck_support_cards: list[PlayerItemLevel] | None = Field(
        default=None, alias="currentDeckSupportCards"
    )
    arena: Arena | None = Field(default=None, alias="arena")
    role: str | None = Field(default=None, alias="role")
    wins: int | None = Field(default=None, alias="wins")
    losses: int | None = Field(default=None, alias="losses")
    total_donations: int | None = Field(default=None, alias="totalDonations")
    league_statistics: PlayerLeagueStatistics | None = Field(default=None, alias="leagueStatistics")
    cards: list[PlayerItemLevel] | None = Field(default=None, alias="cards")
    support_cards: list[PlayerItemLevel] | None = Field(default=None, alias="supportCards")
    current_favourite_card: Item | None = Field(default=None, alias="currentFavouriteCard")
    badges: list[PlayerAchievementBadge] | None = Field(default=None, alias="badges")
    tag: str | None = Field(default=None, alias="tag")
    name: str | None = Field(default=None, alias="name")
    collection_level: int | None = Field(default=None, alias="collectionLevel")
    king_tower_level: int | None = Field(default=None, alias="kingTowerLevel")
    exp_level: int | None = Field(default=None, alias="expLevel")
    trophies: int | None = Field(default=None, alias="trophies")
    best_trophies: int | None = Field(default=None, alias="bestTrophies")
    donations: int | None = Field(default=None, alias="donations")
    donations_received: int | None = Field(default=None, alias="donationsReceived")
    achievements: list[PlayerAchievementProgress] | None = Field(default=None, alias="achievements")
    battle_count: int | None = Field(default=None, alias="battleCount")
    three_crown_wins: int | None = Field(default=None, alias="threeCrownWins")
    challenge_cards_won: int | None = Field(default=None, alias="challengeCardsWon")
    challenge_max_wins: int | None = Field(default=None, alias="challengeMaxWins")
    tournament_cards_won: int | None = Field(default=None, alias="tournamentCardsWon")
    tournament_battle_count: int | None = Field(default=None, alias="tournamentBattleCount")
    current_win_lose_streak: int | None = Field(default=None, alias="currentWinLoseStreak")
    war_day_wins: int | None = Field(default=None, alias="warDayWins")
    clan_cards_collected: int | None = Field(default=None, alias="clanCardsCollected")
    star_points: int | None = Field(default=None, alias="starPoints")
    exp_points: int | None = Field(default=None, alias="expPoints")
    total_exp_points: int | None = Field(default=None, alias="totalExpPoints")
    current_path_of_legend_season_result: PathOfLegendSeasonResult | None = Field(
        default=None, alias="currentPathOfLegendSeasonResult"
    )
    last_path_of_legend_season_result: PathOfLegendSeasonResult | None = Field(
        default=None, alias="lastPathOfLegendSeasonResult"
    )
    best_path_of_legend_season_result: PathOfLegendSeasonResult | None = Field(
        default=None, alias="bestPathOfLegendSeasonResult"
    )
    progress: Any | None = Field(default=None, alias="progress")


class PlayerAchievementBadge(APIModel):
    """PlayerAchievementBadge response; omitted fields remain None."""

    name: str | None = Field(default=None, alias="name")
    level: int | None = Field(default=None, alias="level")
    max_level: int | None = Field(default=None, alias="maxLevel")
    progress: int | None = Field(default=None, alias="progress")
    target: int | None = Field(default=None, alias="target")
    icon_urls: Any | None = Field(default=None, alias="iconUrls")


class PlayerAchievementProgress(APIModel):
    """PlayerAchievementProgress response; omitted fields remain None."""

    name: str | None = Field(default=None, alias="name")
    stars: int | None = Field(default=None, alias="stars")
    value: int | None = Field(default=None, alias="value")
    target: int | None = Field(default=None, alias="target")
    info: str | None = Field(default=None, alias="info")
    completion_info: str | None = Field(default=None, alias="completionInfo")


class PlayerBattleData(APIModel):
    """PlayerBattleData response; omitted fields remain None."""

    tag: str | None = Field(default=None, alias="tag")
    name: str | None = Field(default=None, alias="name")
    crowns: int | None = Field(default=None, alias="crowns")
    king_tower_hit_points: int | None = Field(default=None, alias="kingTowerHitPoints")
    princess_towers_hit_points: Any | None = Field(default=None, alias="princessTowersHitPoints")
    clan: PlayerClan | None = Field(default=None, alias="clan")
    cards: list[PlayerItemLevel] | None = Field(default=None, alias="cards")
    trophy_change: int | None = Field(default=None, alias="trophyChange")
    elixir_leaked: float | None = Field(default=None, alias="elixirLeaked")


class PlayerClan(APIModel):
    """PlayerClan response; omitted fields remain None."""

    tag: str | None = Field(default=None, alias="tag")
    name: str | None = Field(default=None, alias="name")
    badge_id: int | None = Field(default=None, alias="badgeId")


class PlayerItemLevel(APIModel):
    """PlayerItemLevel response; omitted fields remain None."""

    id: int | None = Field(default=None, alias="id")
    name: str | None = Field(default=None, alias="name")
    level: int | None = Field(default=None, alias="level")
    max_level: int | None = Field(default=None, alias="maxLevel")
    count: int | None = Field(default=None, alias="count")
    star_level: int | None = Field(default=None, alias="starLevel")
    evolution_level: int | None = Field(default=None, alias="evolutionLevel")
    rarity: str | None = Field(default=None, alias="rarity")
    elixir_cost: int | None = Field(default=None, alias="elixirCost")
    icon_urls: Any | None = Field(default=None, alias="iconUrls")


class PlayerLeagueStatistics(APIModel):
    """PlayerLeagueStatistics response; omitted fields remain None."""

    current_season: LeagueSeasonResult | None = Field(default=None, alias="currentSeason")
    previous_season: LeagueSeasonResult | None = Field(default=None, alias="previousSeason")
    best_season: LeagueSeasonResult | None = Field(default=None, alias="bestSeason")


class PlayerPathOfLegendRanking(APIModel):
    """PlayerPathOfLegendRanking response; omitted fields remain None."""

    tag: str | None = Field(default=None, alias="tag")
    name: str | None = Field(default=None, alias="name")
    rank: int | None = Field(default=None, alias="rank")
    trophies: int | None = Field(default=None, alias="trophies")
    clan: PlayerRankingClan | None = Field(default=None, alias="clan")
    elo_rating: int | None = Field(default=None, alias="eloRating")


class PlayerRanking(APIModel):
    """PlayerRanking response; omitted fields remain None."""

    tag: str | None = Field(default=None, alias="tag")
    name: str | None = Field(default=None, alias="name")
    rank: int | None = Field(default=None, alias="rank")
    previous_rank: int | None = Field(default=None, alias="previousRank")
    trophies: int | None = Field(default=None, alias="trophies")
    clan: PlayerRankingClan | None = Field(default=None, alias="clan")


class PlayerRankingClan(APIModel):
    """PlayerRankingClan response; omitted fields remain None."""

    tag: str | None = Field(default=None, alias="tag")
    name: str | None = Field(default=None, alias="name")
    badge_id: int | None = Field(default=None, alias="badgeId")


class RiverRaceClan(APIModel):
    """RiverRaceClan response; omitted fields remain None."""

    tag: str | None = Field(default=None, alias="tag")
    name: str | None = Field(default=None, alias="name")
    badge_id: int | None = Field(default=None, alias="badgeId")
    fame: int | None = Field(default=None, alias="fame")
    repair_points: int | None = Field(default=None, alias="repairPoints")
    clan_score: int | None = Field(default=None, alias="clanScore")
    participants: list[RiverRaceParticipant] | None = Field(default=None, alias="participants")


class RiverRaceLogEntry(APIModel):
    """RiverRaceLogEntry response; omitted fields remain None."""

    season_id: int | None = Field(default=None, alias="seasonId")
    section_index: int | None = Field(default=None, alias="sectionIndex")
    created_date: datetime | None = Field(default=None, alias="createdDate")
    standings: list[RiverRaceStanding] | None = Field(default=None, alias="standings")

    @field_validator("created_date", mode="before")
    @classmethod
    def parse_time(cls, value: Any) -> Any:
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y%m%dT%H%M%S.%fZ").replace(tzinfo=UTC)
            except ValueError:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
        return value


class RiverRaceParticipant(APIModel):
    """RiverRaceParticipant response; omitted fields remain None."""

    tag: str | None = Field(default=None, alias="tag")
    name: str | None = Field(default=None, alias="name")
    fame: int | None = Field(default=None, alias="fame")
    repair_points: int | None = Field(default=None, alias="repairPoints")
    decks_used: int | None = Field(default=None, alias="decksUsed")
    decks_used_today: int | None = Field(default=None, alias="decksUsedToday")


class RiverRaceStanding(APIModel):
    """RiverRaceStanding response; omitted fields remain None."""

    rank: int | None = Field(default=None, alias="rank")
    trophy_change: int | None = Field(default=None, alias="trophyChange")
    clan: RiverRaceClan | None = Field(default=None, alias="clan")


class Tournament(APIModel):
    """Tournament response; omitted fields remain None."""

    game_mode: GameMode | None = Field(default=None, alias="gameMode")
    status: str | None = Field(default=None, alias="status")
    preparation_duration: int | None = Field(default=None, alias="preparationDuration")
    members_list: list[TournamentMember] | None = Field(default=None, alias="membersList")
    created_time: datetime | None = Field(default=None, alias="createdTime")
    started_time: datetime | None = Field(default=None, alias="startedTime")
    ended_time: datetime | None = Field(default=None, alias="endedTime")
    first_place_card_prize: int | None = Field(default=None, alias="firstPlaceCardPrize")
    type: str | None = Field(default=None, alias="type")
    duration: int | None = Field(default=None, alias="duration")
    tag: str | None = Field(default=None, alias="tag")
    creator_tag: str | None = Field(default=None, alias="creatorTag")
    name: str | None = Field(default=None, alias="name")
    description: str | None = Field(default=None, alias="description")
    capacity: int | None = Field(default=None, alias="capacity")
    max_capacity: int | None = Field(default=None, alias="maxCapacity")
    level_cap: int | None = Field(default=None, alias="levelCap")

    @field_validator("created_time", "started_time", "ended_time", mode="before")
    @classmethod
    def parse_time(cls, value: Any) -> Any:
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y%m%dT%H%M%S.%fZ").replace(tzinfo=UTC)
            except ValueError:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
        return value


class TournamentHeader(APIModel):
    """TournamentHeader response; omitted fields remain None."""

    tag: str | None = Field(default=None, alias="tag")
    name: str | None = Field(default=None, alias="name")
    status: str | None = Field(default=None, alias="status")
    capacity: int | None = Field(default=None, alias="capacity")
    max_capacity: int | None = Field(default=None, alias="maxCapacity")


class TournamentMember(APIModel):
    """TournamentMember response; omitted fields remain None."""

    tag: str | None = Field(default=None, alias="tag")
    name: str | None = Field(default=None, alias="name")
    rank: int | None = Field(default=None, alias="rank")
    score: int | None = Field(default=None, alias="score")


class TrailEvent(APIModel):
    """TrailEvent response; omitted fields remain None."""

    id: int | None = Field(default=None, alias="id")
    title: Any | None = Field(default=None, alias="title")
    description: Any | None = Field(default=None, alias="description")
    event_tag: str | None = Field(default=None, alias="eventTag")


class UpcomingChests(APIModel):
    """UpcomingChests response; omitted fields remain None."""

    items: list[Chest] | None = Field(default=None, alias="items")


T = TypeVar("T", bound=APIModel)


class Cursors(APIModel):
    before: str | None = None
    after: str | None = None


class Paging(APIModel):
    cursors: Cursors = Field(default_factory=Cursors)


class Page(APIModel, Generic[T]):
    items: list[T] = Field(default_factory=list)
    paging: Paging = Field(default_factory=Paging)


__all__ = [
    "APIModel",
    "Cursors",
    "Paging",
    "Page",
    "Arena",
    "Battle",
    "Chest",
    "Clan",
    "ClanMember",
    "ClanRanking",
    "ClanWarClan",
    "ClanWarLogEntry",
    "ClanWarParticipant",
    "ClanWarStanding",
    "CurrentClanWar",
    "CurrentRiverRace",
    "GameMode",
    "Item",
    "Items",
    "LadderTournament",
    "LadderTournamentRanking",
    "Leaderboard",
    "LeaderboardEntry",
    "LeagueSeason",
    "LeagueSeasonResult",
    "LeagueSeasonV2",
    "Location",
    "PathOfLegendSeasonResult",
    "PeriodLog",
    "PeriodLogEntry",
    "PeriodLogEntryClan",
    "Player",
    "PlayerAchievementBadge",
    "PlayerAchievementProgress",
    "PlayerBattleData",
    "PlayerClan",
    "PlayerItemLevel",
    "PlayerLeagueStatistics",
    "PlayerPathOfLegendRanking",
    "PlayerRanking",
    "PlayerRankingClan",
    "RiverRaceClan",
    "RiverRaceLogEntry",
    "RiverRaceParticipant",
    "RiverRaceStanding",
    "Tournament",
    "TournamentHeader",
    "TournamentMember",
    "TrailEvent",
    "UpcomingChests",
]
