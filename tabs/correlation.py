import pandas as pd
from dash import html, dcc
import plotly.express as px
import dash_bootstrap_components as dbc

from overview_data import get_exchangeId_list, get_crypto_id_list
from tabs.candlestick import get_candlestick_interval
from util import get_data_from_API


def get_correlation_fig(base_id, quote_id, interval):
    data = []
    for exchangeId in get_exchangeId_list(base_id, quote_id):
        url = 'https://api.coincap.io/v2/candles?exchange=' + exchangeId + \
            '&interval=' + interval + '&baseId=' + base_id + '&quoteId=' + quote_id
        data.extend(get_data_from_API(url))

    df = pd.DataFrame(data)

    df['open'] = df['open'].astype('float')
    df['high'] = df['high'].astype('float')
    df['low'] = df['low'].astype('float')
    df['close'] = df['close'].astype('float')
    df['volume'] = df['volume'].astype('float')
    df['period'] = df['period'].astype('int')

    df = df.groupby(by='period', as_index=False).sum()

    df['percentage_change'] = abs(df['close'] - df['open']) / df['open']

    fig = px.scatter(
        df,
        x='volume',
        y='percentage_change'
    )
    return fig


correlation_price_change_volume_tab_cantent = [[
    dbc.Label('Base ID :'),
    dcc.Dropdown(
        id='correlation-base-id',
        options=[
            {'label': id, 'value': id} for id in get_crypto_id_list()
        ],
    ),
    dbc.Label('Quote ID :'),
    dcc.Dropdown(
        id='correlation-quote-id',
        options=[
            {'label': id, 'value': id} for id in get_crypto_id_list()
        ],
    ),
    dbc.Label('Interval :'),
    dcc.Dropdown(
        id='correlation-interval',
        options=[
            {'label': key, 'value': value} for key, value in get_candlestick_interval().items()
        ],
    ),
    html.Div(
        children=[
            html.Div(children=[],
                     id='correlation-plot')
        ],

    )
]]
