Для создания приложения для анализа цен фьючерса ETHUSDT и определения его движения, исключив влияние цены BTCUSDT, можно использовать следующую архитектуру проекта:

## 1 Сбор данных:
Использование API криптобирж для получения исторических цен фьючерса ETHUSDT и BTCUSDT.
Регулярное обновление данных для актуальности анализа.
## 2 Предобработка данных:
Удаление выбросов и аномалий из исторических данных.
Выравнивание временных интервалов между ценами ETHUSDT и BTCUSDT.
Приведение данных к одному временному формату.
## 3 Расчет рендеров цен:
Использование метода расчета относительных изменений цен для создания временных рядов.
Рендер цен ETHUSDT и BTCUSDT в виде временных рядов для последующего анализа движения цен.
## 4 Удаление влияния BTCUSDT:
Применение статистических методов, таких как корреляционный анализ, для измерения связи между ценами ETHUSDT и BTCUSDT.
Выделение временных периодов, когда влияние BTCUSDT на цены ETHUSDT минимально.
## 5 Методика анализа движения цены ETHUSDT:
Использование технического анализа, включая индикаторы, свечной график и т.д.
Применение статистических моделей для прогнозирования будущих изменений цен.
## 6 Подбор параметров:
Определение оптимальных параметров для выбранных методов анализа.
Обучение моделей на исторических данных для оптимизации параметров.
## 7 Разработка приложения:
Создание пользовательского интерфейса для визуализации аналитических результатов.
Интеграция алгоритмов анализа и предсказания в приложение.
## 8 Тестирование и оптимизация:
Проведение тестов на исторических данных для оценки точности и эффективности аналитических методов.
Оптимизация алгоритмов для повышения производительности приложения.
Выбор методики и параметров будет зависеть от конкретных требований и характеристик данных. Например, для анализа цен могут быть использованы технические индикаторы, а для исключения влияния BTCUSDT - статистические методы анализа корреляции. Подбор параметров и оптимизация необходимы для достижения максимальной точности прогнозов.


/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" - установка homebrew
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/valentin/.zprofileeval "$(/opt/homebrew/bin/brew hellenv)" - установка настроек homebrew

brew install postgresql - установка postgresql

psql -U postgres - вход в psql (пароль: 0821)
\q - выход из postgres в терминале

deactivate - деактивация виртуального окружения
rm -rf venv - Удаление виртуального окружения


Ключ API: jjyn6AGhau51Mzpb

Секретный ключ API: rXmwagvlweDEYSQmWkcnuQoiGDv6eQ03

### https://scikit-learn.org/stable/ ML



timestamp: Временная метка для каждого момента времени.
open: Значение открытия ETH на момент времени.
high: Наивысшая цена ETH за период.
low: Наименьшая цена ETH за период.
close: Значение закрытия ETH на момент времени.
volume: Объем торгов ETH за период.

predicted_target: Это предсказанное значение целевой переменной, в данном случае, цены ETH на 1 неделю вперед.
target: Это фактическое (истинное) значение целевой переменной.


## Для определения собственных движений цены фьючерса ETHUSDT, исключая влияние цены BTCUSDT, вы можете использовать статистические методы и анализ корреляции.
Для использования статистических методов, таких как регрессионный анализ, для определения собственных движений цены фьючерса ETHUSDT, исключая влияние цены BTCUSDT, вам может потребоваться библиотека statsmodels для Python. 
Шаги и методики, которые использовались в этом:
-Сбор данных:
Получите исторические данные о ценах фьючерса ETHUSDT и BTCUSDT.
Обратите внимание на временные рамки, которые вы хотите анализировать (например, часовые, дневные, недельные данные).
-Корреляционный анализ:
Рассчитайте корреляцию между ценами ETHUSDT и BTCUSDT. Это может быть сделано с использованием статистических инструментов, таких как коэффициент корреляции Пирсона.
-Разделение движений:
Вычтите влияние цены BTCUSDT из цены ETHUSDT. Например, если вы обнаружили высокую положительную корреляцию, вы можете вычесть определенный процент (коэффициент корреляции) от цены BTCUSDT из цены ETHUSDT.
-Прогнозирование моделью:
Используйте методы машинного обучения для построения модели, которая может предсказывать движения цены ETHUSDT, исключая влияние BTCUSDT. Возможно, вам потребуется временные ряды и регрессионные методы.
-Визуализация:
Постройте графики для визуализации оставшихся движений цены ETHUSDT после исключения влияния BTCUSDT. Сравните их с фактическими ценами, чтобы убедиться в эффективности ваших методов.
-Обновление модели:
Периодически обновляйте свою модель, используя новые данные, чтобы она оставалась актуальной и способной адаптироваться к изменениям на рынке.
-Проверка статистической значимости:
Проверьте статистическую значимость полученных результатов, чтобы убедиться, что ваш подход действительно исключает влияние BTCUSDT и что изменения не случайны.
