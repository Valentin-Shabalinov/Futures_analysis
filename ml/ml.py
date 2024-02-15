# import ccxt
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_squared_error
# from sklearn.preprocessing import MinMaxScaler
# from datetime import datetime, timedelta
# import matplotlib.pyplot as plt
# import numpy as np
# from sqlalchemy import create_engine

# # Ключи API Coinbase Pro
# api_key = 'jjyn6AGhau51Mzpb'
# api_secret = 'rXmwagvlweDEYSQmWkcnuQoiGDv6eQ03'
# api_passphrase = 'pN+X6Vs7Fs/85DM'

# # Создаем объект Coinbase Pro API
# exchange = ccxt.coinbasepro({
#     'apiKey': api_key,
#     'secret': api_secret,
#     'password': api_passphrase,
# })

# # Параметры запроса исторических данных
# timeframe = '1h'  # 1 час
# limit = 15000  # Количество свечей

# # Подключение к базе данных PostgreSQL
# db_connection_string = "postgresql://futures_user:082101@localhost:5432/analys"
# engine = create_engine(db_connection_string)

# # Загружаем исторические данные из таблицы eth_data
# query = "SELECT * FROM eth_data ORDER BY timestamp"
# eth_df = pd.read_sql(query, engine)

# # Преобразуем временные метки в читаемый формат
# eth_df['timestamp'] = pd.to_datetime(eth_df['timestamp'])

# # Создаем признаки (features) для модели
# X = eth_df[['timestamp']]  # В качестве признака используем timestamp
# y = eth_df['close']  # Целевая переменная (target)

# # Разделяем данные на обучающую и тестовую выборки
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# X_test = X_test.sort_values(by=['timestamp'])

# # Создаем и обучаем модель
# model = RandomForestRegressor(n_estimators=100, random_state=42)
# model.fit(X_train, y_train)

# # Генерируем временные метки для прогноза (1 час вперед)
# future_timestamps = pd.date_range(start=eth_df['timestamp'].min(), periods=len(eth_df)+1, freq='60S')

# # Прогнозируем цены на 1 час вперед
# future_predictions = model.predict(pd.DataFrame(future_timestamps, columns=['timestamp']))

# # Преобразуем временные метки в читаемый формат
# future_timestamps_datetime = pd.to_datetime(future_timestamps)

# # Визуализация результатов
# plt.figure(figsize=(12, 6))
# plt.plot(X_test, y_test, color='black', label='Actual Prices')
# plt.plot(X_test, model.predict(X_test), color='blue', linewidth=3, label='Model Predictions')
# plt.plot(future_timestamps_datetime, future_predictions, color='red', linestyle='dashed', linewidth=3, label='Future Predictions')
# plt.xlabel('Timestamp')
# plt.ylabel('ETH-USD Price')
# plt.title('ETH-USD Price Prediction')
# plt.legend()
# plt.show()

# # Закрываем соединение с базой данных
# engine.dispose()

# ml.py
import ccxt
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Ключи API Coinbase Pro
api_key = 'jjyn6AGhau51Mzpb'
api_secret = 'rXmwagvlweDEYSQmWkcnuQoiGDv6eQ03'
api_passphrase = 'pN+X6Vs7Fs/85DM'

# Создаем объект Coinbase Pro API
exchange = ccxt.coinbasepro({
    'apiKey': api_key,
    'secret': api_secret,
    'password': api_passphrase,
})

# Символы для ETHUSD
eth_symbol = 'ETH-USD'

# Параметры запроса исторических данных
timeframe = '1h'  # 1 час

# Загружаем исторические данные для ETH
eth_data = exchange.fetch_ohlcv(eth_symbol, timeframe)
eth_df = pd.DataFrame(eth_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
eth_df['timestamp'] = pd.to_datetime(eth_df['timestamp'], unit='ms')  # Преобразуем временные метки

# Создаем столбец 'target' для предсказания курса ETH на 1 неделю вперед
eth_df['target'] = eth_df['close'].shift(-7)  # Сдвигаем цену на 7 строк вперед

# Удаляем последние 7 строк, так как для них нет значения 'target'
eth_df = eth_df[:-7]

# Разделение данных на обучающий и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(
    eth_df[['open', 'high', 'low', 'close', 'volume']],
    eth_df['target'],
    test_size=0.2,
    random_state=42
)

