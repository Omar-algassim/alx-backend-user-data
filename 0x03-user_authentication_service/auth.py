#!/usr/bin/env python3
"""auth module"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """return hashed password

    Args:
        password (str): passwword string

    Returns:
        bytes: the bytes returned from hashpw
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

def register_user(self, email: str, password: str) -> None:
    """register a user

    Args:
        email (str): email string
        password (str): password string
    """
    try:
        user = self._db.find_user_by(email=email)
        if user:
            raise ValueError(f"User {email} already exists")
    except NoResultFound:
        self._db.add_user(email, _hash_password(password))
