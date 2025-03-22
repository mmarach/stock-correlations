from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, HiddenField, SubmitField, DateField
from wtforms.validators import DataRequired


class TickerForm(FlaskForm):
    tickers = HiddenField(validators=[DataRequired()])  # Hidden field to store all tickers
    start_date = DateField("Start Date", format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField("End Date", format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')
