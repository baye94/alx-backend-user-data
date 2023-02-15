#!/usr/bin/env python3
"""DB module
"""

from typing import Dict, TypeVar
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Method to add a user to the database"""
        if email and hashed_password:
            user = User()
            user.email = email
            user.hashed_password = hashed_password
            self._session.add(user)
            self._session.commit()
            return self._session.query(User).filter_by(email=email).first()

    def find_user_by(self, **kwargs) -> User:
        """Method to find a user using keyword filters"""
        if not kwargs:
            raise InvalidRequestError
        attr = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']
        for k, v in kwargs.items():
            if k not in attr:
                raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Method to update a user in a database"""
        try:
            user = self.find_user_by(id=user_id)
            for k, v in kwargs.items():
                if hasattr(user, k):
                    setattr(user, k, v)
                else:
                    raise ValueError
            self._session.add(user)
            self._session.commit()
            return None
        except NoResultFound:
            raise ValueError
