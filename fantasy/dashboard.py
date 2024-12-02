import pathlib

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output
from flask import Flask


def create_app(debug) -> Flask:

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])
    data = pd.read_csv(pathlib.Path(__file__).parent / "data.csv", index_col=0)

    var_map = {
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
    reverse_var_map = {v: k for k, v in var_map.items()}

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
                            dcc.RangeSlider(0, 30, 1, value=[0, 30], id="my-range-slider"),
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
                                        options=[{"label": pretty, "value": var} for pretty, var in var_map.items()],
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
            dcc.Graph(id="moment-fig"),
        ]
    )

    app.layout = dbc.Container(layout)


    def get_figure(variable: str, round_start: int = 1, round_end: int = 30) -> go.Figure:
        plot_data = data[(data["event"] >= round_start) & (data["event"] <= round_end)]
        fig = px.line(
            plot_data,
            x="event",
            y=variable,
            color="player_name",
            title=f"{reverse_var_map[variable]} fra {round_start} til {round_end}",
        )
        return fig


    def get_sum_figure(variable: str, round_start: int = 1, round_end: int = 30) -> go.Figure:
        plot_data = data[(data["event"] >= round_start) & (data["event"] <= round_end)]
        summed_data = plot_data.groupby("player_name")[variable].sum().sort_values(ascending=False)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=summed_data.index, y=summed_data))
        fig.update_layout(title=f"Sum av {reverse_var_map[variable]} fra runde {round_start} til runde {round_end}")
        return fig


    def get_moment_figure(variable: str, round_start: int = 1, round_end: int = 30) -> go.Figure:
        momentum = data.sort_values(by=["player_name", "event"])
        momentum[variable] = momentum.groupby("player_name")[variable].rolling(4, min_periods=1).mean().values
        plot_data = momentum[(momentum["event"] >= round_start) & (momentum["event"] <= round_end)]
        fig = px.line(
            plot_data,
            x="event",
            y=variable,
            color="player_name",
            title=f"Momentum: Gjennomsnittlig verdi for {reverse_var_map[variable]} de siste 4 kamper",
        )
        return fig


    @app.callback(
        Output("variable-fig", "figure"),
        [
            Input("variable-dropdown", "value"),
            Input("my-range-slider", "value"),
        ],
    )
    def update_round_figure(
        variable: str = "points",
        round_range: list[int] | tuple = (0, 30),
    ) -> go.Figure:
        return get_figure(variable, round_range[0], round_range[1])


    @app.callback(
        Output("sum-fig", "figure"),
        [
            Input("variable-dropdown", "value"),
            Input("my-range-slider", "value"),
        ],
    )
    def update_sum_figure(
        variable: str = "points",
        round_range: list[int] | tuple = (0, 30),
    ) -> go.Figure:
        return get_sum_figure(variable, round_range[0], round_range[1])


    @app.callback(
        Output("moment-fig", "figure"),
        [
            Input("variable-dropdown", "value"),
            Input("my-range-slider", "value"),
        ],
    )
    def update_moment_figure(
        variable: str = "points",
        round_range: list[int] | tuple = (0, 30),
    ) -> go.Figure:
        return get_moment_figure(variable, round_range[0], round_range[1])
    if debug:
        app.run_server(port=8051)

    return app.server


if __name__ == "__main__":
    app = create_app(debug=True)
