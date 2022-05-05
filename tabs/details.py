import pandas as pd
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc

from overview_data import get_crypto_id_list
from util import get_data_from_API


def get_crypto_details(crypto_id) -> dict:
    url = 'https://api.coincap.io/v2/assets/' + crypto_id
    return get_data_from_API(url)


def get_fig(df):
    fig = px.line(
        df,
        x='date',
        y='priceUsd',
        title=''
    )
    return fig


def get_display_df(crypto_id):
    interval = 'd1'
    url = 'https://api.coincap.io/v2/assets/' + \
        crypto_id + '/history?interval=' + interval
    data = get_data_from_API(url)
    df = pd.DataFrame(data)

    df['priceUsd'] = df['priceUsd'].astype('float')
    df['date'] = pd.to_datetime(df['date']).dt.tz_convert(None)
    return df


def get_details_line_fig(crypto_id):
    return get_fig(get_display_df(crypto_id))


crypto_details_tab_content = [[
    dbc.Label('ID :'),
    dcc.Dropdown(
        id='details_crypto_id',
        options=[
            {'label': id, 'value': id} for id in get_crypto_id_list()
        ],
    ),
    html.Div(
        children=[
            html.Div(children=[],
                     id='details-line-plot'),
            html.Div(children=[],
                     id='details-display', className="p-4"),
        ],
    ),
]]