# Обучение модели случайного леса
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Предсказание на тестовом наборе
y_pred = model.predict(X_test)

# Оценка модели
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Применение модели для предсказания курса на 1 неделю вперед для всех данных
eth_df['predicted_target'] = model.predict(eth_df[['open', 'high', 'low', 'close', 'volume']])

# Создаем соединение с базой данных PostgreSQL
db_connection_string = "postgresql://futures_user:aaa@postgres-db:5432/analys"
engine = create_engine(db_connection_string)

# Записываем данные ETH в базу данных
eth_df.to_sql(name='eth_data_predictions', con=engine, if_exists='replace', index=False)

# Закрываем соединение с базой данных
engine.dispose()


# # ml.py
# import os
# import ccxt
# import pandas as pd
# from sqlalchemy import create_engine
# from datetime import datetime, timedelta
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_squared_error
# import numpy as np

# # Ключи API Coinbase Pro
# api_key = os.getenv('API_KEY')
# api_secret = os.getenv('API_SECRET')
# api_passphrase = os.getenv('API_PASSPHRASE')

# # Создаем объект Coinbase Pro API
# exchange = ccxt.coinbasepro({
#     'apiKey': api_key,
#     'secret': api_secret,
#     'password': api_passphrase,
# })

# # Символы для ETHUSD
# eth_symbol = 'ETH-USD'

# # Параметры запроса исторических данных
# timeframe = '1h'  # 1 час

# # Загружаем исторические данные для ETH
# eth_data = exchange.fetch_ohlcv(eth_symbol, timeframe)
# eth_df = pd.DataFrame(eth_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
# eth_df['timestamp'] = pd.to_datetime(eth_df['timestamp'], unit='ms')  # Преобразуем временные метки

# # Создаем столбец 'target' для предсказания курса ETH на 1 неделю вперед
# eth_df['target'] = eth_df['close'].shift(-7)  # Сдвигаем цену на 7 строк вперед

# # Удаляем последние 7 строк, так как для них нет значения 'target'
# eth_df = eth_df[:-7]

# # Разделение данных на обучающий и тестовый наборы
# X_train, X_test, y_train, y_test = train_test_split(
#     eth_df[['open', 'high', 'low', 'close', 'volume']],
#     eth_df['target'],
#     test_size=0.2,
#     random_state=42
# )

# # Обучение модели случайного леса
# model = RandomForestRegressor(random_state=42)
# model.fit(X_train, y_train)

# # Предсказание на тестовом наборе
# y_pred = model.predict(X_test)

# # Оценка модели
# mse = mean_squared_error(y_test, y_pred)
# print(f'Mean Squared Error: {mse}')

# # Применение модели для предсказания курса на 1 неделю вперед для всех данных
# eth_df['predicted_target'] = model.predict(eth_df[['open', 'high', 'low', 'close', 'volume']])

# # Создаем соединение с базой данных PostgreSQL
# db_connection_string = "postgresql://futures_user:082101@localhost:5432/analys"
# engine = create_engine(db_connection_string)

# # Записываем данные ETH в базу данных
# eth_df.to_sql(name='eth_data_with_predictions', con=engine, if_exists='replace', index=False)

# # Генерация временных меток для будущих дат
# current_timestamp = int(datetime.timestamp(datetime.now()))
# target_period = 7 * 24  # 7 дней в часах
# future_timestamps = np.arange(current_timestamp, current_timestamp + target_period * 3600, 3600)

# # Создание DataFrame для предсказанных данных
# df_future = pd.DataFrame(index=pd.to_datetime(future_timestamps, unit='s'))

# # Предсказание цен с использованием обученной модели
# features = df_future.index.astype(np.int64) // 10**9  # Преобразование временных меток
# features_df = pd.DataFrame({'open': [0] * len(features), 'high': [0] * len(features),
#                              'low': [0] * len(features), 'close': [0] * len(features),
#                              'volume': [0] * len(features)}, index=features)

# df_future['predicted_close'] = model.predict(features_df)


# # Создание новой таблицы с предсказанными данными
# df_future.to_sql(name='eth_data_predictions', con=engine, if_exists='replace', index=True)

# # Закрытие соединения
# engine.dispose()
