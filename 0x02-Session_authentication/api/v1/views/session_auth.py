#!/usr/bin/env python3
"""Session auth module for the api
"""
from flask import request, jsonify, make_response, current_app
from models.user import User
from api.v1.views import app_views
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """Authenticates a user and creates a session
    """
    from api.v1.app import auth

    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    user_dict = user.to_json()

    response = jsonify(user_dict)
    response.set_cookie(os.getenv('SESSION_NAME'), str(session_id))

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def auth_session_logout():
    """Deletes a session and logs out the user
    """
    from api.v1.app import auth

    session_id = request.cookies.get(os.getenv('SESSION_NAME'))
    if not session_id:
        return jsonify({}), 404
    if not auth.destroy_session(request):
        return jsonify({}), 404
    return jsonify({}), 200
