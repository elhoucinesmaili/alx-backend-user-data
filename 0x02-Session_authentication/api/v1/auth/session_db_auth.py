#!/usr/bin/env python3
""" Session Database Authentication module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ Session Database Authentication class
    """
    def create_session(self, user_id=None):
        """ Creates and stores new instance of UserSession
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns User ID by requesting UserSession
        """
        if session_id is None:
            return None
        UserSession.load_from_file()
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return None
        if self.session_duration <= 0:
            return user_sessions[0].user_id
        created_at = user_sessions[0].created_at
        if (created_at + 
            timedelta(seconds=self.session_duration)) < datetime.now():
            return None
        return user_sessions[0].user_id

    def destroy_session(self, request=None):
        """ Destroys the UserSession
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return False
        user_sessions[0].remove()
        return True
