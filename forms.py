from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, DateField
from wtforms.validators import DataRequired


class TickerForm(FlaskForm):
    start_date = DateField(label="Start Date", format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField(label="End Date", format='%Y-%m-%d', validators=[DataRequired()])
    tickerInput = StringField(label='Add Stock Ticker')
    tickers = HiddenField(validators=[DataRequired()])  # Hidden field to store all tickers
    submit = SubmitField(label='Submit')
