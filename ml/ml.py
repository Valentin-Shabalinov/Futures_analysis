import ccxt
import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Ключи API Coinbase Pro
api_key = "jjyn6AGhau51Mzpb"
api_secret = "rXmwagvlweDEYSQmWkcnuQoiGDv6eQ03"
api_passphrase = "pN+X6Vs7Fs/85DM"

# Создаем объект Coinbase Pro API
exchange = ccxt.coinbasepro(
    {
        "apiKey": api_key,
        "secret": api_secret,
        "password": api_passphrase,
    }
)

# Символы для ETHUSD
eth_symbol = "ETH-USD"

# Параметры запроса исторических данных
timeframe = "1h"  # 1 час

# Загружаем исторические данные для ETH
eth_data = exchange.fetch_ohlcv(eth_symbol, timeframe)
eth_df = pd.DataFrame(
    eth_data, columns=["timestamp", "open", "high", "low", "close", "volume"]
)
eth_df["timestamp"] = pd.to_datetime(
    eth_df["timestamp"], unit="ms"
)  # Преобразуем временные метки

# Создаем столбец 'target' для предсказания курса ETH на 1 неделю вперед
eth_df["target"] = eth_df["close"].shift(-7)  # Сдвигаем цену на 7 строк вперед

# Удаляем последние 7 строк, так как для них нет значения 'target'
eth_df = eth_df[:-7]

# Разделение данных на обучающий и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(
    eth_df[["open", "high", "low", "close", "volume"]],
    eth_df["target"],
    test_size=0.2,
    random_state=42,
)

# Обучение модели
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Предсказание на тестовом наборе
y_pred = model.predict(X_test)

# Оценка модели
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Применение модели для предсказания курса на 1 неделю вперед для всех данных
eth_df["predicted_target"] = model.predict(
    eth_df[["open", "high", "low", "close", "volume"]]
)
eth_df["predicted_close"] = eth_df[
    "predicted_target"
]  # Создаем столбец 'predicted_close' на основе предсказанной цены

# Создаем соединение с базой данных PostgreSQL
db_connection_string = "postgresql://futures_user:aaa@postgres-db:5432/analys"
# db_connection_string = "postgresql://futures_user:082101@localhost:5432/analys"

engine = create_engine(db_connection_string)

# Записываем данные ETH в базу данных
eth_df.to_sql(name="eth_data_predictions", con=engine, if_exists="replace")

# Закрываем соединение с базой данных
engine.dispose()
