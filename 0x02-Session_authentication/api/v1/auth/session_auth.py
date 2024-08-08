#!/usr/bin/env python3
"""
Session auth module for the api
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.basic_auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """Session auth wrapper around the Auth class"""
    user_id_by_session_id = {}

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns user id based on session id"""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def create_session(self, user_id: str = None) -> str:
        """Creates session id from user id"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = uuid4()
        self.user_id_by_session_id[session_id] = user_id
        return session_id
