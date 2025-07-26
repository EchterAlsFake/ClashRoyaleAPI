"""
ClashRoyaleAPI Copyright (C) 2025 Johannes Habel <EchterAlsFake@proton.me>
Licensed under the General Public License v3, see LICENSE for details
"""

import time
import httpx

from modules.errors import *
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
        return str(self.card_data.get("name"))

    @cached_property
    def id(self) -> int:
        return int(self.card_data.get("id"))

    @cached_property
    def level(self) -> int:
        return int(self.card_data.get("level", 0))

    @cached_property
    def max_level(self) -> int:
        return int(self.card_data.get("maxLevel", 0))

    @cached_property
    def rarity(self) -> str:
        return str(self.card_data.get("rarity"))

    @cached_property
    def count(self) -> int:
        return int(self.card_data.get("count", 0))

    @cached_property
    def elixir_cost(self) -> int:
        return int(self.card_data.get("elixirCost", 0))

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
        return str(self.data.get("name"))

    @cached_property
    def level(self) -> int:
        return int(self.data.get("level", 0))

    @cached_property
    def max_level(self) -> int:
        return int(self.data.get("maxLevel", 0))

    @cached_property
    def progress(self) -> int:
        return int(self.data.get("progress", 0))

    @cached_property
    def target(self) -> int:
        return int(self.data.get("target", 0))

    def get_icon_urls(self) -> dict:
        return self.data.get("iconUrls", {})


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


