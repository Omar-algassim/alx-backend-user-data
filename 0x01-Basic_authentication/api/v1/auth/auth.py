#!/usr/bin/env python3
"""authintication class"""
from flask import request
from typing import List, TypeVar


class auth:
    """authintication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """return Fasle"""
        return False

    def authorization_header(self, request=None) -> str:
        """return None - request will be flask request object"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """return None - request will be flask request object"""
        return None
