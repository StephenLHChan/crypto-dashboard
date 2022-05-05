import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc
import dash_bootstrap_components as dbc

from overview_data import get_crypto_id_list
from util import get_data_from_API, get_local_time

INTERVALS_CANDLESTICK = {
    '1 min': 'm1',
    '5 min': 'm5',
    '15 min': 'm15',
    '30 min': 'm30',
    '1 hr': 'h1',
    '2 hr': 'h2',
    '4 hr': 'h4',
    '8 hr': 'h8',
    '12 hr': 'h12',
    '1 day': 'd1',
    '1 week': 'w1'
}

EXCHANGEID = 'binance'


def get_candlestick_fig(base_id, quote_id, interval):
    url = 'https://api.coincap.io/v2/candles?exchange=' + EXCHANGEID + \
        '&interval=' + interval + '&baseId=' + base_id + '&quoteId=' + quote_id
    data = get_data_from_API(url)

    df = pd.DataFrame(data)

    df['period'] = df['period'].apply(get_local_time)
    fig = go.Figure(data=[go.Candlestick(
        x=df['period'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
    )])

    fig.update_layout(
        title='Candlestick Figure of ' + base_id + '/' + quote_id,
        yaxis_title='Price in USD',
    )

    return fig


def get_candlestick_interval():
    return INTERVALS_CANDLESTICK


candlestick_tab_content = [[
    dbc.Label('Base ID :'),
    dcc.Dropdown(
        id='candlestick-base-id',
        options=[
            {'label': id, 'value': id} for id in get_crypto_id_list()
        ],
    ),
    dbc.Label('Quote ID :'),
    dcc.Dropdown(
        id='candlestick-quote-id',
        options=[
            {'label': id, 'value': id} for id in get_crypto_id_list()
        ],
    ),
    dbc.Label('Interval :'),
    dcc.Dropdown(
        id='candlestick-interval',
        options=[
            {'label': key, 'value': value} for key, value in get_candlestick_interval().items()
        ],
    ),
    html.Div(
        children=[
            html.Div(children=[],
                     id='candlestick-plot')
        ],

    )
]]
