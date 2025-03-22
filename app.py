from flask import Flask, render_template, url_for, request, jsonify
from forms import TickerForm
import json

from data.correlations import get_correlation_matrix, PriceType

app = Flask(__name__)

app.config['WTF_CSRF_ENABLED'] = False


@app.route('/', methods=['GET'])
def index():
    form = TickerForm()
    return render_template('index.html', form=form)


@app.route('/submit', methods=['POST'])
def submit():
    form = TickerForm()
    if form.validate_on_submit():
        tickers = json.loads(form.tickers.data)
        start_date = form.start_date.data
        end_date = form.end_date.data
        correlation_matrix = get_correlation_matrix(tickers, start_date, end_date, PriceType.CLOSE)

        correlation_matrix.style.background_gradient()

        return correlation_matrix.to_html(classes="corr-table")  # Directly return the HTML table

    return "<p>Error: Invalid submission</p>", 400


# @app.route('/add_ticker', methods=['POST'])
# def add_ticker():
#     ticker = request.json.get('ticker', '').strip().upper()
#     return jsonify({'ticker': ticker})  # Return cleaned ticker


if __name__ == '__main__':
    app.run(debug=True)
