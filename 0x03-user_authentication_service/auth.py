#!/usr/bin/env python3
"""
Module for the DB management class
"""
from db import DB
import bcrypt
from user import User
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hashes the input password using bcrypt
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with the given email and password.
        """
        # Check if user already exists
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            user = None
        if user:
            raise ValueError(f"User {email} already exists.")

        # Hash the password
        hashed_password = _hash_password(password)

        # Save the user to the database
        user = User(email=email, hashed_password=hashed_password)
        self._db.add_user(email, hashed_password)
        return user

    def __init__(self):
        self._db = DB()
