import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import requests
from sqlalchemy import create_engine
import datetime
import time
import base64
import hmac
import hashlib
import pytz


# Connecting to the PostgreSQL database
db_connection_string = "postgresql://futures_user:aaa@postgres-db:5432/analys"
# db_connection_string = "postgresql://futures_user:082101@localhost:5432/analys"

engine = create_engine(db_connection_string)
current_year = datetime.datetime.now().year

# Reading data from database tables
btc_data = pd.read_sql_table("btc_data", engine)
eth_data = pd.read_sql_table("eth_data", engine)
eth_data_filtered = pd.read_sql_table("eth_data_filtered", engine)
eth_data_predictions = pd.read_sql_table("eth_data_predictions", engine)

# Initializing Dash application
app = dash.Dash(__name__)


# Coinbase Pro API keys
COINBASE_API_KEY = os.getenv("API_KEY")
COINBASE_API_SECRET = os.getenv("API_SECRET")
COINBASE_API_PASSPHRASE = os.getenv("API_PASSPHRASE")


# Function for signing a request to the Coinbase Pro API
def sign_coinbase_pro_request(timestamp, method, path, body=""):
    api_secret = COINBASE_API_SECRET or ""  # Checking for API_SECRET presence
    message = f"{timestamp}{method}{path}{body}"
    signature = hmac.new(
        base64.b64decode(api_secret.encode("utf-8")),
        message.encode("utf-8"),
        hashlib.sha256,
    )
    signature_b64 = base64.b64encode(signature.digest()).decode("utf-8")
    return signature_b64


