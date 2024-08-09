#!/usr/bin/python3
""" Main 3
"""
from flask import Flask, request, jsonify
from api.v1.auth.session_auth import SessionAuth
from models.user import User
import os
import json


""" Create a user test """
user = User()
user.email = "usession@hbtn.io"
user.password = "pwdsession"
user.save()


""" Create a session ID """
session_auth = SessionAuth()
session_id = session_auth.create_session(user.id)


""" Save in file session ID and user ID """
with open("session_id_hbtn.json", "w") as file:
    json.dump({'user_id': user.id, 'session_id': session_id}, file)


""" Flask App """
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def root_path():
    """ Root path
    """
    user_request = session_auth.current_user(request)
    if user_request is None:
        return jsonify({})
    return jsonify({'user_id': user_request.id})


if __name__ == "__main__":
    host = os.environ.get("API_HOST", "0.0.0.0")
    port = os.environ.get("API_PORT", "5000")
    app.run(host=host, port=port)
