#!/usr/bin/env python3
"""
Module to has a password
"""

from typing import TypeVar, Union
import uuid
from db import DB
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Method to hash a password"""
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pw


def _generate_uuid() -> str:
    """Generate a uuid"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Constructor method"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Method to register a user"""
        if email and password:
            try:
                self._db.find_user_by(email=email)
                raise ValueError("User {} already exists".format(email))
            except NoResultFound:
                hashed_pw = _hash_password(password)
                self._db.add_user(email, hashed_pw)
                return self._db.find_user_by(email=email)
        raise ValueError

    def valid_login(self, email: str, password: str) -> bool:
        """Validate a user credentials for login"""
        try:
            user = self._db.find_user_by(email=email)
            hashed_pw = user.hashed_password
            return bcrypt.checkpw(password.encode('utf-8'), hashed_pw)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Method to create a session id"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, **{'session_id': session_id})
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str)\
            -> TypeVar('User'):
        """Method to get a user object using the session id"""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Method to detroy a session"""
        if not user_id:
            return None
        try:
            self._db.update_user(user_id, **{'session_id': None})
            return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Method to generate a password reset token"""
        try:
            user = self._db.find_user_by(email=email)
            user_id = user.id
            reset_token = _generate_uuid()
            self._db.update_user(user_id, **{'reset_token': reset_token})
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Method to update a user password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_pw = _hash_password(password)
            updates = {'hashed_password': hashed_pw, 'reset_token': None}
            self._db.update_user(user.id, **updates)
        except NoResultFound:
            raise ValueError
