import pytest
import pandas as pd
from sqlalchemy import create_engine


def get_db_connection():
    # Строка подключения к базе данных
    db_connection_string = (
        "postgresql://futures_user:aaa@postgres-db:5432/analys"
    )
    # db_connection_string = "postgresql://futures_user:082101@localhost:5432/analys"
    engine = create_engine(db_connection_string)
    return engine


@pytest.fixture
def db_connection():
    return get_db_connection()


def test_db_connection(db_connection):
    """Тестируем подключение к базе данных."""
    assert db_connection is not None


def test_read_data(db_connection):
    """Тестируем чтение данных из таблицы."""
    query = "SELECT * FROM btc_data LIMIT 10"
    df = pd.read_sql_query(query, db_connection)
    assert len(df) > 0
