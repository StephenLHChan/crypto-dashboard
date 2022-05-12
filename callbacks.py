from tabs.candlestick import candlestick_callbacks
from tabs.marketCap import marketCap_callbacks
from tabs.details import details_callbacks
from tabs.volumn import volumn_callbacks
from tabs.correlation import correlation_callbacks
from layout import layout_callbacks


def register_callbacks(app):
    layout_callbacks(app)
    marketCap_callbacks(app)
    candlestick_callbacks(app)
    details_callbacks(app)
    volumn_callbacks(app)
    correlation_callbacks(app)
