#!/usr/bin/env python3
"""
Stores a session for user
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession
from models.base import Base


class SessionDBAuth(SessionExpAuth):
    """Class to store a session for a user"""

    def create_session(self, user_id=None):
        """Create and stores a data for each session"""
        if not user_id:
            return None
        session_id = super().create_session(user_id)
        session = UserSession(**{'user_id': user_id, 'session_id': session_id})
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get user id for a a session id"""
        UserSession.load_from_file()
        sessions = UserSession.search({'session_id': session_id})
        if sessions:
            session = sessions[0].to_json()
            created = session.get('created_at')
            created = datetime.strptime(created, "%Y-%m-%dT%H:%M:%S")
            exp_date = created + timedelta(seconds=self.session_duration)
            user_id = session.get('user_id')
            if exp_date - datetime.now() < timedelta(seconds=0):
                return None
            else:
                return user_id
        return None

    def destroy_session(self, request=None):
        """Destroy a user session"""
        super().destroy_session(request)
        UserSession.save_to_file()
