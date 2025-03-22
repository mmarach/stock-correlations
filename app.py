from flask import Flask, render_template, url_for, request, jsonify
from forms import TickerForm
import json
import pandas as pd

from data.correlations import get_correlation_matrix, PriceType

pd.options.display.float_format = "{:,.2f}".format

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

        return correlation_matrix.to_html(classes="corr-table")  # Directly return the HTML table

    # If form is invalid, return the form's errors
    errors = []
    for field_name, field_errors in form.errors.items():
        for error in field_errors:
            errors.append(f"{field_name}: {error}")

    # Return a detailed error message
    return "<p>" + "<br>".join(errors) + "</p>", 400


if __name__ == '__main__':
    app.run(debug=True)
