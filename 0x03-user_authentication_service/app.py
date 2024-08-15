#!/usr/bin/env python3
"""Module for a simple flask app"""
from flask import Flask, jsonify, make_response, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def homepage() -> str:
    """The homepage endpoint function"""
    return make_response(jsonify({"message": "Bienvenue"}), 200)


@app.route("/status", methods=["GET"], strict_slashes=False)
def status() -> str:
    """/status endpoint function"""
    return make_response(jsonify({"status": "Ok"}), 200)


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """/users endpoint function"""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
        return (jsonify({"email": email, "message": "user created"}), 200)
    except ValueError:
        return (jsonify({"message": "email already registered"}), 400,)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
