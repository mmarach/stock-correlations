from typing import Optional

from datetime import date

import json

from flask import render_template, request

from stock_correlations.forms import CorrInputForm
from stock_correlations.data import get_correlations_matrix, get_yf_ticker_info


def register_routes(app):
    """Register all routes for the Flask app."""

    @app.route("/")
    @app.route("/home")
    def home():
        """Render the home page."""
        form = CorrInputForm()
        return render_template("home.html", form=form)


    @app.route("/about")
    def about():
        """Render the about page with overview of the app."""
        return render_template("about.html", title="About")


    @app.route("/submit", methods=["POST"])
    def submit_form():
        """Process the submitted form, validate input, and return a correlation matrix as HTML table."""
        form = CorrInputForm()

        tickers = json.loads(form.tickers.data)
        start_date = form.start_date.data
        end_date = form.end_date.data

        error = _validate_form_input(tickers, start_date, end_date)
        if error:
            return _input_error(error)

        use_price_returns = form.use_price_returns.data
        adjust_for_corp_actions = form.adjust_for_corp_actions.data

        correlation_matrix = get_correlations_matrix(
            tickers, start_date, end_date, adjust_for_corp_actions, use_price_returns
        )
        return correlation_matrix.to_html(classes="corr-table")


    @app.route("/verify", methods=["POST"])
    def verify_ticker():
        """Verify that the provided ticker is valid."""
        ticker = request.json.get("ticker", "")
        selected_tickers = request.json.get("selected_tickers", [])

        if ticker in selected_tickers:
            return _input_error(f"Ticker {ticker} has already been selected.")

        if not ticker.isalpha():
            return _input_error("Invalid ticker: Make sure the ticker contains only alpha characters and no spaces.")

        yf_ticker_info = get_yf_ticker_info(ticker)
        if not yf_ticker_info or "regularMarketPrice" not in yf_ticker_info:
            return _input_error("Invalid ticker: The ticker is not available in Yahoo Finance.")

        return ""


def _validate_form_input(tickers: list[str], start_date: date, end_date: date) -> Optional[str]:
    if len(tickers) < 2:
        return "Invalid input: Two or more tickers have to be provided."
    if end_date <= start_date:
        return "Invalid input: The end date must be later than the start date."
    if end_date > date.today():
        return "Invalid input: The end date cannot be in the future."
    return None


def _input_error(error_message: str) -> tuple[str, int]:
    return error_message, 400
