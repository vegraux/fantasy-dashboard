import pathlib

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output
from flask import Flask

from fantasy.plots import get_cumulative_sum_figure, get_figure, get_moment_figure, get_sum_figure
from fantasy.utils import VAR_MAP


def create_app(debug: bool = False) -> Flask:
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])
    data = pd.read_csv(pathlib.Path(__file__).parent / "data.csv", index_col=0)

    layout = html.Div(
        [
            dbc.Row(dbc.Col(html.H1(id="header", children="Drømmehagans fantasy"))),
            html.Br(),
            html.Br(),
            dbc.Row(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5("Velg runder å se data for", className="card-title"),
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
                                    html.H5("Velg variabel", className="card-title"),
                                    dcc.Dropdown(
                                        id="variable-dropdown",
                                        options=[{"label": pretty, "value": var} for pretty, var in VAR_MAP.items()],
                                        placeholder="Chose variable",
                                        value="points",
                                    ),
                                ]
                            ),
                        )
                    ),
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
        return get_figure(data, variable, round_range[0], round_range[1])

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
        return get_sum_figure(data, variable, round_range[0], round_range[1])

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
        return get_cumulative_sum_figure(data, variable, round_range[0], round_range[1])

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
        return get_moment_figure(data, variable, round_range[0], round_range[1])

    if debug:
        app.run_server(port=8051)

    return app.server


if __name__ == "__main__":
    app = create_app(debug=True)
