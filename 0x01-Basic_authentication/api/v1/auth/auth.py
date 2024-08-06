#!/usr/bin/env python3
"""Module manage the API authentication."""
from flask import request
from typing import List, TypeVar

User = TypeVar('User')


class Auth:
    """class to manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns True if the path is not in the list of excluded paths
        This will enable auth for the path
        Must be slash tolerant: path=/api/v1/status and path=/api/v1/status/
        should be considered the same path
        """

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
            # Handle allowing * at the end of excluded path
            if excluded_path[-1] == '*':
                # Confirm startswith
                if path.startswith(excluded_path[:-1]):
                    # Get the remaining string after current match
                    temp = path[len(excluded_path) - 1:]
                    # Ensure temp is not words
                    if len(temp.split()) < 2:
                        return False
                    # Confirm no more than one slashes in the remaining string
                    if temp.count('/') < 2:
                        return False
        # path isn't excluded, so auth is required
        return True

    def authorization_header(self, request=None) -> str:
        """
        Get the Authorization header from the request if reuired and available
        """
        # If auth is not required or not provided
        if request is None or 'Authorization' not in request.headers:
            return None
        # Return the provided auth
        return request.headers['Authorization']

    def current_user(self, request=None) -> User:
        """
        Check if there is an authenticated user
        """
        return None
