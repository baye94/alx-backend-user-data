#!/usr/bin/env python3
"""Session authentication expiration module"""

from datetime import datetime, timedelta
import os
from api.v1.auth.session_auth import SessionAuth
import uuid
from models.user import User


class SessionExpAuth(SessionAuth):
    """Session expiry class"""

    def __init__(self):
        """Constructor method"""

        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Overload session creation"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
                                                "user_id": user_id,
                                                "created_at": datetime.now()
                                                }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get user id for a session id"""
        if not session_id:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict:
            user_id = session_dict.get('user_id')
            if not user_id:
                return None
            if self.session_duration <= 0:
                return user_id
            created = session_dict.get('created_at')
            if not created:
                return None
            exp_date = created + timedelta(seconds=self.session_duration)
            if exp_date - datetime.now() < timedelta(seconds=0):
                return None
            else:
                return user_id
        return None
