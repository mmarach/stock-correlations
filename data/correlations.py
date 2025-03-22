from enum import Enum

from datetime import date

import pandas as pd

import yfinance as yf


class PriceType(Enum):
    OPEN = 'Open'
    CLOSE = 'Close'
    HIGH = 'High'
    LOW = 'Low'


def get_stock_prices(stocks: list[str], start_dt: date, end_dt: date, price_type: PriceType) -> pd.DataFrame:
    res = yf.download(stocks, start=start_dt, end=end_dt, progress=False)
    prices = res[price_type.value]
    return prices


def calculate_correlations(stock_prices: pd.DataFrame) -> pd.DataFrame:
    daily_returns = stock_prices.pct_change()
    correlations = daily_returns.corr()
    return correlations


def get_correlation_matrix(stocks: list[str], start_dt: date, end_dt: date, price_type: PriceType) -> pd.DataFrame:
    stock_prices = get_stock_prices(stocks, start_dt, end_dt, PriceType.CLOSE)
    corr_matrix = calculate_correlations(stock_prices)

    corr_matrix.index.name = None
    return corr_matrix


if __name__ == '__main__':
    faang_stocks = ['AAPL', 'AMZN', 'META', 'GOOG', 'NFLX']
    start_date = date(2022, 5, 1)
    end_date = date(2022, 5, 31)

    out = get_stock_prices(faang_stocks, start_date, end_date, PriceType.CLOSE)
    print(out)

    corrs = calculate_correlations(out)
    print(corrs)
