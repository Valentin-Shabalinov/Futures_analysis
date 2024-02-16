import ccxt
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os

# Ключи API Coinbase Pro
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
api_passphrase = os.getenv('API_PASSPHRASE')

# Создаем объект Coinbase Pro API
exchange = ccxt.coinbasepro({
    'apiKey': api_key,
    'secret': api_secret,
    'password': api_passphrase,
})

# Символы для ETHUSD и BTCUSD
eth_symbol = 'ETH-USD'
btc_symbol = 'BTC-USD'

# Параметры запроса исторических данных
timeframe = '1h'  # 1 час
block_size = 300  # Размер блока запроса (максимальное значение - 300)

# Начальная временная метка для BTC
start_time_btc = exchange.parse8601('2022-01-01T00:00:00Z')

# Создаем соединение с базой данных PostgreSQL
db_connection_string = "postgresql://futures_user:aaa@postgres-db:5432/analys"
engine = create_engine(db_connection_string)

# Записываем данные BTC в базу данных
btc_data_list = []

while True:
    # Загружаем исторические данные для BTC
    btc_data = exchange.fetch_ohlcv(btc_symbol, timeframe, since=start_time_btc, limit=block_size)
    if not btc_data:
        break
    btc_data_list += btc_data
    start_time_btc = btc_data[-1][0] + 1  # Устанавливаем новую временную метку для следующего блока

# Преобразуем данные BTC в DataFrame
btc_df = pd.DataFrame(btc_data_list, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# Преобразуем временные метки в читаемый формат
btc_df['timestamp'] = btc_df['timestamp'].apply(lambda x: datetime.utcfromtimestamp(x / 1000).strftime('%Y-%m-%d %H:%M:%S'))

# Записываем данные BTC в базу данных
btc_df.to_sql(name='btc_data', con=engine, if_exists='replace', index=False)

# Начальная временная метка для ETH
start_time_eth = exchange.parse8601('2022-01-01T00:00:00Z')

# Записываем данные ETH в базу данных
eth_data_list = []

while True:
    # Загружаем исторические данные для ETH
    eth_data = exchange.fetch_ohlcv(eth_symbol, timeframe, since=start_time_eth, limit=block_size)
    if not eth_data:
        break
    eth_data_list += eth_data
    start_time_eth = eth_data[-1][0] + 1  # Устанавливаем новую временную метку для следующего блока

# Преобразуем данные ETH в DataFrame
eth_df = pd.DataFrame(eth_data_list, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# Преобразуем временные метки в читаемый формат
eth_df['timestamp'] = eth_df['timestamp'].apply(lambda x: datetime.utcfromtimestamp(x / 1000).strftime('%Y-%m-%d %H:%M:%S'))

# Записываем данные ETH в базу данных
eth_df.to_sql(name='eth_data', con=engine, if_exists='replace', index=False)

# Закрываем соединение с базой данных
engine.dispose()