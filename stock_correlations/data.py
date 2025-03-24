from typing import Any, Optional

from datetime import date

import pandas as pd

import yfinance as yf


def get_correlations_matrix(
        tickers: list[str],
        start_dt: date,
        end_dt: date,
        adjust_for_corp_actions: bool = True,
        use_price_returns: bool = True
) -> pd.DataFrame:
    """
    Computes the correlation matrix for a given set of stock tickers over a specified date
    range, using stock prices retrieved from Yahoo Finance.

    - If 'use_adjusted' is True, the function uses adjusted closing prices, accounting for
      applicable splits and dividend distributions. Otherwise, unadjusted closing prices
      are used.
    - If 'use_returns' is True, the function computes correlation based on daily returns
      instead of raw prices.
    """
    data = _fetch_stock_prices(tickers, start_dt, end_dt)

    data = data["Adj Close"] if adjust_for_corp_actions else data["Close"]
    if use_price_returns:
        data = data.pct_change()

    correlations = data.corr()
    correlations.index.name = None
    return correlations


def get_yf_ticker_info(ticker: str) -> Optional[dict[str, Any]]:
    """Fetches ticker information from Yahoo Finance."""
    # The 'yfinance' library can behave inconsistently, sometimes simply returning None when
    # the specified ticker is not found Yahoo Finance's database, and sometimes raising an
    # AttributeError. To handle this, we catch the exception and return None.
    try:
        yf_ticker = yf.Ticker(ticker)
        yf_ticker_info = yf_ticker.get_info()
        return yf_ticker_info
    except AttributeError:
        return None


def _fetch_stock_prices(tickers: list[str], start_dt: date, end_dt: date) -> pd.DataFrame:
    raw = yf.download(tickers, start=start_dt, end=end_dt, progress=False, auto_adjust=False)
    return raw


if __name__ == "__main__":
    stock_tickers = ["AAPL", "MZN", "META", "GOOG", "NFLX"]
    start_date = date(2024, 12, 1)
    end_date = date(2024, 12, 31)

    corr_matrix = get_correlations_matrix(stock_tickers, start_date, end_date)
    print(corr_matrix)
