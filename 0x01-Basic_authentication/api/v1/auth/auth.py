#!/usr/bin/env python3
"""authintication class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """authintication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """return Fasle if path in execluded_paths true otherwise"""
        if not path:
            return True
        if type(path) == str and not path[-1] == '/':
            path += '/'
        for i in excluded_paths:
            if i[-1] == '*':
                if path.startswith(i[:-1]):
                    return False
            if path == i:
                return False

        if excluded_paths == [] or excluded_paths is None:
            return True
        return True

    def authorization_header(self, request=None) -> str:
        """return None - request will be flask request object"""
        if not request or not request.headers.get('Authorization'):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """return None - request will be flask request object"""
        return None
