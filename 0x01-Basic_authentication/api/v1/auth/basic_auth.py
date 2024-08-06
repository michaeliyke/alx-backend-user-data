#!/usr/bin/env python3
"""Module manage the API authentication."""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """Basic Auth class implements basic authentication."""

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
