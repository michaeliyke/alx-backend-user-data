#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = os.getenv('AUTH_TYPE', None)

if auth:
    from api.v1.auth.basic_auth import BasicAuth
    from api.v1.auth.auth import Auth
    from api.v1.auth.session_auth import SessionAuth

    if auth == 'basic_auth':
        auth = BasicAuth()
    elif auth == 'session_auth':
        auth = SessionAuth()
    else:
        auth = Auth


@app.before_request
def before_request():
    """ Before request
    """
    if auth:
        request.current_user = auth.current_user(request)
    excluded = [
        '/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/',
        '/api/v1/auth_session/login/']
    # if auth is needed i.e is specified in the environment variable, and
    # path is not excluded from auth
    requires_auth = auth.require_auth(request.path, excluded)
    if auth and requires_auth:
        has_authorization = auth.authorization_header(request)
        has_cookie = auth.session_cookie(request)
        is_valid_user = auth.current_user(request)
        if has_cookie(request):
            return
        # if request contains no Authorization header, disallow it
        if not has_authorization:
            abort(401)
        # If request user isn't authenticated, disallow it
        if not is_valid_user:
            abort(403)


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
