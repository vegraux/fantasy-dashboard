import time
from enum import StrEnum
from pathlib import Path

import httpx
import pandas as pd

transport = httpx.HTTPTransport(retries=3)


class API(StrEnum):
    BASE_API = "https://fantasy.eliteserien.no/api"
    MANAGER_HISTORY = f"{BASE_API}/entry/{{manager_id}}/history/"


def fetch_league_manager_data(league_id: int) -> list[dict]:
    url = f"https://fantasy.eliteserien.no/api/leagues-classic/{league_id}/standings/"
    with httpx.Client() as client:
        response = client.get(url)
        response.raise_for_status()
        data = response.json()
        return data["standings"]["results"]


def fetch_manager_history(manager_id: int) -> list[dict]:
    url = API.MANAGER_HISTORY.format(manager_id=manager_id)
    with httpx.Client() as client:
        response = client.get(url)
        response.raise_for_status()
        return response.json()


def get_player_and_team_info() -> [list[dict], list[dict]]:
    url = "https://fantasy.eliteserien.no/api/bootstrap-static/"
    with httpx.Client() as client:
        response = client.get(url)
        response.raise_for_status()
        data = response.json()
    return data["elements"], data["teams"]


def fetch_manager_event_player_in_squad(manager_id: int, event_id: int) -> [list[dict], list[dict]]:
    url = f"https://fantasy.eliteserien.no/api/entry/{manager_id}/event/{event_id}/picks/"
    with httpx.Client() as client:
        response = client.get(url)
        response.raise_for_status()
        data = response.json()

        for pick in data["picks"]:
            pick["manager_id"] = manager_id
            pick["event_id"] = event_id
        return data["picks"], data["automatic_subs"]


class FetchData:
    def __init__(self, league_id: int = 1350, year: int = 2025) -> None:
        self.league_id = league_id
        self.data_dir = Path(__file__).parent / "data" / f"{year}"
        self.managers = fetch_league_manager_data(league_id)
        self.manager_event_stats = self.fetch_manager_event_stats_data()
        self.player_info, self.team_info = get_player_and_team_info()
        self.manager_squad, self.automatic_subs = self.get_player_in_squad()
        self.player_event_stats = self.fetch_player_event_stats()

    def save_data(self) -> None:
        """Save data to csv files."""
        pd.DataFrame(self.managers).to_csv(self.data_dir / "manager_info.csv")
        pd.DataFrame(self.manager_event_stats).to_csv(self.data_dir / "manager_event_stats.csv")
        pd.DataFrame(self.player_info).to_csv(self.data_dir / "player_info.csv")
        pd.DataFrame(self.team_info).to_csv(self.data_dir / "team_info.csv")
        pd.DataFrame(self.player_event_stats).to_csv(self.data_dir / "player_event_stats.csv")
        pd.DataFrame(self.manager_squad).to_csv(self.data_dir / "manager_squad.csv")
        pd.DataFrame(self.automatic_subs).to_csv(self.data_dir / "automatic_subs.csv")

    def fetch_manager_event_stats_data(self) -> list[dict]:
        all_data = []
        for manager_data in self.managers:
            data = fetch_manager_history(manager_data["entry"])
            for entry in data["current"]:
                round_data = entry | {k: v for k, v in manager_data.items() if k in ["entry_name", "player_name"]}
                all_data.append(round_data)
        return all_data

    def fetch_player_event_stats(self) -> list[dict]:
        url = "https://fantasy.eliteserien.no/api/element-summary/{player_id}/"
        player_event_stats = []
        with httpx.Client(transport=transport) as client:
            for player_id in self.unique_players:
                time.sleep(0.5)
                response = client.get(url.format(player_id=player_id))
                response.raise_for_status()
                data = response.json()

                # Find the stats for the given event
                player_event_stats.extend(data["history"])
        return player_event_stats

    def get_player_in_squad(self) -> [list[dict], list[dict]]:
        manager_squad, automatic_subs = [], []
        for manager in self.managers:
            for event in range(1, self.played_rounds + 1):
                player_in_squad, automatic_sub = fetch_manager_event_player_in_squad(manager["entry"], event)
                manager_squad.extend(player_in_squad)
                automatic_subs.extend(automatic_sub)
        return manager_squad, automatic_subs

    @property
    def unique_players(self) -> set[int]:
        return {player["element"] for player in self.manager_squad}

    @property
    def played_rounds(self) -> int:
        return max(self.manager_event_stats, key=lambda x: x["event"])["event"]


if __name__ == "__main__":
    fetcher = FetchData()
    fetcher.save_data()
