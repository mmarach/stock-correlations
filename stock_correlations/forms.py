from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField, DateField, BooleanField
from wtforms.validators import DataRequired


class CorrInputForm(FlaskForm):
    start_date = DateField(label="Start Date", format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField(label="End Date", format='%Y-%m-%d', validators=[DataRequired()])
    use_price_returns = BooleanField(label="Use Price Returns", default=True)
    adjust_for_corp_actions = BooleanField(label="Adjust for Corporate Actions", default=True)
    tickers = HiddenField()  # Hidden field to store all tickers
    submit = SubmitField(label='Submit')
