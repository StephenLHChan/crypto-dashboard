from datetime import datetime
import pandas as pd
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc

from util import get_data_from_API
from overview_data import get_exchangeId_list, get_crypto_id_list


def convertToDaysInWeek(timestamp: int) -> str:
    conversion = {
        0: 'Mon',
        1: 'Tue',
        2: 'Wed',
        3: 'Thu',
        4: 'Fri',
        5: 'Sat',
        6: 'Sun',
    }
    return conversion[datetime.fromtimestamp(timestamp / 1000).weekday()]


def get_fig(df):
    fig = px.bar(
        df,
        x='daysInWeek',
        y='volume',
        title='Volume in Days in Week',
    )
    return fig


def get_display_df(base_id, quote_id):
    data = []
    for exchangeId in get_exchangeId_list(base_id, quote_id):
        url = 'https://api.coincap.io/v2/candles?exchange=' + exchangeId + \
            '&interval=' + 'd1' + '&baseId=' + base_id + '&quoteId=' + quote_id
        data.extend(get_data_from_API(url))

    df = pd.DataFrame(data)
    df['period'] = df['period'].astype('int')
    df['volume'] = df['volume'].astype('float')
    df['daysInWeek'] = df['period'].apply(convertToDaysInWeek)

    return df.groupby(by='daysInWeek', as_index=False).sum().sort_values(by='volume')


def get_volume_fig(base_id, quote_id):
    return get_fig(get_display_df(base_id, quote_id))


volume_daysInWeek_tab_content = [[
    dbc.Label('Base ID :'),
    dcc.Dropdown(
        id='volume_daysInWeek-base-id',
        options=[
            {'label': id, 'value': id} for id in get_crypto_id_list()
        ],
    ),
    dbc.Label('Quote ID :'),
    dcc.Dropdown(
        id='volume_daysInWeek-quote-id',
        options=[
            {'label': id, 'value': id} for id in get_crypto_id_list()
        ],
    ),
    html.Div(
        children=[
            html.Div(children=[],
                     id='volume_daysInWeek-plot', className="p-4"),
        ],
    ),
]]
