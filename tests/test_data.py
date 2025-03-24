import pytest
from unittest.mock import patch

from pathlib import Path

from datetime import date

import pandas as pd

from stock_correlations.data import get_correlations_matrix


ROOT = "stock_correlations.data"
RESOURCES = Path("resources")


def read_multiindex_data(filename: str) -> pd.DataFrame:
    data = pd.read_json(RESOURCES / filename)
    data.columns = data.columns.str.split(", ", expand=True)
    data.index = pd.to_datetime(data.index)
    return data


@pytest.fixture(scope="session")
def mock_stock_data():
    return read_multiindex_data("mock_stock_prices.json")


@pytest.fixture
def mock_fetch_stock_prices(mock_stock_data):
    with patch(f"{ROOT}._fetch_stock_prices", return_value=mock_stock_data):
        yield


def test_get_correlations_matrix(mock_fetch_stock_prices):
    mock_tickers = ["FOO", "BAR"]
    mock_start_dt = date(2024, 12, 1)
    mock_end_dt = date(2024, 12, 14)

    # Test using adjusted closing prices and computing correlations on daily returns
    corr = get_correlations_matrix(
        mock_tickers, mock_start_dt, mock_end_dt, adjust_for_corp_actions=True, use_price_returns=True
    )

    assert corr.loc["FOO", "BAR"] == pytest.approx(-0.48272668, rel=1e-6)

    # Test using unadjusted closing prices and computing correlations on daily returns
    corr = get_correlations_matrix(
        mock_tickers, mock_start_dt, mock_end_dt, adjust_for_corp_actions=False, use_price_returns=True
    )

    assert corr.loc["FOO", "BAR"] == pytest.approx(-0.48272723, rel=1e-6)

    # Test using unadjusted closing prices and computing correlations on raw price values
    corr = get_correlations_matrix(
        mock_tickers, mock_start_dt, mock_end_dt, adjust_for_corp_actions=False, use_price_returns=False
    )

    assert corr.loc["FOO", "BAR"] == pytest.approx(0.8244538, rel=1e-6)
