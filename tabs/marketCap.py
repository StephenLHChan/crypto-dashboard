import pandas as pd
import plotly.express as px
from dash import html, dcc, Input, Output, dash_table
from dash.exceptions import PreventUpdate

from overview_data import get_overview_data, get_rank_list


def generate_pie(df):
    return dcc.Graph(
        figure={
            "data": [
                {
                    "labels": df['name'],
                    "values": df['marketCapUsd'],
                    "type": "pie",
                    "marker": {"line": {"color": "white", "width": 1}},
                    "hoverinfo": "values",
                }
            ],
            "layout": {
                "title": "Market Capacity Distribution of Cryptocurrency",
                "margin": dict(l=20, r=20, t=80, b=20),
                "showlegend": True,
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "white"},
                "autosize": True,
            },
        },
    )


def generate_table(df):
    return html.Table(
        [
            html.Thead(
                html.Tr([html.Th("Rank"), html.Th("Name"), html.Th("Market Cap in USD")]))
        ] +
        [
            html.Tbody(
                [html.Tr([
                    html.Td(df.iloc[i][col]) for col in df.columns
                ]) for i in range(len(df))]
            )]
    )


def get_display_df(df, num_Of_Record):
    df_minority = df.drop(
        index=df[df['rank'] < num_Of_Record].index)

    df_others = pd.DataFrame(
        {
            'name': 'Others',
            'rank': num_Of_Record + 1,
            'marketCapUsd': df_minority['marketCapUsd'].sum()
        },
        index=[num_Of_Record]
    )

    frames = [
        df.drop(index=df[df['rank'] > num_Of_Record].index),
        df_others
    ]
    return pd.concat(frames)[['rank', 'name', 'marketCapUsd']]


def get_marketCap_data():
    return get_overview_data().filter(['name', 'rank', 'marketCapUsd'])


marketCap_tab_content = [[
    html.Label("Number of Records :"),
    dcc.Dropdown(
        id='num_Of_Record',
        options=[
            {'label': rank, 'value': rank} for rank in get_rank_list()
        ],
    ),
    html.Div(
        children=[
            html.Div(children=[],
                     id='marketCap-pie-plot'),
            html.Div(children=[],
                     id='marketCap-detail')
        ],
    ),
]]


def marketCap_callbacks(app):
    @ app.callback(
        [Output(component_id='marketCap-pie-plot', component_property='children'),
         Output(component_id='marketCap-detail', component_property='children')
         ],
        [Input(component_id='num_Of_Record', component_property='value'),
         ], prevent_initial_call=True
    )
    def render_marketCap_fig(num_Of_Record):
        print('num_Of_Record', num_Of_Record)
        if num_Of_Record is None:
            raise PreventUpdate
        data_all = get_marketCap_data()
        data_display = get_display_df(data_all, num_Of_Record)
        return [generate_pie(data_display)], generate_table(data_display)
