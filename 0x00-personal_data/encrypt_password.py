#!/usr/bin/env python3
"""Alx Backend User Data module"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password and returns a salted hash"""
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the generated salt
    return bcrypt.hashpw(password.encode(), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates if a password matches a hashed password"""
    # Check if the provided password matches the hashed password
    return bcrypt.checkpw(password.encode(), hashed_password)