class Player:
    def __init__(self, player_tag: str, client: httpx.Client, cache: APICache):
        self.client = client
        self.cache = cache
        self.player_tag = str(player_tag).replace("#", "%23")
        url = f"https://api.clashroyale.com/v1/players/{self.player_tag}"
        self.json_response = self.cache.get(url=url)

        if not self.json_response:
            response = self.client.get(url=url)

            if response.status_code == 200:
                self.json_response: dict = response.json()
                self.cache.set(url=url, data=self.json_response) # Apply values to temporary cache

            elif response.status_code == 403:
                raise InvalidAPIToken(f"Your API token is invalid, or you've been completely blocked. Make sure to "
                                      f"whitelist your IP address on the Clash Royale API Dashboard!")

            elif response.status_code == 429:
                raise RateLimitExceeded(f"Ratelimit has been exceeded, please try again later.")

            elif response.status_code == 500:
                raise APIError("Internal Server Error, please try again later. If problem persists, reach out to Supercell support.")

            elif response.status_code == 503:
                raise APIError("The official API is currently under maintenance or in different terms unavailable, please try again later.")

            elif response.status_code == 400:
                raise InvalidParameter("An invalid parameter was passed. Is the player tag correct? Make sure it follows the format like: #2VVYYRVYP")


    @cached_property
    def name(self) -> str:
        return str(self.json_response.get("name"))

    @cached_property
    def experience_level(self) -> int:
        return int(self.json_response.get("expLevel"))

    @cached_property
    def trophies(self) -> int:
        return int(self.json_response.get("trophies"))

    @cached_property
    def best_trophies(self) -> int:
        return int(self.json_response.get("bestTrophies"))

    @cached_property
    def wins(self) -> int:
        return int(self.json_response.get("wins"))

    @cached_property
    def losses(self) -> int:
        return int(self.json_response.get("losses"))

    @cached_property
    def battle_count(self) -> int:
        return int(self.json_response.get("battleCount"))

    @cached_property
    def three_crown_wins(self) -> int:
        return int(self.json_response.get("threeCrownWins"))

    @cached_property
    def challenge_cards_won(self) -> int:
        return int(self.json_response.get("challengeCardsWon"))

    @cached_property
    def challenge_max_win(self) -> int:
        return int(self.json_response.get("challengeMaxWin"))

    @cached_property
    def tournament_cards_won(self) -> int:
        return int(self.json_response.get("tournamentCardsWon"))

    @cached_property
    def tournament_battle_count(self) -> int:
        return int(self.json_response.get("tournamentBattleCount"))

    @cached_property
    def clan_role(self) -> str:
        return str(self.json_response.get("role"))

    @cached_property
    def clan_donations_currently(self) -> int:
        return int(self.json_response.get("donations"))

    @cached_property
    def clan_donations_received_currently(self) -> int:
        return int(self.json_response.get("donationsReceived"))

    @cached_property
    def clan_donations_total(self) -> int:
        return int(self.json_response.get("totalDonations"))

    @cached_property
    def war_day_wins_currently(self) -> int:
        return int(self.json_response.get("warDayWins"))

    @cached_property
    def clan_cards_collected(self) -> int:
        return int(self.json_response.get("clanCardsCollected"))

    @cached_property
    def clan_tag(self) -> str:
        return str(self.json_response.get("clan")["tag"])

    @cached_property
    def clan_name(self) -> str:
        return str(self.json_response.get("clan")["name"])

    @cached_property
    def clan_badge_id(self) -> int:
        return int(self.json_response.get("clan")["badgeId"])

    @cached_property
    def current_arena_id(self) -> int:
        return int(self.json_response.get("arena")["id"])

    @cached_property
    def current_arena_name(self) -> str:
        return str(self.json_response.get("arena")["name"])

    @cached_property
    def star_points(self) -> int:
        return int(self.json_response.get("starPoints"))

    @cached_property
    def exp_points(self) -> int:
        return int(self.json_response.get("expPoints"))

    @cached_property
    def total_exp_points(self) -> int:
        return int(self.json_response.get("totalExpPoints"))

    @cached_property
    def legacy_trophy_road_highscore(self) -> int:
        return int(self.json_response.get("legacyTrophyRoadHighscore"))

    def get_league_statistics(self) -> PlayerLeagueStatistics:
        return PlayerLeagueStatistics(stats=self.json_response.get("leagueStatistics"))

    def get_player_badges(self) -> Generator[PlayerBadge, None, None]:
        badge_data_raw = self.json_response.get("badges")
        for badge in badge_data_raw:
            yield PlayerBadge(badge)

    def get_player_achievements(self) -> Generator[PlayerAchievement, None, None]:
        achievement_data_raw = self.json_response.get("achievements")
        for achievement in achievement_data_raw:
            yield PlayerAchievement(achievement)

    def get_player_cards(self) -> Generator[PlayerCard, None, None]:
        player_cards_raw = self.json_response.get("cards")
        for card in player_cards_raw:
            yield PlayerCard(card)

    def get_player_support_cards(self) -> Generator[PlayerSupportCard, None, None]:
        player_support_cards_raw = self.json_response.get("supportCards")
        for support_card in player_support_cards_raw:
            yield PlayerSupportCard(support_card)

    def get_player_current_deck(self) -> Generator[PlayerCurrentDeck, None, None]:
        player_current_deck_raw = self.json_response.get("currentDeck")
        for current_deck in player_current_deck_raw:
            yield PlayerCurrentDeck(current_deck)

    def get_player_current_support_cards(self) -> Generator[PlayerCurrentSupportCard, None, None]:
        player_current_support_card_raw = self.json_response.get("currentDeckSupportCards")
        for support_card_raw in player_current_support_card_raw:
            yield PlayerCurrentSupportCard(support_card_raw)

    def get_player_current_favorite_card(self) -> Generator[PlayerCurrentFavouriteCard, None, None]:
        yield PlayerCurrentFavouriteCard(self.json_response.get("currentFavouriteCard"))

    def get_current_path_of_legend_season_result(self) -> dict:
        return dict(self.json_response.get("currentPathOfLegendSeasonResult"))

    def get_last_path_of_legend_season_result(self) -> dict:
        return dict(self.json_response.get("lastPathOfLegendSeasonResult"))

    def get_best_path_of_legend_season_result(self) -> dict:
        return dict(self.json_response.get("bestPathOfLegendSeasonResult"))

    def get_player_progress(self) -> dict:
        return dict(self.json_response.get("progress"))


class RoyaleAPI:
    def __init__(self, api_token: str, timeout=20, proxy=None, verify=True, ttl=None):
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Accept": "application/json"
        }
        self.client = httpx.Client(timeout=timeout, headers=self.headers, proxy=proxy, verify=verify)
        self.cache = APICache(ttl=ttl)

    def get_player(self, player_tag: str) -> Player:
        return Player(player_tag=player_tag, client=self.client, cache=self.cache)


if __name__ == "__main__":
    api = RoyaleAPI(api_token=test_token)
    player = api.get_player(player_tag="#2VVYYRVYP") # Yeah I am using my own token for testing, now u have it, have fun lmao
