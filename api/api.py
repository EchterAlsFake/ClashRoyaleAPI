"""
ClashRoyaleAPI Copyright (C) 2025 Johannes Habel <EchterAlsFake@proton.me>
Licensed under the General Public License v3, see LICENSE for details
"""

import time
import httpx

from modules.errors import *
from datetime import datetime
from functools import cached_property
from typing import Generator, Optional

test_token = ""


class APICache:
    def __init__(self, ttl: Optional[int] = 300):
        """
        :param ttl: Time-to-live for cache entries in seconds. Set to None to cache forever.
        """
        self._cache = {}
        self._ttl = ttl  # seconds

    def _is_valid(self, timestamp: float) -> bool:
        if self._ttl is None:
            return True
        return (time.time() - timestamp) < self._ttl

    def get(self, url: str) -> Optional[dict]:
        entry = self._cache.get(url)
        if entry:
            timestamp, data = entry
            if self._is_valid(timestamp):
                return data
            else:
                self._cache.pop(url, None)  # expired
        return None

    def set(self, url: str, data: dict) -> None:
        self._cache[url] = (time.time(), data)


class BaseCard:
    """
    A base class for a general card in Clash Roayle.
    Used in everything that has something to do with
    a card, to keep the codebase minimal and use abstraction
    for more efficiency.
    """
    def __init__(self, card_data: dict):
        self.card_data = card_data

    @cached_property
    def name(self) -> str:
        value = self.card_data.get("name")
        return str(value) if value is not None else None

    @cached_property
    def id(self) -> int:
        value = self.card_data.get("id")
        return int(value) if value is not None else None

    @cached_property
    def level(self) -> int:
        value = self.card_data.get("level")
        return int(value) if value is not None else None

    @cached_property
    def max_level(self) -> int:
        value = self.card_data.get("maxLevel")
        return int(value) if value is not None else None

    @cached_property
    def rarity(self) -> str:
        value = self.card_data.get("rarity")
        return str(value) if value is not None else None

    @cached_property
    def count(self) -> int | None:
        value = self.card_data.get("count")
        return int(value) if value is not None else None

    @cached_property
    def elixir_cost(self) -> int | None:
        value = self.card_data.get("elixirCost")
        return int(value) if value is not None else None

    @cached_property
    def star_level(self) -> int | None:
        value = str(self.card_data.get("starLevel"))
        return int(value) if value is not None else None

    @cached_property
    def evolution_level(self) -> int | None:
        value = self.card_data.get("evolutionLevel")
        return int(value) if value is not None else None

    def get_icon_urls(self) -> dict:
        return self.card_data.get("iconUrls", {})


class BaseNamedProgress:
    """
    A base class for a general achievement or badge.
    Used in everything that has something to do with
    a card, to keep the codebase minimal and use abstraction
    for more efficiency.
    """
    def __init__(self, data: dict):
        self.data = data

    @cached_property
    def name(self) -> str:
        value = self.data.get("name")
        return str(value) if value is not None else None

    @cached_property
    def level(self) -> int:
        value = self.data.get("level")
        return int(value) if value is not None else None

    @cached_property
    def max_level(self) -> int:
        value = self.data.get("maxLevel")
        return int(value) if value is not None else None

    @cached_property
    def progress(self) -> int:
        value = self.data.get("progress")
        return int(value) if value is not None else None

    @cached_property
    def target(self) -> int:
        value = self.data.get("target")
        return int(value) if value is not None else None

    def get_icon_urls(self) -> dict:
        return self.data.get("iconUrls", {})

"""
Everything Player related
"""

