#!/usr/bin/python3
from flask import Flask
"""
starts a Flask web application listening on any IP port 5000.
"""
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """Sends the string 'Hello BNB!' to the browser"""
    return "Hello HBNB!"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
