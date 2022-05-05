import pandas as pd
import dash
from dash import html, dcc, Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc


from tabs.candlestick import get_candlestick_fig, candlestick_tab_content
from tabs.marketCap import get_marketCap_pie, get_marketCap_details, marketCap_tab_content
from tabs.details import get_crypto_details, get_details_line_fig, crypto_details_tab_content
from tabs.volumn import get_volume_fig, volume_daysInWeek_tab_content
from tabs.correlation import get_correlation_fig, correlation_price_change_volume_tab_cantent


app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB, dbc.icons.BOOTSTRAP],
                suppress_callback_exceptions=True)
server = app.server

app.title = "Crypto Dashboard"

app.layout = dbc.Container(html.Div(
    children=[
        html.H1('Crypto Dashboard',
                className="display-4"
                ),
        html.Hr(),

        dbc.Tabs(
            [
                dbc.Tab(label="Market Cap Overview", tab_id="market-cap"),
                dbc.Tab(label="Crypto Details", tab_id="crypto-details"),
                dbc.Tab(label="Candlestick Chart", tab_id="candlestick"),
                dbc.Tab(label="Volume of days in week",
                        tab_id="volume-daysInWeek"),
                dbc.Tab(label="Correlation between Price change and Volume",
                        tab_id="correlation-price_change-volume")
            ],
            id="tabs",
            active_tab="market-cap",
        ),
        dcc.Loading(
            children=[
                html.Div(id="tab-content", className="p-4 d-flex flex-column min-vh-100")]
        ),
        html.Footer(
            children=[
                html.Section(
                    children=[
                        html.Div(
                            'Get connected with me on social networks:', className="me-5 d-none d-lg-block"
                        ),
                        html.Div(
                            [
                                html.A(
                                    html.I(className='bi bi-github'),
                                    href='https://github.com/StephenLHChan',
                                    className="me-4 text-reset"
                                ),
                                html.A(
                                    html.I(className='bi bi-linkedin'),
                                    href='https://www.linkedin.com/in/stephenlhc',
                                    className="me-4 text-reset"
                                )
                            ], className="me-5 d-none d-lg-block"
                        )
                    ], className="d-flex justify-content-center justify-content-lg-between p-4 border-bottom"
                )
            ], className="text-center text-lg-start bg-light text-muted mt-auto")
    ])
)


@app.callback(
    [Output("tab-content", "children"),
     ],
    [Input("tabs", "active_tab"),
     ]
)
def render_tab_content(active_tab):
    if active_tab is not None:
        if active_tab == "market-cap":
            return marketCap_tab_content
        elif active_tab == "candlestick":
            return candlestick_tab_content
        elif active_tab == "crypto-details":
            return crypto_details_tab_content
        elif active_tab == "volume-daysInWeek":
            return volume_daysInWeek_tab_content
        elif active_tab == "correlation-price_change-volume":
            return correlation_price_change_volume_tab_cantent
    return "No tab selected"


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


@ app.callback(
    [Output(component_id='candlestick-plot', component_property='children'),
     ],
    [Input(component_id='candlestick-base-id', component_property='value'),
     Input(component_id='candlestick-quote-id', component_property='value'),
     Input(component_id='candlestick-interval', component_property='value'),
     ], prevent_initial_call=True
)
def render_candlestick_fig(base_id, quote_id, interval):
    print('candlestick-base_id: ', base_id,
          'candlestick-quote-id :', quote_id,
          'candlestick-interval: ', interval)
    if base_id is None:
        raise PreventUpdate

    if quote_id is None:
        raise PreventUpdate

    if interval is None:
        raise PreventUpdate

    return [dcc.Graph(figure=get_candlestick_fig(base_id, quote_id, interval))]


@app.callback(
    [Output(component_id='details-display', component_property='children'),
     Output(component_id='details-line-plot', component_property='children')

     ],
    [Input(component_id='details_crypto_id', component_property='value'),
     ], prevent_initial_call=True
)
def render_details(crypto_id):
    print('details_crypto_id', crypto_id)
    if crypto_id is None:
        raise PreventUpdate

    return [
        dbc.Table(
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
    ], [dcc.Graph(figure=get_details_line_fig(crypto_id))]


@ app.callback(
    [Output(component_id='volume_daysInWeek-plot', component_property='children'),
     ],
    [Input(component_id='volume_daysInWeek-base-id', component_property='value'),
     Input(component_id='volume_daysInWeek-quote-id',
           component_property='value'),
     ], prevent_initial_call=True
)
def render_volume_daysInWeek(base_id, quote_id):
    if base_id is None:
        raise PreventUpdate

    if quote_id is None:
        raise PreventUpdate

    return [dcc.Graph(figure=get_volume_fig(base_id, quote_id))]


@ app.callback(
    [Output(component_id='correlation-plot', component_property='children'),
     ],
    [Input(component_id='correlation-base-id', component_property='value'),
     Input(component_id='correlation-quote-id',
           component_property='value'),
     Input(component_id='correlation-interval',
           component_property='value'),
     ], prevent_initial_call=True
)
def render_correlation(base_id, quote_id, interval):
    if base_id is None:
        raise PreventUpdate

    if quote_id is None:
        raise PreventUpdate

    if interval is None:
        raise PreventUpdate

    return [dcc.Graph(figure=get_correlation_fig(base_id, quote_id, interval))]


if __name__ == '__main__':
    PORT = 8050
    app.run_server(debug=True, port=PORT)
