from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import statsmodels.api as sm

# Database connection
engine = create_engine("postgresql://futures_user:aaa@postgres-db:5432/analys")
# engine = create_engine(
#     "postgresql://futures_user:082101@localhost:5432/analys"
#     )

# Loading data from btc_data table
btc_data_query = "SELECT timestamp, close AS btc_close FROM btc_data"
btc_data_df = pd.read_sql(btc_data_query, engine)

# Loading data from eth_data table
eth_data_query = "SELECT timestamp, close AS eth_close FROM eth_data"
eth_data_df = pd.read_sql(eth_data_query, engine)

# Merging data based on timestamp
merged_data = pd.merge(btc_data_df, eth_data_df, on="timestamp", how="inner")

# Correlation analysis
correlation_matrix = np.corrcoef(
    merged_data["btc_close"], merged_data["eth_close"]
)
correlation = correlation_matrix[0, 1]

# Printing correlation coefficient
print(f"Correlation coefficient between BTC and ETH: {correlation}")

# Adding constant for regression
merged_data = sm.add_constant(merged_data)

# Regression model
model = sm.OLS(merged_data["eth_close"], merged_data[["const", "btc_close"]])
results = model.fit()

# Getting regression coefficients
beta_btc = results.params["btc_close"]

# Separating movements
eth_data_df["eth_close_filtered"] = (
    eth_data_df["eth_close"] - beta_btc * btc_data_df["btc_close"]
)

# Writing data to a new table eth_data_filtered
eth_data_df.to_sql(
    "eth_data_filtered", engine, if_exists="replace", index=False
)
