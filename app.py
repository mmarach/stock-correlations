from flask import Flask, render_template
import yfinance as yf

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def hello():
    ticker = yf.Ticker("AAPL")
    info = ticker.info
    return render_template("index.html", value=info["regularMarketPrice"])


@app.route("/about")
def about():
    return "About Page"


if __name__ == '__main__':
    app.run(debug=True)
