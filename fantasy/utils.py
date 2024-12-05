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

ORIGINAL_PLAYER_VARIABLES = {
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

CALC_PLAYER_VARS = {
    "Poeng uten kapteiner": "original_total_points",
    "Poeng tjent på kapteiner": "total_points_captain_gain",
    "Poeng fra automatiske bytter": "points_from_automatic_subs",
}

PLAYER_VARIABLES = ORIGINAL_PLAYER_VARIABLES | CALC_PLAYER_VARS

REVERSE_PLAYER_VARIABLES = {v: k for k, v in PLAYER_VARIABLES.items()}

GROUPBY_VARIABLE = {
    "Spiller": "web_name",
    "Posisjon på banen": "field_position",
    "Lag": "name",
    "Ingen gruppering": None,
}
REVERSE_GROUPBY_VARIABLE = {v: k for k, v in GROUPBY_VARIABLE.items()}
