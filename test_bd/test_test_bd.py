import os
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from test_bd import engine, exchange


# Testing the creation and setup of the API object
def test_api_setup():
    assert exchange.apiKey == os.getenv("API_KEY"), "Incorrect API key"
    assert exchange.secret == os.getenv("API_SECRET"), "Incorrect API secret"
    assert exchange.password == os.getenv(
        "API_PASSPHRASE"
    ), "Incorrect API password"


# Testing fetching historical data from the API
@patch("ccxt.coinbasepro.fetch_ohlcv")
def test_fetch_data(mock_fetch_ohlcv):
    mock_data = [[1609459200000, 29000, 29500, 28700, 29300, 1200]]
    mock_fetch_ohlcv.return_value = mock_data
    btc_data = exchange.fetch_ohlcv("BTC-USD", "1h", limit=1)
    assert btc_data == mock_data, "Incorrect historical data"


# Testing converting data to DataFrame
def test_data_to_dataframe():
    mock_data = [[1609459200000, 29000, 29500, 28700, 29300, 1200]]
    df = pd.DataFrame(
        mock_data,
        columns=["timestamp", "open", "high", "low", "close", "volume"],
    )
    assert not df.empty, "DataFrame is empty"
    assert df.iloc[0]["close"] == 29300, "Incorrect data in DataFrame"


# Testing writing data to the database
@patch("sqlalchemy.engine.base.Engine.connect")
def test_save_data_to_db(mock_connect):
    mock_connect.return_value = True
    assert engine.connect(), "Failed to connect to the database"


# Testing closing the database connection
@patch("sqlalchemy.engine.base.Engine.dispose")
def test_close_db_connection(mock_dispose):
    mock_dispose.return_value = None
    engine.dispose()
    mock_dispose.assert_called_once(), "Database connection was not closed"
