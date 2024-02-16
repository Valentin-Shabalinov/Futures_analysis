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


# Подключение к базе данных PostgreSQL
db_connection_string = "postgresql://futures_user:aaa@postgres-db:5432/analys"
engine = create_engine(db_connection_string)

# Чтение данных из таблиц базы данных
btc_data = pd.read_sql_table("btc_data", engine)
eth_data = pd.read_sql_table("eth_data", engine)
eth_data_filtered = pd.read_sql_table("eth_data_filtered", engine)
eth_data_predictions = pd.read_sql_table("eth_data_predictions", engine)

# Инициализация Dash-приложения
app = dash.Dash(__name__)


# Ключи API Coinbase Pro
COINBASE_API_KEY = os.getenv("API_KEY")
COINBASE_API_SECRET = os.getenv("API_SECRET")
COINBASE_API_PASSPHRASE = os.getenv("API_PASSPHRASE")


# Функция для подписи запроса к Coinbase Pro API
def sign_coinbase_pro_request(timestamp, method, path, body=""):
    api_secret = COINBASE_API_SECRET or ""  # Проверка наличия API_SECRET
    message = f"{timestamp}{method}{path}{body}"
    signature = hmac.new(
        base64.b64decode(api_secret.encode("utf-8")),
        message.encode("utf-8"),
        hashlib.sha256,
    )
    signature_b64 = base64.b64encode(signature.digest()).decode("utf-8")
    return signature_b64


# Функция для получения цены в реальном времени с использованием Coinbase Pro API
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


# # Функция для получения текущей даты и времени в формате "ГГГГ-ММ-ДД ЧЧ:ММ:СС"
def get_current_datetime():
    moscow_tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(moscow_tz)
    return now.strftime("%Y-%m-%d %H:%M:%S")


# Обновление цен в реальном времени каждые 10 секунд
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
            btc_output = f"Цена BTC {current_datetime}: ${btc_price}"
        else:
            btc_output = "Не удалось получить цену BTC"

        if eth_price is not None:
            eth_output = f"Цена ETH {current_datetime}: ${eth_price}"
        else:
            eth_output = "Не удалось получить цену ETH"

        return btc_output, eth_output
    except Exception as e:
        print(f"Error updating real-time prices: {e}")
        return "Ошибка обновления цен", "Ошибка обновления цен"


# Макет с боковой панелью
app.layout = html.Div(
    [
        html.Nav(
            children=[
                html.H2(
                    "Меню",
                    style={
                        "display": "block",
                        "font-weight": "bold",
                        "color": "#333",
                        "padding": "10px",
                    },
                ),
                html.A(
                    "Исторические данные BTC",
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
                    "Исторические данные ETH",
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
                    "Данные ETH без влияния BTC",
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
                    "Прогнозы ETH",
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
                        "color": "#333",
                        "padding": "10px",
                    },
                ),
                html.Div(
                    id="real-time-eth-price",
                    style={
                        "display": "block",
                        "text-decoration": "none",
                        "font-weight": "bold",
                        "color": "#333",
                        "padding": "10px",
                    },
                ),
                dcc.Interval(
                    id="real-time-interval-component",
                    interval=10
                    * 1000,  # Обновление каждые 10 секунд (в миллисекундах)
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
                "background-color": "#314455",
                "min-height": "100vh",
                "width": "80vw",
            },
        ),  # Обновленный стиль
    ],
    style={"height": "100vh", "background-color": "#314455"},
)


# Отображение разных графиков в зависимости от выбранной ссылки в боковой панели
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
                        "name": "Данные BTC",
                    }
                ],
                "layout": {"title": "Исторические данные BTC"},
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
                        "name": "Данные ETH",
                    }
                ],
                "layout": {"title": "Исторические данные ETH"},
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
                        "name": "Прогноз ETH",
                    }
                ],
                "layout": {"title": "Прогноз ETH"},
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
                        "name": "Данные ETH",
                    },
                    {
                        "x": eth_data_filtered["timestamp"],
                        "y": eth_data_filtered["eth_close_filtered"],
                        "type": "line",
                        "name": "Данные ETH без влияния BTC",
                    },
                ],
                "layout": {"title": "Данные ETH без влияния BTC"},
            },
        )
    else:
        return html.H1("Добро пожаловать!")


# Запуск Dash-приложения
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
