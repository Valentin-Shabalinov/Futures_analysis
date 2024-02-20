import ccxt
import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# API Keys for Coinbase Pro
api_key = "jjyn6AGhau51Mzpb"
api_secret = "rXmwagvlweDEYSQmWkcnuQoiGDv6eQ03"
api_passphrase = "pN+X6Vs7Fs/85DM"

# Creating Coinbase Pro API object
exchange = ccxt.coinbasepro(
    {
        "apiKey": api_key,
        "secret": api_secret,
        "password": api_passphrase,
    }
)

# Symbols for ETHUSD
eth_symbol = "ETH-USD"

# Parameters for fetching historical data
timeframe = "1h"  # 1 hour

# Loading historical data for ETH
eth_data = exchange.fetch_ohlcv(eth_symbol, timeframe)
eth_df = pd.DataFrame(
    eth_data, columns=["timestamp", "open", "high", "low", "close", "volume"]
)
eth_df["timestamp"] = pd.to_datetime(
    eth_df["timestamp"], unit="ms"
)  # Converting timestamps

# Creating 'target' column for predicting ETH price 1 week ahead
eth_df["target"] = eth_df["close"].shift(-7)  # Shifting price 7 rows forward

# Removing the last 7 rows as they don't have a 'target' value
eth_df = eth_df[:-7]

# Splitting data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    eth_df[["open", "high", "low", "close", "volume"]],
    eth_df["target"],
    test_size=0.2,
    random_state=42,
)

# Training the model
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Prediction on the test set
y_pred = model.predict(X_test)

# Evaluating the model
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Applying the model to predict the price 1 week ahead for all data
eth_df["predicted_target"] = model.predict(
    eth_df[["open", "high", "low", "close", "volume"]]
)
eth_df["predicted_close"] = eth_df[
    "predicted_target"
]  # Creating 'predicted_close' column based on predicted price

# Creating connection to PostgreSQL database
db_connection_string = "postgresql://futures_user:aaa@postgres-db:5432/analys"
# db_connection_string = "postgresql://futures_user:082101@localhost:5432/analys"

engine = create_engine(db_connection_string)

# Writing ETH data to the database
eth_df.to_sql(name="eth_data_predictions", con=engine, if_exists="replace")

# Closing the database connection
engine.dispose()
