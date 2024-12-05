import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

from fantasy.utils import REVERSE_PLAYER_VARIABLES, REVERSE_VAR_MAP


def get_sum_figure(data: pd.DataFrame, variable: str, round_start: int = 1, round_end: int = 30) -> go.Figure:
    plot_data = data[(data["event"] >= round_start) & (data["event"] <= round_end)]
    summed_data = plot_data.groupby("player_name")[variable].sum().sort_values(ascending=False)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=summed_data.index, y=summed_data))
    fig.update_layout(title=f"Sum av {REVERSE_VAR_MAP[variable]} fra runde {round_start} til runde {round_end}")
    return fig


def get_moment_figure(data: pd.DataFrame, variable: str, round_start: int = 1, round_end: int = 30) -> go.Figure:
    momentum = data.sort_values(by=["player_name", "event"])
    momentum[variable] = momentum.groupby("player_name")[variable].rolling(4, min_periods=1).mean().values
    plot_data = momentum[(momentum["event"] >= round_start) & (momentum["event"] <= round_end)]
    fig = px.line(
        plot_data,
        x="event",
        y=variable,
        color="player_name",
        title=f"Momentum: Gjennomsnittlig verdi for {REVERSE_VAR_MAP[variable]} de siste 4 rundene",
    )
    return fig


def get_cumulative_sum_figure(
    data: pd.DataFrame, variable: str, round_start: int = 1, round_end: int = 30
) -> go.Figure:
    cumulative = data.sort_values(by=["player_name", "event"])
    cumulative[variable] = cumulative.groupby("player_name")[variable].cumsum()
    plot_data = cumulative[(cumulative["event"] >= round_start) & (cumulative["event"] <= round_end)]
    fig = px.line(
        plot_data,
        x="event",
        y=variable,
        color="player_name",
        title=f"Samlet sum så langt i sesongen for {REVERSE_VAR_MAP[variable]}",
    )
    return fig


def get_figure(data: pd.DataFrame, variable: str, round_start: int = 1, round_end: int = 30) -> go.Figure:
    plot_data = data[(data["event"] >= round_start) & (data["event"] <= round_end)]
    fig = px.line(
        plot_data,
        x="event",
        y=variable,
        color="player_name",
        title=f"{REVERSE_VAR_MAP[variable]} fra runde {round_start} til runde {round_end}",
    )
    return fig


def get_variable_by_player_per_manager(
    data: pd.DataFrame,
    variable: str,
    round_start: int = 1,
    round_end: int = 30,
    only_active_players: bool = True,
    group_var: str = "field_position",  # web_name
) -> go.Figure:
    data = data.copy()

    data = data.query(f"event_id >= {round_start} and event_id <= {round_end}")

    if only_active_players:
        data = data.query("multiplier > 0")

    if variable == "points_from_automatic_subs":
        data = data.query("automatic_sub")
        variable = "total_points"

    points_per_player = data.groupby(["player_name", group_var])[variable].sum().reset_index()
    zeros = [player for player, b in (points_per_player.groupby(group_var)[variable].sum() == 0).items() if b]
    points_per_player = points_per_player[~points_per_player[group_var].isin(zeros)]

    manager_ordering = points_per_player.groupby("player_name")[variable].sum().sort_values(ascending=False).index

    points_per_player = points_per_player.sort_values(by=["player_name", variable], ascending=False)
    fig = px.bar(
        points_per_player,
        x="player_name",
        y=variable,
        color=group_var,
        title=f"{REVERSE_PLAYER_VARIABLES[variable]} fra runde {round_start} til runde {round_end}",
        category_orders={"player_name": manager_ordering},
    )
    fig.update_layout(height=800)

    return fig
