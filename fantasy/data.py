from pathlib import Path

import pandas as pd

from fantasy.utils import PLAYER_VARIABLES

POSITION_MAP = {1: "Keeper", 2: "Forsvar", 3: "Midtbane", 4: "Angrep"}


class DataReader:
    def __init__(self) -> None:
        self.data_dir = Path(__file__).parent / "data"
        self.manager_squad = self.read_csv("manager_squad.csv")
        self.automatic_subs = self.read_csv("automatic_subs.csv")
        self.player_info = self.read_csv("player_info.csv")
        self.manager_info = self.read_csv("manager_info.csv")
        self.team_info = self.read_csv("team_info.csv")
        self.player_event_stats = self.read_csv("player_event_stats.csv")
        self.manager_event_stats = self.read_csv("manager_event_stats.csv")
        self.data_per_player = self.merge_manager_squad_with_player_stats()

    def read_csv(self, filename: str) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / filename, index_col=0)

    def merge_manager_squad_with_player_stats(self) -> pd.DataFrame:
        player_cols = list(PLAYER_VARIABLES.values())
        player_event = self.player_event_stats.groupby(["element", "round"])[player_cols].sum().reset_index()
        return (
            self.manager_squad.merge(
                player_event, left_on=["element", "event_id"], right_on=["element", "round"], how="left", validate="m:1"
            )
            .merge(self.manager_info, left_on="manager_id", right_on="entry", how="left")
            .merge(
                self.player_info.assign(field_position=self.player_info["element_type"].map(POSITION_MAP))[
                    ["id", "web_name", "field_position", "team"]
                ],
                left_on="element",
                right_on="id",
                how="left",
            )
            .merge(self.team_info, left_on="team", right_on="id", how="left")
        )
