#!/usr/bin/env python3
"""session class"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """SessionAuth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create session for user depending on user_id"""
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """return the user id base on session id"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """return user based on session cookie"""
        session = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """destroy session"""
        print(request)
        if request is None:
            return False
        session = self.session_cookie(request)
        if not session:
            return False
        user_id = self.user_id_for_session_id(session)
        if not user_id:
            return False
        del self.user_id_by_session_id[session]
        return True
