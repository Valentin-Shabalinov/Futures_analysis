import pytest
import pandas as pd
from sqlalchemy import create_engine


def get_db_connection():
    # Database connection string
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
    """Test the database connection."""
    assert db_connection is not None


def test_read_data(db_connection):
    """Test reading data from a table."""
    query = "SELECT * FROM btc_data LIMIT 10"
    df = pd.read_sql_query(query, db_connection)
    assert len(df) > 0
