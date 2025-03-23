import os

import pandas as pd

from flask import Flask

from stock_correlations.config import Config


pd.options.display.float_format = "{:,.2f}".format


def create_app(app_config=Config):
    app = Flask(__name__)

    app.config.from_object(app_config)

    with app.app_context():
        from stock_correlations import routes

    return app
