# -*- coding: utf-8 -*-
"""
Created on Mon May  6 12:27:40 2024

@author: aforozco
"""
# app.py

import pandas as pd
from dash import Dash, Input, Output, dcc, html
import dash_bootstrap_components as dbc

data = (
    pd.read_csv("avocado.csv")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
    .sort_values(by="Date")
)
regions = data["region"].sort_values().unique()
avocado_types = data["type"].sort_values().unique()

external_stylesheets = [dbc.themes.CYBORG]
#app = Dash(__name__, external_stylesheets=external_stylesheets)

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Avocado Analytics: Understand Your Avocados!"

app.layout = dbc.Container([
    dbc.Row([
        html.P("🥑", className="header-emoji")
    ]),
    dbc.Row([
        html.H1("Avocado Analytics",className="text-primary text-center fs-3")
    ]),
    dbc.Row([
        html.P("Analyze the behavior of avocado prices and the number",
              className="header-description")
    ]),
    dbc.Row([
        html.P("of avocados sold in the US between 2015 and 2018",
              className="header-description")
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Row([
            html.Div(children="Region", className="menu-title")
            ]),
            dbc.Row([
            dcc.Dropdown(
                id="region-filter",
                options=[
                    {"label": region, "value": region}
                    for region in regions
                ],
                value="Albany",
                clearable=False,
                className="dropdown",
            )
            ]),
        ], width=3),

        dbc.Col([
            dbc.Row([
            html.Div(children="Type", className="menu-title")
            ]),
            dbc.Row([
            dcc.Dropdown(
                id="type-filter",
                options=[
                    {
                        "label": avocado_type.title(),
                        "value": avocado_type,
                    }
                    for avocado_type in avocado_types
                ],
                value="organic",
                clearable=False,
                searchable=False,
                className="dropdown",
            ),
            ])
        ], width=3),
        dbc.Col([
            dbc.Row([
            html.Div(
                children="Date Range", className="menu-title"
            ),
            ]),
            dbc.Row([
            dcc.DatePickerRange(
                id="date-range",
                min_date_allowed=data["Date"].min().date(),
                max_date_allowed=data["Date"].max().date(),
                start_date=data["Date"].min().date(),
                end_date=data["Date"].max().date(),
            ),
            ])
        ], width=3),
    ]),
    dbc.Row([
        html.Div(
            children=dcc.Graph(
                id="price-chart",
                config={"displayModeBar": False},
            ),
            className="card",
        ),
    ]),
    dbc.Row([
       html.Div(
           children=dcc.Graph(
               id="volume-chart",
               config={"displayModeBar": False},
           ),
           className="card",
       ),
    ]),
], fluid=True) 
    


@app.callback(
    Output("price-chart", "figure"),
    Output("volume-chart", "figure"),
    Input("region-filter", "value"),
    Input("type-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_charts(region, avocado_type, start_date, end_date):
    filtered_data = data.query(
        "region == @region and type == @avocado_type"
        " and Date >= @start_date and Date <= @end_date"
    )
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["AveragePrice"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Average Price of Avocados",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Total Volume"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Avocados Sold", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return price_chart_figure, volume_chart_figure

if __name__ == "__main__":
    app.run(debug=True)