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


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """User password update endpoint function"""
    try:
        email = request.form.get("email") or request.json.get("email")
        reset_token = request.form.get("reset_token") or request.json.get(
            "reset_token")
        new_password = request.form.get("new_password") or request.json.get(
            "new_password")

        AUTH.update_password(reset_token, new_password)
        return make_response(jsonify({
            "email": email,
            "message": "Password updated",
        }), 200)
    except Exception:
        abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def reset_password() -> str:
    """User reset password endpoint function - returns the token"""
    try:
        email = request.form.get("email") or request.json.get("email")
        reset_token = AUTH.get_reset_password_token(email)
    except Exception as e:
        abort(403)
    return make_response(jsonify({
        "email": email,
        "reset_token": reset_token,
    }), 200)


@ app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """User profile endpoint function"""
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return make_response(jsonify({
                "email": user.email,
            }), 200)
    abort(403)


@ app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """User logout endpoint function"""
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect("/")
    abort(403)


@ app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """User login endpoint function"""
    email = request.form.get("email") or request.cookies.get(
        "email") or request.json.get("email")
    password = request.form.get("password") or request.cookies.get(
        "password") or request.json.get("password")

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = make_response(jsonify({
            "message": "logged in",
            "email": email,
        }), 200)
        response.set_cookie("session_id", session_id)
        return response
    abort(401)


@ app.route("/", methods=["GET"], strict_slashes=False)
def homepage() -> str:
    """The homepage endpoint function"""
    return make_response(jsonify({"message": "Bienvenue"}), 200)


@ app.route("/status", methods=["GET"], strict_slashes=False)
def status() -> str:
    """/status endpoint function"""
    return make_response(jsonify({"status": "Ok"}), 200)


@ app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """User registeration endpoint function"""
    email = request.form.get("email") or request.json.get("email")
    password = request.form.get("password") or request.json.get("password")

    try:
        AUTH.register_user(email, password)
        return (jsonify({"email": email, "message": "user created"}), 200)
    except ValueError:
        return (jsonify({"message": "email already registered"}), 400,)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
