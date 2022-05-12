import pandas as pd
import plotly.express as px
from dash import html, dcc, Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from overview_data import get_overview_data, get_rank_list


def get_fig(df):
    return px.pie(
        df,
        values='marketCapUsd',
        names='name',
        title='Market Cap',
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

        return [dcc.Graph(figure=get_marketCap_pie(num_Of_Record))], dbc.Table.from_dataframe(get_marketCap_details(num_Of_Record), striped=True, bordered=True, hover=True)
