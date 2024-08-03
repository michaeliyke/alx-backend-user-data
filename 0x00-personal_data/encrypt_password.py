import bcrypt

#!/usr/bin/env python3
"""Alx Backend User Data module"""


def hash_password(password: str) -> bytes:
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password with the generated salt
    return bcrypt.hashpw(password.encode(), salt)
