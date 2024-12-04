VAR_MAP = {
    "Runde": "event",
    "Rundepoeng": "points",
    "Total poeng": "total_points",
    "Runderangering": "rank",
    "Total rangering": "overall_rank",
    "Penger på bok": "bank",
    "Lagverdi": "value",
    "Bytter": "event_transfers",
    "Byttekostnad": "event_transfers_cost",
    "Poeng på benken": "points_on_bench",
}
REVERSE_VAR_MAP = {v: k for k, v in VAR_MAP.items()}

PLAYER_VARIABLES = {
    "Assists": "assists",
    "Mål": "goals_scored",
    "Poeng": "total_points",
    "Bonus": "bonus",
    "Minutter": "minutes",
    "Rent bur": "clean_sheets",
    "Gule kort": "yellow_cards",
    "Røde kort": "red_cards",
    "Selvmål": "own_goals",
    "Straffer reddet": "penalties_saved",
    "Straffebom": "penalties_missed",
    "Redninger": "saves",
}


REVERSE_PLAYER_VARIABLES = {v: k for k, v in PLAYER_VARIABLES.items()}
