#!/usr/bin/env python3

# Imports

from flask import Flask
from flask import send_file
from flask import request

# Init Flask Server
app = Flask(__name__)

# Helper Functions

# Routes

@app.route("/test")
def test():
  return "<p>Your Princess is in another castle</p>"

@app.route("/delayed")
def delayed_response():

    print("args: ",request.args,"\nheaders: ", request.headers,"\norigin: " , request.origin,"\nremote_addr: " ,request.remote_addr)
    import time
    sleep_time = 10
    print("Sleep timer started!", sleep_time,"seconds")
    time.sleep(sleep_time)
    print("Timer done!")

    return send_file("test_image.png", mimetype="image/png")