class PlayerLeagueStatistics:
    def __init__(self, stats: dict):
        self.current_season: dict = stats.get("currentSeason")
        self.previous_season: dict = stats.get("previousSeason")
        self.best_season: dict = stats.get("bestSeason")

    @cached_property
    def current_season_trophies(self) -> int:
        return int(self.current_season.get("trophies"))

    @cached_property
    def current_season_best_trophies(self) -> int:
        return int(self.current_season.get("bestTrophies"))

    @cached_property
    def previous_season_id(self) -> str:
        return str(self.previous_season.get("id"))

    @cached_property
    def previous_season_trophies(self) -> int:
        return int(self.previous_season.get("trophies"))

    @cached_property
    def previous_season_best_trophies(self) -> int:
        return int(self.previous_season.get("bestTrophies"))

    @cached_property
    def best_season_id(self) -> str:
        return str(self.best_season.get("id"))

    @cached_property
    def best_season_trophies(self) -> int:
        return int(self.best_season.get("trophies"))


class PlayerBadge(BaseNamedProgress):
    pass


class PlayerAchievement(BaseCard):
    def __init__(self, achievement: dict):
        super().__init__(achievement)
        self.achievement = achievement

    @cached_property
    def stars(self) -> int:
        return int(self.achievement.get("stars"))

    @cached_property
    def value(self) -> int:
        return int(self.achievement.get("value"))

    @cached_property
    def info(self) -> str:
        return str(self.achievement.get("info"))

    @cached_property
    def completion_info(self) -> str:
        return str(self.achievement.get("completionInfo"))


class PlayerCard(BaseCard):
    pass


class PlayerSupportCard(BaseCard):
    pass


class PlayerCurrentDeck(BaseCard):
    pass


class PlayerCurrentSupportCard(BaseCard):
    pass


class PlayerCurrentFavouriteCard(BaseCard):
    pass


class PlayerBattleBase:
    def __init__(self, data: dict):
        self.data = data

    @cached_property
    def tag(self) -> str:
        return str(self.data.get("tag"))

    @cached_property
    def name(self) -> str:
        return str(self.data.get("name"))

    @cached_property
    def crowns(self) -> int:
        return int(self.data.get("crowns"))

    @cached_property
    def king_tower_hit_points(self) -> int:
        return int(self.data.get("kingTowerHitPoints"))

    @cached_property
    def princess_tower_hit_points(self) -> list | str:
        values = self.data.get("princessTowerHitPoints")
        return values

    @cached_property
    def clan_tag(self) -> str | None:
        return self.data.get("clan").get("tag")

    @cached_property
    def clan_name(self) -> str | None:
        return self.data.get("clan").get("name")

    @cached_property
    def clan_badge_id(self) -> int | None:
        return self.data.get("clan").get("badgeId")

    @cached_property
    def trophy_change(self) -> int | None:
        return self.data.get("trophyChange")

    @cached_property
    def global_rank(self) -> str | int:
        return self.data.get("globalRank")

    @cached_property
    def elixir_leaked(self) -> float | int:
        return self.data.get("elixirLeaked")

    def get_cards(self) -> Generator[PlayerCard, None, None]:
        for card in self.data.get("cards", []):
            yield PlayerCard(card)


class PlayerBattleTeam(PlayerBattleBase):
    pass

class PlayerBattleOpponent(PlayerBattleBase):
    pass


class PlayerBattleLog:
    def __init__(self, data: dict):
        self.data = data

    @cached_property
    def type(self) -> str:
        return str(self.data.get("type"))

    @cached_property
    def battle_time(self) -> datetime:
        return datetime.strptime(self.data.get("battleTime"), "%Y%m%dT%H%M%S.%fZ")

    @cached_property
    def is_ladder_tournament(self) -> bool:
        return False if self.data.get("isLadderTournament") == "false" else True

    @cached_property
    def deck_selection(self) -> str:
        return str(self.data.get("deckSelection"))

    @cached_property
    def is_hosted_match(self) -> bool:
        return True if self.data.get("isHostedMatch") == "true" else False

    @cached_property
    def league_number(self) -> int:
        return int(self.data.get("leagueNumber"))

    def get_game_mode(self) -> dict:
        return dict(self.data.get("gameMode"))

    def get_arena(self) -> dict:
        return dict(self.data.get("arena"))

    def get_team_data(self) -> Generator[PlayerBattleTeam, None, None]:
        for team in self.data.get("team", []):
            yield PlayerBattleTeam(team)

    def get_opponent_team_data(self) -> Generator[PlayerBattleOpponent, None, None]:
        for opponent in self.data.get("opponent", []):
            yield PlayerBattleOpponent(opponent)


