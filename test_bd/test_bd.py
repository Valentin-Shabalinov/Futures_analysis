import ccxt
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os

# API Keys for Coinbase Pro
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
api_passphrase = os.getenv("API_PASSPHRASE")

# Creating Coinbase Pro API object
exchange = ccxt.coinbasepro(
    {
        "apiKey": api_key,
        "secret": api_secret,
        "password": api_passphrase,
    }
)

# Symbols for ETHUSD and BTCUSD
eth_symbol = "ETH-USD"
btc_symbol = "BTC-USD"

# Parameters for fetching historical data
timeframe = "1h"  # 1 hour
block_size = 300  # Request block size (maximum value - 300)

# Starting timestamp for BTC
start_time_btc = exchange.parse8601("2022-01-01T00:00:00Z")

# Creating connection to PostgreSQL database
db_connection_string = "postgresql://futures_user:aaa@postgres-db:5432/analys"
# Alternate db_connection_string = "postgresql://futures_user:082101@localhost:5432/analys"

engine = create_engine(db_connection_string)

# Writing BTC data to the database
btc_data_list = []

while True:
    # Fetching historical data for BTC
    btc_data = exchange.fetch_ohlcv(
        btc_symbol, timeframe, since=start_time_btc, limit=block_size
    )
    if not btc_data:
        break
    btc_data_list += btc_data
    start_time_btc = (
        btc_data[-1][0] + 1
    )  # Setting new timestamp for the next block

# Converting BTC data to DataFrame
btc_df = pd.DataFrame(
    btc_data_list,
    columns=["timestamp", "open", "high", "low", "close", "volume"],
)

# Converting timestamps to readable format
btc_df["timestamp"] = btc_df["timestamp"].apply(
    lambda x: datetime.utcfromtimestamp(x / 1000).strftime("%Y-%m-%d %H:%M:%S")
)

# Writing BTC data to the database
btc_df.to_sql(name="btc_data", con=engine, if_exists="replace", index=False)

# Starting timestamp for ETH
start_time_eth = exchange.parse8601("2022-01-01T00:00:00Z")

# Writing ETH data to the database
eth_data_list = []

while True:
    # Fetching historical data for ETH
    eth_data = exchange.fetch_ohlcv(
        eth_symbol, timeframe, since=start_time_eth, limit=block_size
    )
    if not eth_data:
        break
    eth_data_list += eth_data
    start_time_eth = (
        eth_data[-1][0] + 1
    )  # Setting new timestamp for the next block

# Converting ETH data to DataFrame
eth_df = pd.DataFrame(
    eth_data_list,
    columns=["timestamp", "open", "high", "low", "close", "volume"],
)

# Converting timestamps to readable format
eth_df["timestamp"] = eth_df["timestamp"].apply(
    lambda x: datetime.utcfromtimestamp(x / 1000).strftime("%Y-%m-%d %H:%M:%S")
)

# Writing ETH data to the database
eth_df.to_sql(name="eth_data", con=engine, if_exists="replace", index=False)

# Closing the database connection
engine.dispose()
