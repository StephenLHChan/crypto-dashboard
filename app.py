import dash

from layout import layout
from callbacks import register_callbacks

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.title = "Crypto Dashboard"
app.layout = layout
register_callbacks(app)


if __name__ == '__main__':
    PORT = 8050
    app.run_server(debug=True, port=PORT)
