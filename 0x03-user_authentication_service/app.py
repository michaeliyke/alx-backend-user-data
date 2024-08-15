#!/usr/bin/env python3
"""Module for a simple flask app"""
from flask import Flask, jsonify, make_response

app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def homepage():
    """The homepage function"""
    return make_response(jsonify({"message": "Bienvenue"}), 200)


@app.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """The status function"""
    return make_response(jsonify({"status": "Ok"}), 200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
