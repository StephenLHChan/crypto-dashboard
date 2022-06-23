from dash import html, dcc, Input, Output
from tabs.candlestick import candlestick_tab_content
from tabs.marketCap import marketCap_tab_content
from tabs.details import crypto_details_tab_content
from tabs.volumn import volume_daysInWeek_tab_content
from tabs.correlation import correlation_price_change_volume_tab_cantent


def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[html.H5('Crypto Dashboard')],
            )

        ]
    )


def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                className="custom-tabs",
                value="market-cap",
                children=[
                    dcc.Tab(
                        id="market-cap-tab",
                        label="Market Cap Overview",
                        value="market-cap",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="crypto-details-tab",
                        label="Crypto Details",
                        value="crypto-details",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="candlestick-tab",
                        label="Candlestick Chart",
                        value="candlestick",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="volume-daysInWeek-tab",
                        label="Volume of days in week",
                        value="volume-daysInWeek",
                        className="custom-tab",
                        selected_className="custom-tab--selected",

                    ),
                    dcc.Tab(
                        id="correlation-price_change-volume-tab",
                        label="Correlation",
                        value="correlation-price_change-volume",
                        className="custom-tab",
                        selected_className="custom-tab--selected",

                    )
                ],

            )
        ]
    )


layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                dcc.Loading(
                    children=[
                        html.Div(id="app-content")])
            ]
        )
    ])


def layout_callbacks(app):
    @ app.callback(
        [Output("app-content", "children"),
         ],
        [Input("app-tabs", "value"),
         ]
    )
    def render_tab_content(active_tab):
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
