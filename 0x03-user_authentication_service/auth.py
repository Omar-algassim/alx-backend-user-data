#!/usr/bin/env python3
"""auth module"""
from bcrypt import hashpw, gensalt
from user import User
from sqlalchemy.exc import NoResultFound
from db import DB


def _hash_password(password: str) -> bytes:
    """hash a password
    """
    return hashpw(password.encode(), gensalt())
