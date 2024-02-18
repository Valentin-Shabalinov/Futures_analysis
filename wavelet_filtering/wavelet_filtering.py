from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import statsmodels.api as sm

# Подключение к базе данных
engine = create_engine("postgresql://futures_user:aaa@postgres-db:5432/analys")
# engine = create_engine("postgresql://futures_user:082101@localhost:5432/analys")


# Загрузка данных из таблицы btc_data
btc_data_query = "SELECT timestamp, close AS btc_close FROM btc_data"
btc_data_df = pd.read_sql(btc_data_query, engine)

# Загрузка данных из таблицы eth_data
eth_data_query = "SELECT timestamp, close AS eth_close FROM eth_data"
eth_data_df = pd.read_sql(eth_data_query, engine)

# Объединение данных по временной метке
merged_data = pd.merge(btc_data_df, eth_data_df, on="timestamp", how="inner")

# Анализ корреляции
correlation_matrix = np.corrcoef(
    merged_data["btc_close"], merged_data["eth_close"]
)
correlation = correlation_matrix[0, 1]

# Вывод коэффициента корреляции
print(f"Коэффициент корреляции между BTC и ETH: {correlation}")

# Добавление константы для регрессии
merged_data = sm.add_constant(merged_data)

# Регрессионная модель
model = sm.OLS(merged_data["eth_close"], merged_data[["const", "btc_close"]])
results = model.fit()

# Получение коэффициентов регрессии
beta_btc = results.params["btc_close"]

# Разделение движений
eth_data_df["eth_close_filtered"] = (
    eth_data_df["eth_close"] - beta_btc * btc_data_df["btc_close"]
)

# Запись данных в новую таблицу eth_data_filtered
eth_data_df.to_sql(
    "eth_data_filtered", engine, if_exists="replace", index=False
)
