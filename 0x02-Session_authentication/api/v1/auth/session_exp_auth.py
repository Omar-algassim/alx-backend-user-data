#!/usr/bin/env python3
"""exepire time class"""
from os import getenv
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime


class SessionExpAuth(SessionAuth):
    """session expire class"""
    
    def __init__(self):
        """initialize"""
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """overload create session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """get the user id for session id"""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id[session_id].get('user_id')
        if 'created_at' not in self.user_id_by_session_id[session_id]:
            return None
        if (datetime.now() - self.user_id_by_session_id[session_id]['created_at']
                ).seconds > self.session_duration:
            return None
        return self.user_id_by_session_id[session_id].get('user_id')
