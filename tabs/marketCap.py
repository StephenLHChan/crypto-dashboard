import pandas as pd
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc

from overview_data import get_overview_data, get_rank_list


def get_fig(df):
    marketCap_pie_fig = px.pie(
        df,
        values='marketCapUsd',
        names='name',
        title='Market Cap',
    )
    return marketCap_pie_fig


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
    return pd.concat(frames)


def get_marketCap_pie(num_of_record):
    data = get_overview_data().filter(['name', 'rank', 'marketCapUsd'])
    return get_fig(get_display_df(data, num_of_record))


def get_marketCap_details(num_of_record: int):
    data = get_overview_data().filter(['rank', 'name', 'marketCapUsd'])
    return get_display_df(data, num_of_record)


marketCap_tab_content = [[
    dbc.Label("Number of Records :"),
    dcc.Dropdown(
        id='num_Of_Record',
        options=[
            {'label': rank, 'value': rank} for rank in get_rank_list()
        ],
    ),
    html.Div(
        children=[
            html.Div(children=[],
                     id='marketCap-pie-plot', className="p-4"),
            html.Div(children=[],
                     id='marketCap-detail', className="p-4")
        ],
    ),
]]
