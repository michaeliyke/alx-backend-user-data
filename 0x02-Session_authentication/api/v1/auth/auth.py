#!/usr/bin/env python3
"""Module manage the API authentication."""
from flask import request
from typing import List, TypeVar
import os

User = TypeVar('User')


class Auth:
    """class to manage the API authentication"""

    def session_cookie(self, request=None):
        """Get the session cookie from the request"""
        if request is None:
            return None
        cookie_name = os.getenv('SESSION_NAME')
        return request.cookies.get(cookie_name)

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines whether authentication is required for a given path.

        Returns True if the path is not in the list of excluded paths,
        enabling authentication for the path. Handles paths that end with
        or without a slash interchangeably and supports wildcard '*' at
        the end of excluded paths.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths to exclude from auth.

        Returns:
            bool: True if authentication is required, False otherwise.
    """

        if not path or not excluded_paths:
            return True

        # Enure the path ends with a '/'
        path = path if path.endswith('/') else path + '/'

        # Enure all excluded paths end with a '/'
        normalized_paths = [
            p if p.endswith('/') or p.endswith('*') else p + '/'
            for p in excluded_paths
        ]

        # Finally, check if the path is excluded from auth
        for excluded_path in normalized_paths:
            # Handle wildcard at the end of the excluded path
            if excluded_path.endswith('*'):
                base_path = excluded_path[:-1]  # Remove the '*'
                if path.startswith(base_path):
                    # Get the remaining path after the base path
                    remaining_path = path[len(base_path):]
                    # Ensure remaining_path doesn't contain a string after '/'
                    temp = remaining_path.split('/')
                    if len(temp) == 2 and not temp[1]:
                        return False
            elif path == excluded_path:
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
