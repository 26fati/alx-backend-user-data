#!/usr/bin/env python3
"""Auth module

This module contains the Auth class
which is responsible for interacting
with the authentication database.
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound
from typing import Union
import uuid


def _hash_password(password: str) -> str:
    """Hashes a password using bcrypt.

    Args:
        password: The password to be hashed.

    Returns:
        The hashed password as a string.
    """
    hashed_pasw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_pasw


def _generate_uuid() -> str:
    """Generates a UUID.

    Returns:
        A UUID as a string.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.

    Methods:
    - register_user
    - valid_login
    - create_session
    - get_user_from_session_id
    - destroy_session
    - get_reset_password_token
    - update_password
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user.

        Args:
            email: The email of the user.
            password: The password of the user.

        Returns:
            The User object representing the registered user.

        Raises:
            ValueError: If the user already exists.
        """
        try:
            user = self._db.find_user_by(email=email)
            print(user.email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_pasw = _hash_password(password)
            return self._db.add_user(email, hashed_pasw)

    def valid_login(self, email: str, password: str) -> bool:
        """Validates a user's login credentials.

        Args:
            email: The email of the user.
            password: The password of the user.

        Returns:
            True if the login credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates a session for a user.

        Args:
            email: The email of the user.

        Returns:
            The session ID as a string.

        Raises:
            None
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Retrieves a user based on a session ID.

        Args:
            session_id: The session ID of the user.

        Returns:
            The User object representing the user if found, None otherwise.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id):
        """Destroys a user's session.

        Args:
            user_id: The ID of the user.

        Returns:
            None

        Raises:
            None
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset password token for a user.

        Args:
            email: The email of the user.

        Returns:
            The reset password token as a string.

        Raises:
            ValueError: If the user does not exist.
        """
        try:
            user = self._db.find_user_by(email=email)
            user.reset_token = _generate_uuid()
            return user.reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str):
        """Updates a user's password.

        Args:
            reset_token: The reset password token.
            password: The new password.

        Returns:
            None

        Raises:
            ValueError: If the reset token is invalid.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        user.hashed_password = _hash_password(password)
        user.reset_token = None
