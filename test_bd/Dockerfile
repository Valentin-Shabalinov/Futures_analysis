# Используйте официальный образ Python 3.11
FROM python:3.11

# Устанавливаем зависимости для компиляции некоторых библиотек
RUN apt-get update && \
    apt-get install -y build-essential

# Устанавливаем необходимые библиотеки из системных пакетов
RUN pip install --no-cache-dir numpy psycopg2

WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем файлы приложения
COPY . .

# Команда для выполнения
CMD ["python", "test_bd.py"]

