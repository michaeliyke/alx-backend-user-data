#!/usr/bin/env python3
"""
Module for the DB management class
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hashes the input password using bcrypt
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password
