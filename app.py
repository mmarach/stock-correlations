from datetime import date

import json
import pandas as pd

from flask import Flask, render_template, request

from forms import TickerForm

from data.correlations import get_correlations_matrix, check_ticker_in_yf


pd.options.display.float_format = "{:,.2f}".format

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False


@app.route('/')
@app.route('/home')
def home():
    """Show the main Home page."""
    form = TickerForm()
    return render_template('home.html', form=form)


@app.route('/about')
def about():
    """Show an overview on how to use and navigate Diary Dash."""
    return render_template('about.html', title='About')


@app.route('/submit', methods=['POST'])
def submit():
    form = TickerForm()
    # if form.validate_on_submit():
    tickers = json.loads(form.tickers.data)
    if len(tickers) < 2:
        return input_error("Invalid input: Two or more tickers have to be provided.")

    start_date = form.start_date.data
    end_date = form.end_date.data
    if end_date <= start_date:
        return input_error("Invalid input: The end date must be later than the start date.")
    elif end_date > date.today():
        return input_error("Invalid input: The end date cannot be in the future.")

    use_returns = form.use_returns.data
    use_adjusted = form.use_adjusted.data

    correlation_matrix = get_correlations_matrix(tickers, start_date, end_date, use_adjusted, use_returns)
    return correlation_matrix.to_html(classes="corr-table")  # Directly return the HTML table


@app.route('/verify', methods=['POST'])
def verify_ticker():
    ticker = request.json.get("ticker", "")

    if not ticker.isalpha():
        return input_error("Invalid ticker: Make sure the ticker contains only alpha characters and no spaces.")

    if not check_ticker_in_yf(ticker):
        return input_error("Invalid ticker: The ticker isn't available in Yahoo Finance.")

    return ""


def input_error(error_message: str) -> tuple[str, int]:
    return render_template("error.html", error_message=error_message), 400


if __name__ == '__main__':
    app.run(debug=True)
