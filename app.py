import json
import pandas as pd

from flask import Flask, render_template, request, jsonify

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
    if form.validate_on_submit():
        tickers = json.loads(form.tickers.data)
        start_date = form.start_date.data
        end_date = form.end_date.data
        use_returns = form.use_returns.data
        use_adjusted = form.use_adjusted.data

        correlation_matrix = get_correlations_matrix(tickers, start_date, end_date, use_adjusted, use_returns)
        return correlation_matrix.to_html(classes="corr-table")  # Directly return the HTML table

    # If form is invalid, return the form's errors
    errors = []
    for field_name, field_errors in form.errors.items():
        for error in field_errors:
            errors.append(f"{field_name}: {error}")

    # Return a detailed error message
    return "<p>" + "<br>".join(errors) + "</p>", 400


@app.route('/verify', methods=['POST'])
def verify_ticker():
    ticker = request.json.get("ticker", "").strip().upper()

    if not ticker.isalpha():
        error_message = "Invalid ticker: Make sure the ticker contains only alpha characters and no spaces."
        return render_template("error.html", error_message=error_message), 400

    if not check_ticker_in_yf(ticker):
        error_message = "Invalid ticker: Ticker isn't available in Yahoo Finance."
        return render_template("error.html", error_message=error_message), 400

    return jsonify({"valid": True})


if __name__ == '__main__':
    app.run(debug=True)
