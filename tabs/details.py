import pandas as pd
import plotly.express as px
from dash import html, dcc, Input, Output
from dash.exceptions import PreventUpdate

from overview_data import get_crypto_id_list
from util import get_data_from_API


def get_crypto_details(crypto_id) -> dict:
    url = 'https://api.coincap.io/v2/assets/' + crypto_id
    return get_data_from_API(url)


def generate_fig(df, crypto_id):
    return dcc.Graph(
        figure={
            "data": [
                {
                    "x": df['date'],
                    "y": df['priceUsd'],
                    "type": "line",
                    "marker": {"line": {"color": "white", "width": 1}},
                    "hoverinfo": "values",
                }
            ],
            "layout": {
                "title": "Price of " + crypto_id + " (1 day interval)",
                "margin": dict(l=50, r=20, t=80, b=50),
                "showlegend": False,
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "white"},
                "autosize": True,
            },
        },
    )


def get_display_df(crypto_id):
    interval = 'd1'
    url = 'https://api.coincap.io/v2/assets/' + \
        crypto_id + '/history?interval=' + interval
    data = get_data_from_API(url)
    df = pd.DataFrame(data)

    df['priceUsd'] = df['priceUsd'].astype('float')
    df['date'] = pd.to_datetime(df['date']).dt.tz_convert(None)
    return df


crypto_details_tab_content = [[
    html.Label(children='ID :'),
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


def details_callbacks(app):
    @app.callback(
        [Output(component_id='details-display', component_property='children'),
         Output(component_id='details-line-plot',
                component_property='children')

         ],
        [Input(component_id='details_crypto_id', component_property='value'),
         ], prevent_initial_call=True
    )
    def render_details(crypto_id):
        print('details_crypto_id', crypto_id)
        df = get_display_df(crypto_id)
        if crypto_id is None:
            raise PreventUpdate

        return [
            html.Table(
                [
                    html.Thead(
                        html.Tr([html.Th("Fields"), html.Th("Details")]))
                ] +
                [
                    html.Tbody(
                        [html.Tr([
                            html.Td(key),
                            html.Td(value)])for key, value in get_crypto_details(crypto_id).items()
                         ]
                    )]
            )
        ], [generate_fig(df, crypto_id)]
