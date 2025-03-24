from typing import Any, Optional

from datetime import date

import pandas as pd

import yfinance as yf


def get_correlations_matrix(
        tickers: list[str], start_dt: date, end_dt: date, use_adjusted: bool = True, use_returns: bool = True
) -> pd.DataFrame:
    """
    Computes the correlation matrix for a given set of stock tickers over a specified date range,
    using stock prices retrieved from Yahoo Finance.

    @param tickers: List of stock ticker symbols to include in the correlation matrix.
    @param start_dt: The start date for the calculations date range.
    @param end_dt: The end date for the calculations date range.
    @param use_adjusted: If True, adjusted closing prices are used, accounting for applicable splits and dividend distributions.
                         If False, unadjusted closing prices are used.
    @param use_returns: If True, computes correlation on daily returns. Otherwise, raw price values are used.
    @return: Dataframe with correlations between the input tickers.
    """
    data = _fetch_stock_prices(tickers, start_dt, end_dt, use_adjusted)

    if use_returns:
        data = data.pct_change()
    correlations = data.corr()

    correlations.index.name = None
    return correlations


def _fetch_stock_prices(tickers: list[str], start_dt: date, end_dt: date, use_adjusted: bool) -> pd.DataFrame:
    raw = yf.download(tickers, start=start_dt, end=end_dt, progress=False, auto_adjust=False)
    prices = raw['Adj Close'] if use_adjusted else raw['Close']
    return prices


def get_yf_ticker_info(ticker: str) -> Optional[dict[str, Any]]:
    try:
        yf_ticker = yf.Ticker(ticker)
        yf_ticker_info = yf_ticker.get_info()
        return yf_ticker_info
    except AttributeError:
        return None


if __name__ == '__main__':
    stock_tickers = ['AAPL', 'AMZN', 'META', 'GOOG', 'NFLX']
    start_date = date(2024, 12, 1)
    end_date = date(2024, 12, 31)

    corr_matrix = get_correlations_matrix(stock_tickers, start_date, end_date)
    print(corr_matrix)
