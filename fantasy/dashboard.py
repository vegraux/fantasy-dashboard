import dash
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output
from flask import Flask

from fantasy.data import DataReader
from fantasy.plots import (
    get_cumulative_sum_figure,
    get_figure,
    get_moment_figure,
    get_sum_figure,
    get_variable_by_player_per_manager,
)
from fantasy.utils import GROUPBY_VARIABLE, PLAYER_VARIABLES, VAR_MAP


def create_app(debug: bool = False) -> Flask:
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])
    data = DataReader()

    layout = html.Div(
        [
            dbc.Row(dbc.Col(html.H1(id="header", children="Drømmehagans fantasy"))),
            html.Br(),
            html.Br(),
            dbc.Row(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("Velg runder å se data for", className="card-title"),
                            dcc.RangeSlider(1, 30, 1, value=[1, 30], id="my-range-slider"),
                        ]
                    )
                )
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Col(html.H6("Velg variabel:", className="card-title")),
                                            dbc.Col(html.H6("Grupper data etter:", className="card-title")),
                                        ]
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                dcc.Dropdown(
                                                    id="player-variable-dropdown",
                                                    options=[
                                                        {"label": p, "value": v} for p, v in PLAYER_VARIABLES.items()
                                                    ],
                                                    value="total_points",
                                                )
                                            ),
                                            dbc.Col(
                                                dcc.Dropdown(
                                                    id="groupby-variable-dropdown",
                                                    options=[
                                                        {"label": p, "value": v} for p, v in GROUPBY_VARIABLE.items()
                                                    ],
                                                    value="web_name",
                                                )
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        )
                    ),
                ]
            ),
            dcc.Graph(id="var-per-player-fig"),
            dbc.Row(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6("Velg manager-variabel:", className="card-title"),
                                dcc.Dropdown(
                                    id="variable-dropdown",
                                    options=[{"label": pretty, "value": var} for pretty, var in VAR_MAP.items()],
                                    value="points",
                                ),
                            ]
                        ),
                    )
                ]
            ),
            html.Br(),
            dcc.Graph(id="sum-fig"),
            dcc.Graph(id="variable-fig"),
            dcc.Graph(id="cumulative-fig"),
            dcc.Graph(id="moment-fig"),
        ]
    )

    app.layout = dbc.Container(layout)

    @app.callback(
        Output("variable-fig", "figure"),
        [
            Input("variable-dropdown", "value"),
            Input("my-range-slider", "value"),
        ],
    )
    def update_round_figure(
        variable: str = "points",
        round_range: list[int] | tuple = (1, 30),
    ) -> go.Figure:
        return get_figure(data.manager_event_stats, variable, round_range[0], round_range[1])

    @app.callback(
        Output("sum-fig", "figure"),
        [
            Input("variable-dropdown", "value"),
            Input("my-range-slider", "value"),
        ],
    )
    def update_sum_figure(
        variable: str = "points",
        round_range: list[int] | tuple = (1, 30),
    ) -> go.Figure:
        return get_sum_figure(data.manager_event_stats, variable, round_range[0], round_range[1])

    @app.callback(
        Output("cumulative-fig", "figure"),
        [
            Input("variable-dropdown", "value"),
            Input("my-range-slider", "value"),
        ],
    )
    def update_moment_figure(
        variable: str = "points",
        round_range: list[int] | tuple = (1, 30),
    ) -> go.Figure:
        return get_cumulative_sum_figure(data.manager_event_stats, variable, round_range[0], round_range[1])

    @app.callback(
        Output("moment-fig", "figure"),
        [
            Input("variable-dropdown", "value"),
            Input("my-range-slider", "value"),
        ],
    )
    def update_cumulative_figure(
        variable: str = "points",
        round_range: list[int] | tuple = (1, 30),
    ) -> go.Figure:
        return get_moment_figure(data.manager_event_stats, variable, round_range[0], round_range[1])

    @app.callback(
        Output("var-per-player-fig", "figure"),
        [
            Input("groupby-variable-dropdown", "value"),
            Input("player-variable-dropdown", "value"),
            Input("my-range-slider", "value"),
        ],
    )
    def update_var_per_player_figure(
        groupby_variable: str = "web_name",
        variable: str = "total_points",
        round_range: list[int] | tuple = (1, 30),
    ) -> go.Figure:
        return get_variable_by_player_per_manager(
            data.data_per_player, variable, round_range[0], round_range[1], group_var=groupby_variable
        )

    if debug:
        app.run_server(port=8051)

    return app.server


if __name__ == "__main__":
    create_app(debug=True)
