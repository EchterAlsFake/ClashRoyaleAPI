"""
ClashRoyaleAPI Copyright (C) 2025 Johannes Habel <EchterAlsFake@proton.me>
Licensed under the General Public License v3, see LICENSE for details
"""

import httpx

from modules.errors import *
from functools import cached_property

test_token = "nothing in here lmao fuck off scrapers ahahahaha"

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

class PlayerBadges:
    def __init__(self, badges: dict):
        self.badges = badges

class Player:
    def __init__(self, player_tag: str, api_token: str):
        self.player_tag = str(player_tag).replace("#", "%23")
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Accept": "application/json"
        }
        self.client = httpx.Client(timeout=20, headers=self.headers)
        response = self.client.get(url=f"https://api.clashroyale.com/v1/players/{self.player_tag}")

        if response.status_code == 200:
            self.json_response: dict = response.json()

        elif response.status_code == 403:
            raise InvalidAPIToken(f"Token: {self.api_token} is invalid, or you've been completely blocked. Make sure to"
                                  f"whitelist your IP address on the Clash Royale API Dashboard!")

        elif response.status_code == 429:
            raise RateLimitExceeded(f"Ratelimit for: {self.api_token} has been exceeded, please try again later.")

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

    def get_league_statistics(self) -> PlayerLeagueStatistics:
        return PlayerLeagueStatistics(stats=self.json_response.get("leagueStatistics"))

class RoyaleAPI:
    def __init__(self, api_token: str):
        self.api_token = api_token


    def get_player(self, player_tag: str) -> Player:
        return Player(player_tag, self.api_token)


if __name__ == "__main__":
    api = RoyaleAPI(api_token=test_token)
    api.get_player(player_tag="#2VVYYRVYP") # Yeah I am using my own token for testing, now u have it, have fun lmao