class Player:
    def __init__(self, data: dict):
        self.data = data

    @cached_property
    def name(self) -> str:
        return str(self.data.get("name"))

    @cached_property
    def experience_level(self) -> int:
        return int(self.data.get("expLevel"))

    @cached_property
    def trophies(self) -> int:
        return int(self.data.get("trophies"))

    @cached_property
    def best_trophies(self) -> int:
        return int(self.data.get("bestTrophies"))

    @cached_property
    def wins(self) -> int:
        return int(self.data.get("wins"))

    @cached_property
    def losses(self) -> int:
        return int(self.data.get("losses"))

    @cached_property
    def battle_count(self) -> int:
        return int(self.data.get("battleCount"))

    @cached_property
    def three_crown_wins(self) -> int:
        return int(self.data.get("threeCrownWins"))

    @cached_property
    def challenge_cards_won(self) -> int:
        return int(self.data.get("challengeCardsWon"))

    @cached_property
    def challenge_max_win(self) -> int:
        return int(self.data.get("challengeMaxWin"))

    @cached_property
    def tournament_cards_won(self) -> int:
        return int(self.data.get("tournamentCardsWon"))

    @cached_property
    def tournament_battle_count(self) -> int:
        return int(self.data.get("tournamentBattleCount"))

    @cached_property
    def clan_role(self) -> str:
        return str(self.data.get("role"))

    @cached_property
    def clan_donations_currently(self) -> int:
        return int(self.data.get("donations"))

    @cached_property
    def clan_donations_received_currently(self) -> int:
        return int(self.data.get("donationsReceived"))

    @cached_property
    def clan_donations_total(self) -> int:
        return int(self.data.get("totalDonations"))

    @cached_property
    def war_day_wins_currently(self) -> int:
        return int(self.data.get("warDayWins"))

    @cached_property
    def clan_cards_collected(self) -> int:
        return int(self.data.get("clanCardsCollected"))

    @cached_property
    def clan_tag(self) -> str:
        return str(self.data.get("clan")["tag"])

    @cached_property
    def clan_name(self) -> str:
        return str(self.data.get("clan")["name"])

    @cached_property
    def clan_badge_id(self) -> int:
        return int(self.data.get("clan")["badgeId"])

    @cached_property
    def current_arena_id(self) -> int:
        return int(self.data.get("arena")["id"])

    @cached_property
    def current_arena_name(self) -> str:
        return str(self.data.get("arena")["name"])

    @cached_property
    def star_points(self) -> int:
        return int(self.data.get("starPoints"))

    @cached_property
    def exp_points(self) -> int:
        return int(self.data.get("expPoints"))

    @cached_property
    def total_exp_points(self) -> int:
        return int(self.data.get("totalExpPoints"))

    @cached_property
    def legacy_trophy_road_highscore(self) -> int:
        return int(self.data.get("legacyTrophyRoadHighscore"))

    def get_league_statistics(self) -> PlayerLeagueStatistics:
        return PlayerLeagueStatistics(stats=self.data.get("leagueStatistics"))

    def get_player_badges(self) -> Generator[PlayerBadge, None, None]:
        badge_data_raw = self.data.get("badges")
        for badge in badge_data_raw:
            yield PlayerBadge(badge)

    def get_player_achievements(self) -> Generator[PlayerAchievement, None, None]:
        achievement_data_raw = self.data.get("achievements")
        for achievement in achievement_data_raw:
            yield PlayerAchievement(achievement)

    def get_player_cards(self) -> Generator[PlayerCard, None, None]:
        player_cards_raw = self.data.get("cards")
        for card in player_cards_raw:
            yield PlayerCard(card)

    def get_player_support_cards(self) -> Generator[PlayerSupportCard, None, None]:
        player_support_cards_raw = self.data.get("supportCards")
        for support_card in player_support_cards_raw:
            yield PlayerSupportCard(support_card)

    def get_player_current_deck(self) -> Generator[PlayerCurrentDeck, None, None]:
        player_current_deck_raw = self.data.get("currentDeck")
        for current_deck in player_current_deck_raw:
            yield PlayerCurrentDeck(current_deck)

    def get_player_current_support_cards(self) -> Generator[PlayerCurrentSupportCard, None, None]:
        player_current_support_card_raw = self.data.get("currentDeckSupportCards")
        for support_card_raw in player_current_support_card_raw:
            yield PlayerCurrentSupportCard(support_card_raw)

    def get_player_current_favorite_card(self) -> Generator[PlayerCurrentFavouriteCard, None, None]:
        yield PlayerCurrentFavouriteCard(self.data.get("currentFavouriteCard"))

    def get_current_path_of_legend_season_result(self) -> dict:
        return dict(self.data.get("currentPathOfLegendSeasonResult"))

    def get_last_path_of_legend_season_result(self) -> dict:
        return dict(self.data.get("lastPathOfLegendSeasonResult"))

    def get_best_path_of_legend_season_result(self) -> dict:
        return dict(self.data.get("bestPathOfLegendSeasonResult"))

    def get_player_progress(self) -> dict:
        return dict(self.data.get("progress"))



