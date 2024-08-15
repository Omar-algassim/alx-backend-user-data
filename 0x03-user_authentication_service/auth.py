#!/usr/bin/env python3
"""auth module"""
from bcrypt import hashpw, gensalt
from db import DB


def _hash_password(password: str) -> bytes:
    """return hashed password

    Args:
        password (str): passwword string

    Returns:
        bytes: the bytes returned from hashpw
    """
    return hashpw(password.encode('utf-8'), gensalt())



class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()