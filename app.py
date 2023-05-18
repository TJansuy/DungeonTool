#!/usr/bin/env python3

# Imports

from flask import Flask
from flask import send_file

# Init Flask Server
app = Flask(__name__)

# Helper Functions

# Routes

@app.route("/test")
def test():
  return "<p>Your Princess is in another castle</p>"

@app.route("/delayed")
def delayed_response():
    import time
    time.sleep(10)
    return send_file("test_image.png", mimetype="image/png")