# Function for getting real-time price using the Coinbase Pro API
def get_real_time_price(product_id):
    url = f"https://api.pro.coinbase.com/products/{product_id}/ticker"
    timestamp = str(time.time())
    headers = {
        "CB-ACCESS-KEY": COINBASE_API_KEY,
        "CB-ACCESS-SIGN": sign_coinbase_pro_request(
            timestamp, "GET", f"/products/{product_id}/ticker"
        ),
        "CB-ACCESS-TIMESTAMP": timestamp,
        "CB-ACCESS-PASSPHRASE": COINBASE_API_PASSPHRASE,
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        price = float(data["price"])
        return price
    except requests.exceptions.RequestException as e:
        print(f"Error fetching real-time price: {e}")
        return None


# Function to get the current date and time in the format "YYYY-MM-DD HH:MM:SS"
def get_current_datetime():
    moscow_tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(moscow_tz)
    return now.strftime("%Y-%m-%d %H:%M:%S")


# Updating real-time prices every 10 seconds
@app.callback(
    [
        Output("real-time-btc-price", "children"),
        Output("real-time-eth-price", "children"),
    ],
    [Input("real-time-interval-component", "n_intervals")],
)
def update_real_time_prices(n_intervals):
    try:
        btc_price = get_real_time_price("BTC-USD")
        eth_price = get_real_time_price("ETH-USD")

        current_datetime = get_current_datetime()

        if btc_price is not None:
            btc_output = f"BTC Price {current_datetime}: ${btc_price}"
        else:
            btc_output = "Failed to fetch BTC price"

        if eth_price is not None:
            eth_output = f"ETH Price {current_datetime}: ${eth_price}"
        else:
            eth_output = "Failed to fetch ETH price"

        return btc_output, eth_output
    except Exception as e:
        print(f"Error updating real-time prices: {e}")
        return "Error updating prices", "Error updating prices"


# Layout with a sidebar
app.layout = html.Div(
    [
        html.Nav(
            children=[
                html.H2(
                    "Menu",
                    style={
                        "display": "block",
                        "font-weight": "bold",
                        "color": "#333",
                        "padding": "10px",
                    },
                ),
                html.A(
                    "BTC historical data",
                    href="/btc",
                    style={
                        "display": "block",
                        "text-decoration": "none",
                        "font-weight": "bold",
                        "color": "#644E5B",
                        "padding": "10px",
                    },
                ),
                html.A(
                    "ETH historical data",
                    href="/eth",
                    style={
                        "display": "block",
                        "text-decoration": "none",
                        "font-weight": "bold",
                        "color": "#644E5B",
                        "padding": "10px",
                    },
                ),
                html.A(
                    "ETH data without BTC influence",
                    href="/eth-filtered",
                    style={
                        "display": "block",
                        "text-decoration": "none",
                        "font-weight": "bold",
                        "color": "#644E5B",
                        "padding": "10px",
                    },
                ),
                html.A(
                    "ETH forecasts",
                    href="/eth-predictions",
                    style={
                        "display": "block",
                        "text-decoration": "none",
                        "font-weight": "bold",
                        "color": "#644E5B",
                        "padding": "10px",
                    },
                ),
                html.Div(
                    id="real-time-btc-price",
                    style={
                        "display": "block",
                        "text-decoration": "none",
                        "font-weight": "bold",
                        "color": "#D3D3D3",
                        "padding": "10px",
                        "border": "2px dotted black",
                        "margin-top": "60px",  # Отступ сверху
                        "margin-bottom": "10px",  # Отступ снизу
                        "background-color": "#4F6B72",
                    },
                ),
                html.Div(
                    id="real-time-eth-price",
                    style={
                        "display": "block",
                        "text-decoration": "none",
                        "font-weight": "bold",
                        "color": "#98FF98",
                        "padding": "10px",
                        "border": "2px dotted black",
                        "background-color": "#4F6B72",
                    },
                ),
                dcc.Interval(
                    id="real-time-interval-component",
                    interval=10
                    * 1000,  # Update every 10 seconds (in milliseconds)
                    n_intervals=0,
                ),
            ],
            style={
                "width": "20%",
                "position": "fixed",
                "height": "100vh",
                "backgroundColor": "#97AABD",
            },
        ),
        html.Div(
            [
                dcc.Location(id="url", refresh=False),
                html.Div(id="page-content"),
            ],
            style={
                "margin-left": "20%",
                "padding": "20px",
                "background-color": "#1F2833",
                "min-height": "100vh",
                "width": "80vw",
            },
        ),  # Updated style
        html.Footer(
            children=[
                html.Div(
                    f'© 2024-{current_year}',
                    style={
                        'textAlign': 'center',
                        'color': '#FFF',
                        'padding': '20px',
                        'background-color': '#1F2833',
                        'margin-top': '20px',
                    }
                )
            ],
            style={
                'position': 'relative',
                'bottom': '0',
                'width': '100%',
                'height': '60px',
            }
        )
    ],
    style={"height": "100vh", "background-color": "#314455"},
)


# Displaying different charts depending on the sidebar link selected
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/btc":
        return dcc.Graph(
            id="btc-chart",
            figure={
                "data": [
                    {
                        "x": btc_data["timestamp"],
                        "y": btc_data["close"],
                        "type": "line",
                        "name": "BTC Data",
                    }
                ],
                "layout": {"title": "BTC Historical Data"},
            },
        )
    elif pathname == "/eth":
        return dcc.Graph(
            id="eth-data-chart",
            figure={
                "data": [
                    {
                        "x": eth_data["timestamp"],
                        "y": eth_data["close"],
                        "type": "line",
                        "name": "ETH Data",
                    }
                ],
                "layout": {"title": "ETH Historical Data"},
            },
        )
    elif pathname == "/eth-predictions":
        return dcc.Graph(
            id="eth-predictions-chart",
            figure={
                "data": [
                    {
                        "x": eth_data_predictions["timestamp"],
                        "y": eth_data_predictions["predicted_close"],
                        "type": "line",
                        "name": "ETH Forecast",
                    }
                ],
                "layout": {"title": "ETH Forecast"},
            },
        )
    elif pathname == "/eth-filtered":
        return dcc.Graph(
            id="eth-filtered-chart",
            figure={
                "data": [
                    {
                        "x": eth_data["timestamp"],
                        "y": eth_data["close"],
                        "type": "line",
                        "name": "ETH Data",
                    },
                    {
                        "x": eth_data_filtered["timestamp"],
                        "y": eth_data_filtered["eth_close_filtered"],
                        "type": "line",
                        "name": "ETH Data Without BTC Influence",
                    },
                ],
                "layout": {"title": "ETH Data Without BTC Influence"},
            },
        )
    else:
        return html.H1("Welcome!")


# Running the Dash application
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
