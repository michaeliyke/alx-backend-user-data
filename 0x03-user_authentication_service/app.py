#!/usr/bin/env python3
"""Module for a simple flask app"""
from flask import (
    Flask,
    jsonify,
    make_response,
    request,
    abort,
    redirect,
)
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def reset_password() -> str:
    """/reset_password endpoint function"""
    try:
        email = request.form.get("email")
        reset_token = AUTH.generate_reset_token(email)
    except ValueError:
        abort(403)
    return make_response(jsonify({
        "email": email,
        "reset_token": reset_token,
    }), 200)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """/profile endpoint function"""
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return make_response(jsonify({
                "email": user.email,
            }), 200)
    abort(403)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """/sessions endpoint function to logout"""
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect("/")
    abort(403)


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """/sessions endpoint function"""
    email = request.form.get("email")
    password = request.form.get("password")

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = make_response(jsonify({
            "message": "logged in",
            "email": email,
        }), 200)
        response.set_cookie("session_id", session_id)
        return response
    abort(401)


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
