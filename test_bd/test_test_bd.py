import os
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from test_bd import engine, exchange


# Тестирование создания и настройки объекта API
def test_api_setup():
    assert exchange.apiKey == os.getenv("API_KEY"), "Неверный API ключ"
    assert exchange.secret == os.getenv("API_SECRET"), "Неверный API секрет"
    assert exchange.password == os.getenv(
        "API_PASSPHRASE"
    ), "Неверный API пароль"


# Тестирование получения исторических данных от API
@patch("ccxt.coinbasepro.fetch_ohlcv")
def test_fetch_data(mock_fetch_ohlcv):
    mock_data = [[1609459200000, 29000, 29500, 28700, 29300, 1200]]
    mock_fetch_ohlcv.return_value = mock_data
    btc_data = exchange.fetch_ohlcv("BTC-USD", "1h", limit=1)
    assert btc_data == mock_data, "Неверные исторические данные"


# Тестирование преобразования данных в DataFrame
def test_data_to_dataframe():
    mock_data = [[1609459200000, 29000, 29500, 28700, 29300, 1200]]
    df = pd.DataFrame(
        mock_data,
        columns=["timestamp", "open", "high", "low", "close", "volume"],
    )
    assert not df.empty, "DataFrame пустой"
    assert df.iloc[0]["close"] == 29300, "Неверные данные в DataFrame"


# Тестирование записи данных в базу данных
@patch("sqlalchemy.engine.base.Engine.connect")
def test_save_data_to_db(mock_connect):
    mock_connect.return_value = True
    assert engine.connect(), "Не удалось подключиться к базе данных"


# Тестирование закрытия соединения с базой данных
@patch("sqlalchemy.engine.base.Engine.dispose")
def test_close_db_connection(mock_dispose):
    mock_dispose.return_value = None
    engine.dispose()
    mock_dispose.assert_called_once(), "Соединение с базой данных не было закрыто"
