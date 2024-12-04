from pathlib import Path

import pandas as pd

from fantasy.utils import PLAYER_VARIABLES


class DataReader:
    def __init__(self) -> None:
        self.data_dir = Path(__file__).parent / "data"
        self.manager_squad = self.read_csv("manager_squad.csv")
        self.automatic_subs = self.read_csv("automatic_subs.csv")
        self.player_info = self.read_csv("player_info.csv")
        self.manager_info = self.read_csv("manager_info.csv")
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
            .merge(self.player_info[["id", "web_name"]], left_on="element", right_on="id", how="left")
        )
