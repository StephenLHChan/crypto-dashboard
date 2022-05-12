from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
from tabs.candlestick import candlestick_tab_content
from tabs.marketCap import marketCap_tab_content
from tabs.details import crypto_details_tab_content
from tabs.volumn import volume_daysInWeek_tab_content
from tabs.correlation import correlation_price_change_volume_tab_cantent

layout = dbc.Container(html.Div(
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


def layout_callbacks(app):
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
