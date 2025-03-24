### Stock Correlations App
Stock Correlations is a web app built with Flask. The app calculates correlations between selected stocks.

The app utilises Yahoo's publicly available APIs to obtain historical price data from Yahoo Finance using which the 
correlations are computed. For more information on Yahoo's APIs, see https://developer.yahoo.com/api/.

### Installation

To install all required dependencies, run:
```bash
pip install -r requirements.txt
```

### App Structure

```
|──────stock_correlations/
| |──────__init__.py
| |──────config.py
| |──────data.py
| |──────forms.py
| |──────routes.py
| |──────templates/
| | |──────about.html
| | |──────home.html
| | |──────layout.html
| |──────static/
| | |──────main.css
| |──────tests/
|──────app.py
|──────README.md
|──────requirements.txt
```

### App Configuration
The app's configuration is set in `config.py`. You can modify it to suit your requirements.

**Note**: Flask-WTF enables CSRF protection by default. If you're running the app locally, you may need to disable CSRF 
protection, add the following in `config.py`:
```
WTF_CSRF_ENABLED = False
```

### Running the App

To start locally the Flask development server, run:
```
python app.py
```
or:
```
flask run
```

You can use `flask --debug` to run the app in debug mode. 

By default, Flask runs on port `5000`:
```
http://127.0.0.1:5000/
```

### Running Unit Tests

To execute all tests, run:
```
pytest tests/
```

For more detailed test output, use `pytest -v`.
