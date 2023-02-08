#!/usr/bin/env python3
"""
User sessions data model
"""

from models.base import Base


class UserSession(Base):
    """User session class that defines a user session"""

    def __init__(self, *args: list, **kwargs: dict):
        """Constructor method for class instance"""
        super().__init__(*args, **kwargs)
        self.session_id = kwargs.get('session_id')
        self.user_id = kwargs.get('user_id')
