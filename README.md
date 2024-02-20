## TA7

## Application for Futures Price Analysis

### Description
### The task consists of 2 parts:

- You need to determine the intrinsic movements of the ETHUSDT futures price, excluding movements caused by the influence of the BTCUSDT price. Describe the methodology you chose, the parameters you selected, and why (justification can be provided in the README).
- Write a Python program that monitors the ETHUSDT futures price in real-time (with minimal delay) and, using the method you selected, determines the intrinsic price movements of ETH. If the price changes by 1% in the last 60 minutes, the program outputs a message in the console. Meanwhile, the program should continue to work, constantly reading the current price.
### To implement the project, the following actions were taken:
- Historical data on cryptocurrencies Ethereum (ETH) and Bitcoin (BTC) were collected using the Coinbase Pro exchange API and recorded in a PostgreSQL database. The data includes opening, closing, maximum, minimum prices, and trading volumes for each hour, starting from the specified date.
- An analysis of the relationship between the closing prices of Bitcoin (BTC) and Ethereum (ETH) was performed using correlation analysis and linear regression methods. After analysis, the data, filtered from the influence of BTC on ETH, are recorded in a new table in the PostgreSQL database.
- Based on the Ethereum (ETH) price data obtained through the Coinbase Pro API, steps were taken to load data, preprocess, train the model, evaluate accuracy, and record predictions in the PostgreSQL database for the purpose of predicting prices one week in advance.
- A Dash application was created for the visualization and analysis of data on cryptocurrencies Bitcoin (BTC) and Ethereum (ETH), including historical data, price forecasts, and analysis of BTC's influence on ETH. The application allows users to view real-time price charts and historical data loaded from the PostgreSQL database, as well as ETH price forecasts.
### To work with the project, the following steps must be taken:

- Clone the repository.
- Activate the virtual environment with venv/bin/activate.
- Create a .env file and fill it with data from the env.sample file (for simplicity, I've used my own data).
- Start the containers with the command docker-compose up --build (run twice, as the first attempt creates the tables, and the second fills them with data).
- Open a browser and go to http://localhost:8050 to access the application.



## Russian version
## ТА7
## Приложение для анализа цен фьючерса 
### Описание

Задание состоит из 2 частей:

1. Вам нужно определить собственные движения цены фьючерса ETHUSDT, исключив из них движения вызванные влиянием цены BTCUSDT. Опишите, какую методику вы выбрали, какие параметры подобрали, и почему (обоснование можно оформить в README).
2. Напишите программу на Python, которая в реальном времени (с минимальной задержкой) следит за ценой фьючерса ETHUSDT и используя выбранный вами метод, определяет собственные движение цены ETH. При изменении цены на 1% за последние 60 минут, программа выводит сообщение в консоль. При этом программа должна продолжать работать дальше, постоянно считывая актуальную цену.

### Для реализации проекта были выполнены следующие дествия:
- Произведен сбор исторических данных о криптовалютах Ethereum (ETH) и Bitcoin (BTC) с использованием API биржи Coinbase Pro и записи этих данных в базу данных PostgreSQL. Данные включают в себя цены открытия, закрытия, максимальные, минимальные цены, а также объемы торгов за каждый час, начиная с указанной даты.

- Произведен анализ взаимосвязи между ценами закрытия Bitcoin (BTC) и Ethereum (ETH) с использованием методов корреляционного анализа и линейной регрессии. После анализа данные, отфильтрованные от влияния BTC на ETH, записываются в новую таблицу в базе данных PostgreSQL.

- На основе данных о ценах Ethereum (ETH), полученных через API Coinbase Pro, для обучения модели с целью прогнозирования цен на 1 неделю вперёд, выполнены этапы загрузки данных, предварительной обработки, обучения модели, оценки точности и записи прогнозов в базу данных PostgreSQL.

- Создано Dash-приложение предназначеное для визуализации и анализа данных о криптовалютах Bitcoin (BTC) и Ethereum (ETH), включая исторические данные, прогнозы цен и анализ влияния BTC на ETH. Приложение позволяет пользователям просматривать графики цен в реальном времени и исторические данные, загруженные из базы данных PostgreSQL, а также прогнозы цен на ETH.

## Для работы с проектом необходимо выполнить следующие действия:

- Клонировать репозиторий.
- Активировать виртуальное окружение venv/bin/activate
- Создать файл .env, заполнить его данными из файла env.sample (для простоты данные оставил свои)
- Запустить контейнеры командой docker-compose up --build (запустить дважды, так как при первой попытке создаются таблицы, а пи второй заполняются данные)
- Откройте браузер и перейдите по адресу http://localhost:8050 для доступа к приложению
