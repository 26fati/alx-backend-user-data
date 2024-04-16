#!/usr/bin/env python3
""" to manage the API authentication.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Template for all authentication system you will implement.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required for the given path.
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        path = path.rstrip('/')
        for execlude_path in excluded_paths:
            execlude_path = execlude_path.rstrip('/')
            if execlude_path == path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header for the given request.
        """
        if request is None:
            return None
        if 'Authorization' in request.headers:
            return request.headers['Authorization']
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve the current authenticated user.
        """
        return None
