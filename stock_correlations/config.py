import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # If you want to run the app locally, you can disable the CSRF protection
    # by uncommenting the following line. Make sure to enable it again before
    # deploying to production.
    # WTF_CSRF_ENABLED = False
