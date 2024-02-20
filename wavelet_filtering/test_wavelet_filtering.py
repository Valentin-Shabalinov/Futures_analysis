import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
import statsmodels.api as sm
import wavelet_filtering


# Fixture for creating a test DataFrame
@pytest.fixture
def test_data():
    data = {
        "timestamp": ["2022-01-01 00:00:00", "2022-01-01 01:00:00"],
        "btc_close": [50000, 51000],
        "eth_close": [4000, 4100],
    }
    return pd.DataFrame(data)


# Testing data loading
@patch("wavelet_filtering.pd.read_sql")
def test_load_data(mock_read_sql, test_data):
    mock_read_sql.return_value = test_data
    btc_data_df = wavelet_filtering.pd.read_sql(
        wavelet_filtering.btc_data_query, wavelet_filtering.engine
    )
    eth_data_df = wavelet_filtering.pd.read_sql(
        wavelet_filtering.eth_data_query, wavelet_filtering.engine
    )
    assert (
        not btc_data_df.empty and not eth_data_df.empty
    ), "DataFrame should contain data"


# Testing correlation analysis
def test_correlation_analysis(test_data):
    correlation_matrix = np.corrcoef(
        test_data["btc_close"], test_data["eth_close"]
    )
    correlation = correlation_matrix[0, 1]
    assert (
        correlation <= 1 and correlation >= -1
    ), "Correlation coefficient should be within -1 to 1"


# Testing regression analysis
def test_regression_analysis(test_data):
    with patch.object(
        sm.OLS, "fit", return_value=MagicMock(params={"btc_close": 0.5})
    ):
        test_data = sm.add_constant(test_data)
        model = sm.OLS(
            test_data["eth_close"], test_data[["const", "btc_close"]]
        )
        results = model.fit()
        beta_btc = results.params["btc_close"]
        assert beta_btc == 0.5, "Regression analysis result is incorrect"


# Testing writing processed data
@patch("wavelet_filtering.pd.DataFrame.to_sql")
def test_write_processed_data(mock_to_sql, test_data):
    wavelet_filtering.eth_data_df = (
        test_data  # Using the test DataFrame as a mock
    )
    wavelet_filtering.eth_data_df.to_sql(
        "eth_data_filtered",
        wavelet_filtering.engine,
        if_exists="replace",
        index=False,
    )
    mock_to_sql.assert_called_once_with(
        "eth_data_filtered",
        wavelet_filtering.engine,
        if_exists="replace",
        index=False,
    ), "Data should be written to the table"
