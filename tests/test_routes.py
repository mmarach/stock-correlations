import pytest
from unittest.mock import patch

from datetime import date, timedelta

import json
import pandas as pd

from stock_correlations import create_app


ROOT = "stock_correlations.routes"


class MockConfig:
    WTF_CSRF_ENABLED = False


@pytest.fixture
def mock_client():
    app = create_app(MockConfig)
    app.config.update(TESTING=True)

    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_get_correlations_matrix():
    mock_corr_matrix = pd.DataFrame().corr()
    with patch(f"{ROOT}.get_correlations_matrix", return_value=mock_corr_matrix):
        yield


@pytest.fixture
def mock_get_yf_ticker_info():
    def side_effect(ticker):
        if ticker == "BAR":
            return {"sector": "Technology"}
        elif ticker == "BAZ":
            return None
        return {"sector": "Technology", "regularMarketPrice": 100.0}

    with patch(f"{ROOT}.get_yf_ticker_info", side_effect=side_effect):
        yield


def test_home(mock_client):
    response = mock_client.get("/")
    assert response.status_code == 200
    assert response.content_type == "text/html; charset=utf-8"


def test_about(mock_client):
    response = mock_client.get("/about")
    assert response.status_code == 200
    assert response.content_type == "text/html; charset=utf-8"


def test_submit_form(mock_client, mock_get_correlations_matrix):
    # Test submitting valid data and receiving the correlation matrix
    mock_form = {
        "tickers": json.dumps(["FOO", "BAR"]),
        "start_date": (date.today() - timedelta(days=30)).isoformat(),
        "end_date": date.today().isoformat(),
        "use_returns": True,
        "use_adjusted": False
    }
    response = mock_client.post("/submit", json=mock_form)

    assert response.status_code == 200
    assert b'class="dataframe corr-table"' in response.data

    # Test submitting an invalid date range (end_date before start_date)
    mock_form["start_date"] = date.today().isoformat()
    mock_form["end_date"] = (date.today() - timedelta(days=1)).isoformat()

    response = mock_client.post("/submit", json=mock_form)

    assert response.status_code == 400
    assert b"Invalid input: The end date must be later than the start date." in response.data

    # Test submitting an invalid (future) end date
    mock_form["end_date"] = (date.today() + timedelta(days=1)).isoformat()

    response = mock_client.post("/submit", json=mock_form)

    assert response.status_code == 400
    assert b"Invalid input: The end date cannot be in the future." in response.data

    # Test submitting fewer than two tickers
    mock_form["tickers"] = json.dumps(["FOO"])

    response = mock_client.post("/submit", json=mock_form)

    assert response.status_code == 400
    assert b"Invalid input: Two or more tickers have to be provided." in response.data


def test_verify_ticker(mock_client, mock_get_yf_ticker_info):
    # Test that a valid ticker returns an empty response
    response = mock_client.post("/verify", json={"ticker": "FOO"})

    assert response.status_code == 200
    assert b"" in response.data

    # Test submitting an already selected ticker
    response = mock_client.post("/verify", json={"ticker": "FOO", "selected_tickers": ["FOO", "BAR"]})

    assert response.status_code == 400
    assert b"Ticker FOO has already been selected." in response.data

    # Test submitting an invalid ticker containing non-alpha characters
    response = mock_client.post("/verify", json={"ticker": "FOO123"})

    assert response.status_code == 400
    assert b"Invalid ticker: Make sure the ticker contains only alpha characters and no spaces." in response.data

    # Test submitting a ticker without price data in Yahoo Finance's database
    response = mock_client.post("/verify", json={"ticker": "BAR"})

    assert response.status_code == 400
    assert b"Invalid ticker: The ticker is not available in Yahoo Finance." in response.data

    # Test submitting a ticker not found in Yahoo Finance's database
    response = mock_client.post("/verify", json={"ticker": "BAZ"})

    assert response.status_code == 400
    assert b"Invalid ticker: The ticker is not available in Yahoo Finance." in response.data
