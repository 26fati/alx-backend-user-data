#!/usr/bin/env python3
""" to manage the Basic API authentication.
"""
from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """Class for basic authentication.
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        '''
        a method that returns the Base64
        part of the Authorization header for a Basic Authentication.
        '''
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        '''
        a method hat returns
        the decoded value of a Base64 string base64_authorization_header.
        '''
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        '''
        a method  that returns the user email and password
        from the Base64 decoded value.
        '''
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        lst = decoded_base64_authorization_header.split(':')
        return (lst[0], lst[1])

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        '''
        a method that returns
        the User instance based on his email and password.
        '''
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            users = User.search({"email": user_email})
            if users is None:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        a method that overloads Auth
        and retrieves the User instance for a request
        '''
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            code = self.extract_base64_authorization_header(auth_header)
            if code is not None:
                decoded_token = self.decode_base64_authorization_header(code)
                if decoded_token is not None:
                    credentials = self.extract_user_credentials(decoded_token)
                    if credentials is not None:
                        user = self.user_object_from_credentials(
                            credentials[0], credentials[1])
                        return user
        return
