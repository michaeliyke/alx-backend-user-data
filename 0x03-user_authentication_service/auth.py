#!/usr/bin/env python3
"""
Module for the DB management class
"""
from db import DB
import bcrypt  # type: ignore
from user import User
import uuid
from sqlalchemy.orm.exc import NoResultFound  # type: ignore


def _hash_password(password: str) -> bytes:
    """
    Hashes the input password using bcrypt
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def _generate_uuid() -> str:
    """
    Generates a new UUID and returns it as a string.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def create_session(self, email: str) -> str:
        """
        Creates a new session for the user with the given email.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
        except NoResultFound:
            return None
        return session_id

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates the login credentials for the given email and password.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode(), user.hashed_password)

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with the given email and password.
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            user = None
        if user:
            raise ValueError(f"User {email} already exists.")

        return self._db.add_user(email, _hash_password(password))

    def __init__(self):
        self._db = DB()
