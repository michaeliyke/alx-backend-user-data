#!/usr/bin/env python3
"""Module manage the API authentication."""
from flask import request
from typing import List, TypeVar, Tuple
from api.v1.auth.auth import Auth
import base64
from models.user import User

user = TypeVar('User')


class BasicAuth(Auth):
    """Basic Auth class implements basic authentication."""

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> user:
        """Returns the User instance based on email and password."""
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None
        user = User.search({'email': user_email})
        if not user:
            return None
        user = user[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> Tuple[str, str]:
        """Extracts the user credentials from the base64 decoded value.
        Returns the user email and password from the Base64 decoded value.
        """
        if not decoded_base64_authorization_header:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """Decodes a base64 string to get the encoded bytes."""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            byte_obj = base64.b64decode(base64_authorization_header)
            return byte_obj.decode('utf-8')
        except Exception as err:
            return None

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracts the base64 part of the Authorization header."""
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]
