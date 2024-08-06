#!/usr/bin/env python3
"""Module manage the API authentication."""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic Auth class implements basic authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns True if the path is not in the list of excluded paths
        This will enable auth for the path
        Must be slash tolerant: path=/api/v1/status and path=/api/v1/status/
        should be considered the same path

        if not path or not excluded_paths:
            return True

        # Make sure the path ends with a '/'
        if path[-1] != '/':
            path += '/'

        # Make sure all excluded paths end with a '/'
        for i in range(len(excluded_paths)):
            if excluded_paths[i][-1] != '/':
                excluded_paths[i] += '/'

        # Finally, check if the path is excluded from auth
        for excluded_path in excluded_paths:
            if excluded_path == path:
                return False
        # path isn't excluded, so auth is required
        return True
        """