"""
Everything clan related
"""


class ClanMember:
    def __init__(self, member_data):
        self.member_data = member_data

    @cached_property
    def tag(self) -> str:
        return self.member_data.get("tag")

    @cached_property
    def name(self) -> str:
        return self.member_data.get("name")

    @cached_property
    def role(self) -> str:
        return self.member_data.get("role")

    @cached_property
    def last_seen(self) -> datetime:
        return datetime.strptime(self.member_data.get("lastSeen"), "%Y%m%dT%H%M%S.%fZ")

    @cached_property
    def exp_level(self) -> int:
        return self.member_data.get("expLevel")

    @cached_property
    def trophies(self) -> int:
        return self.member_data.get("trophies")

    @cached_property
    def clan_rank(self) -> int:
        return int(self.member_data.get("clanRank"))

    @cached_property
    def previous_clan_rank(self) -> int:
        return int(self.member_data.get("previousClanRank"))

    @cached_property
    def donations(self) -> int:
        return int(self.member_data.get("donations"))

    @cached_property
    def donations_received(self) -> int:
        return int(self.member_data.get("donationsReceived"))

    @cached_property
    def clan_chest_points(self) -> int:
        return int(self.member_data.get("clanChestPoints"))

    def get_arena(self) -> dict:
        return dict(self.member_data.get("arena"))


class Clan:
    def __init__(self, data: dict, cursor = None):
        self.data = data
        self.cursor = cursor

    @cached_property
    def name(self) -> str:
        return str(self.data.get("name"))

    @cached_property
    def type(self) -> str:
        return str(self.data.get("type"))

    @cached_property
    def description(self) -> str:
        return str(self.data.get("description"))

    @cached_property
    def badge_id(self) -> int:
        return int(self.data.get("badgeId"))

    @cached_property
    def clan_score(self) -> int:
        return int(self.data.get("clanScore"))

    @cached_property
    def clan_war_trophies(self) -> int:
        return int(self.data.get("clanWarTrophies"))

    @cached_property
    def required_trophies(self) -> int:
        return int(self.data.get("requiredTrophies"))

    @cached_property
    def donations_per_week(self) -> int:
        return int(self.data.get("donationsPerWeek"))

    @cached_property
    def clan_chest_status(self) -> str:
        return str(self.data.get("clanChestStatus"))

    @cached_property
    def clan_chest_level(self) -> int:
        return int(self.data.get("clanChestLevel"))

    @cached_property
    def clan_chest_max_level(self) -> int:
        return int(self.data.get("clanChestMaxLevel"))

    @cached_property
    def member_count(self) -> int:
        return int(self.data.get("members"))

    def get_members(self) -> Generator[ClanMember, None, None]:
        for member_data in self.data.get("memberList"):
            yield ClanMember(member_data)

    def get_location(self) -> dict:
        return dict(self.data.get("location"))


