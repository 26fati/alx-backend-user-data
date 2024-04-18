#!/usr/bin/env python3
"""
Definition of class SessionExpAuth
"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session authentication class with expiration.
    """
    def __init__(self) -> None:
        ''' initialization'''
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Creates a session id for the user.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieves the user id of the user associated with
        a given session id.
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            return session_dictionary.get('user_id')
        if 'created_at' not in session_dictionary.keys():
            return None
        current_date = datetime.now()
        session_duration = timedelta(seconds=self.session_duration)
        exp_time = session_duration + session_dictionary['created_at']
        if exp_time < current_date:
            return None
        else:
            return session_dictionary['user_id']
