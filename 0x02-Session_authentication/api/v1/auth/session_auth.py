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
from uuid import uuid4, UUID
from typing import Union
from models.user import User


class SessionAuth(Auth):
    """Session auth wrapper around the Auth class"""
    user_id_by_session_id = {}

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value."""
        if request is None:
            return None
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        return User.get(user_id)

    def user_id_for_session_id(self, session_id: Union[str, UUID] = None)\
            -> str:
        """Returns user id based on session id"""
        if session_id is None:
            return None
        if type(session_id) is not str:
            if type(session_id) is not UUID:
                return None
            session_id = str(session_id)
        return self.user_id_by_session_id.get(session_id, None)

    def create_session(self, user_id: str = None) -> str:
        """Creates session id from user id"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = uuid4()
        self.user_id_by_session_id[str(session_id)] = user_id
        return session_id

    def destroy_session(self, request=None):
        """Deletes the user session / logout"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
