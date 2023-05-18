#!/usr/bin/env python3

# Imports

from flask import Flask

# Init Flask Server
app = Flask(__name__)

# Helper Functions

# Routes

@app.route("/test")
def test():
  return "<p>Your Princess is in another castle</p>"
