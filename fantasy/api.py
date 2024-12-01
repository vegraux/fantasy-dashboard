from enum import StrEnum

import httpx


class API(StrEnum):
    BASE_API = "https://fantasy.eliteserien.no/api"
    MANAGER_HISTORY = f"{BASE_API}/entry/{{manager_id}}/history/"


def fetch_league_manager_data(league_id: int) -> list[int]:
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


if __name__ == "__main__":
    import pandas as pd

    data = fetch_data()
    df = pd.DataFrame(data)
    df.to_csv("data.csv")
