import pandas as pd

from flask import Flask

from stock_correlations.config import Config


pd.options.display.float_format = "{:,.2f}".format


def create_app(app_config=Config):
    app = Flask(__name__)
    app.config.from_object(app_config)

    from stock_correlations.routes import register_routes
    register_routes(app)

    return app
