#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from user import User
from user import Base


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
        """Create a User object"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> str:
        """find user depond on key and value"""
        user_list = self._session.query(User).all()

        for key, value in kwargs.items():
            if key not in User.__dict__:
                raise InvalidRequestError

            for user in user_list:
                if getattr(user, key) == value:
                    return user
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs: any) -> None:
        """update user attributes which found by user_id
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if key not in User.__dict__:
                raise ValueError
            setattr(user, key, value)
            self._session.commit()
