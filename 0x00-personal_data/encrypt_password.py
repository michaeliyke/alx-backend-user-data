import bcrypt

#!/usr/bin/env python3
"""Alx Backend User Data module"""


def hash_password(password: str) -> bytes:
    """Hashes a password and returns a salted hash"""
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password with the generated salt
    return bcrypt.hashpw(password.encode(), salt)
