from collections.abc import Iterable
from enum import StrEnum

import httpx


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


def fetch_data() -> list[dict]:
    all_data = []
    manager_datas = fetch_league_manager_data(998)
    for manager_data in manager_datas:
        data = fetch_manager_history(manager_data["entry"])
        for entry in data["current"]:
            round_data = entry | {k: v for k, v in manager_data.items() if k in ["entry_name", "player_name"]}
            all_data.append(round_data)
    return all_data


def get_player_info() -> list[dict]:
    url = "https://fantasy.eliteserien.no/api/bootstrap-static/"
    with httpx.Client() as client:
        response = client.get(url)
        response.raise_for_status()
        data = response.json()
    return data["elements"]


def fetch_player_event_stats(player_ids: Iterable[int]) -> list[dict]:
    url = "https://fantasy.eliteserien.no/api/element-summary/{player_id}/"
    player_event_stats = []
    with httpx.Client() as client:
        for player_id in player_ids:
            response = client.get(url.format(player_id=player_id))
            response.raise_for_status()
            data = response.json()

            # Find the stats for the given event
            player_event_stats.extend(data["history"])
    return player_event_stats


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


def get_player_in_squad() -> [list[dict], list[dict]]:
    manager_data = fetch_league_manager_data(998)
    manager_squad, automatic_subs = [], []
    for manager in manager_data:
        for event in range(1, 31):
            player_in_squad, automatic_sub = fetch_manager_event_player_in_squad(manager["entry"], event)
            manager_squad.extend(player_in_squad)
            automatic_subs.extend(automatic_sub)
    return manager_squad, automatic_subs


def fetch_all_relevant_data() -> None:
    """Fetch relevant data an store to csv."""


if __name__ == "__main__":
    # data = fetch_data()
    # df = pd.DataFrame(data)
    # df.to_csv("manager_event_stats.csv")
    # manager_squad, automatic_subs = get_player_in_squad()
    # pd.DataFrame(manager_squad).to_csv("manager_squad.csv")
    # pd.DataFrame(automatic_subs).to_csv("automatic_subs.csv")
    # player_info = get_player_info()
    # player_stats = fetch_manager_event_player_in_squad(1716, 30)

    # manager_squad = pd.read_csv("data/manager_squad.csv", index_col=0)
    # unique_players = manager_squad["element"].unique()

    # player_event_stats = fetch_player_event_stats(unique_players)
    # pd.DataFrame(player_event_stats).to_csv("data/player_event_stats.csv")

    # player_info = get_player_info()
    # pd.DataFrame(player_info).to_csv("data/player_info.csv")

    # manager_info = fetch_league_manager_data(998)
    pass
