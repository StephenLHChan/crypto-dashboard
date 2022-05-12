import dash
import dash_bootstrap_components as dbc

from layout import layout
from callbacks import register_callbacks

app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB, dbc.icons.BOOTSTRAP],
                suppress_callback_exceptions=True)
server = app.server

app.title = "Crypto Dashboard"
app.layout = layout
register_callbacks(app)


if __name__ == '__main__':
    PORT = 8050
    app.run_server(debug=True, port=PORT)