class ClanRiverRaceLog:
    def __init__(self, data: dict):
        pass


class ClanRiverRaceCurrent:
    pass

class RoyaleAPI:
    def __init__(self, api_token: str, timeout=20, proxy=None, verify=True, ttl=None):
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Accept": "application/json"
        }
        self.client = httpx.Client(timeout=timeout, headers=self.headers, proxy=proxy, verify=verify)
        self.cache = APICache(ttl=ttl)

    def fetch_api_request(self, url):
        json_response = self.cache.get(url=url)

        if not json_response:
            response = self.client.get(url=url)

            if response.status_code == 200:
                json_response: dict = response.json()
                self.cache.set(url=url, data=json_response)  # Apply values to temporary cache

            elif response.status_code == 403:
                raise InvalidAPIToken(f"Your API token is invalid, or you've been completely blocked. Make sure to "
                                      f"whitelist your IP address on the Clash Royale API Dashboard!")

            elif response.status_code == 429:
                raise RateLimitExceeded(f"Ratelimit has been exceeded, please try again later.")

            elif response.status_code == 500:
                raise APIError(
                    "Internal Server Error, please try again later. If problem persists, reach out to Supercell support.")

            elif response.status_code == 503:
                raise APIError(
                    "The official API is currently under maintenance or in different terms unavailable, please try again later.")

            elif response.status_code == 400:
                raise InvalidParameter(
                    "An invalid parameter was passed. Is the player tag correct? Make sure it follows the format like: #2VVYYRVYP")

        return json_response

    def get_player(self, player_tag: str) -> Player:
        player_tag = str(player_tag.replace("#", "%23"))
        url = f"https://api.clashroyale.com/v1/players/{player_tag}"
        data = self.fetch_api_request(url=url)
        return Player(data)

    def get_player_chest_cycle(self, player_tag: str) -> dict:
        player_tag = str(player_tag.replace("#", "%23"))
        url = f"https://api.clashroyale.com/v1/players/{player_tag}/upcomingchests"
        data = self.fetch_api_request(url=url)
        cycle = data.get("items")
        return cycle

    def get_player_battle_log(self, player_tag: str) -> Generator[PlayerBattleLog, None, None]:
        player_tag = str(player_tag.replace("#", "%23"))
        url = f"https://api.clashroyale.com/v1/players/{player_tag}/battlelog"
        data = self.fetch_api_request(url=url)
        for log in data:
            yield PlayerBattleLog(log)

    def get_clan(self, clan_tag: str) -> Clan:
        clan_tag = str(clan_tag.replace("#", "%23"))
        url = f"https://api.clashroyale.com/v1/clans/{clan_tag}"
        data = self.fetch_api_request(url=url)
        return Clan(data)

    def get_clan_river_race_log(self, clan_tag: str) -> ClanRiverRaceLog:
        clan_tag = str(clan_tag.replace("#", "%23"))
        url = f"https://api.clashroyale.com/v1/clans/{clan_tag}/riverracelog"
        data = self.fetch_api_request(url=url)
        return ClanRiverRaceLog(data)

    def search_clans(self, query: str, location_id: str = None, min_members: int = None, max_members: int = None,
                     min_score: int = 0, limit: int = None, after: str = None, before: str = None) -> Generator[Clan, None, None]:
            pass


if __name__ == "__main__":
    api = RoyaleAPI(api_token=test_token)
    battle_log = api.get_player_battle_log(player_tag="#2VVYYRVYP")

