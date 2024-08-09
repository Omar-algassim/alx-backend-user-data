#!/usr/bin/env python3
""" UserSession module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""
    
    def create_session(self, user_id=None):
        """create session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        UserSession(user_id=user_id, session_id=session_id).save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """get user id for session id"""
        if session_id is None:
            return None
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return None
        if self.session_duration <= 0:
            return user_session[0].user_id
        if 'created_at' not in user_session[0].__dict__:
            return None
        if (
            datetime.now() - user_session[0].created_at
        ).seconds > self.session_duration:
            return None
        return user_session[0].user_id
490c5c75-75df-4db2-aec3-89c0fd0f7439
    def destroy_session(self, request=None):
        """destroy session"""
        if request is None:
            return False
        session = self.session_cookie(request)
        if session is None:
            return False
        user_session = UserSession.search({'session_id': session})
        if not user_session:
            return False
        user_session[0].remove()
        return True
