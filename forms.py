from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, DateField
from wtforms.validators import DataRequired, ValidationError


class TickerForm(FlaskForm):
    start_date = DateField(label="Start Date", format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField(label="End Date", format='%Y-%m-%d', validators=[DataRequired()])
    tickerInput = StringField(label='Add Stock Ticker')
    tickers = HiddenField(validators=[DataRequired()])  # Hidden field to store all tickers
    submit = SubmitField(label='Submit')

    def validate_end_date(self, filed):
        if filed.data <= self.start_date.data:
            raise ValidationError('Finish date must more or equal start date.')
