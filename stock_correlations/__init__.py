import os

import pandas as pd

from flask import Flask


pd.options.display.float_format = "{:,.2f}".format

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# app.config['WTF_CSRF_ENABLED'] = False


from stock_correlations import routes
