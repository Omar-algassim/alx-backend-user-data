#!/usr/bin/env python3
"""basic auth class"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """basic auth class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract base64 authorization header"""
        if not authorization_header or not isinstance(
                        authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
                                        self,
                                        base64_authorization_header: str
                                        ) -> str:
        """decode base64 authorization header"""
        if not base64_authorization_header or\
                not isinstance(base64_authorization_header, str):
            return None
        try:
            return base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """extract user and password from base64 authorization header"""
        if not decoded_base64_authorization_header or not isinstance(
                decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        header = decoded_base64_authorization_header.split(':', 1)
        user = header[0]
        email = header[1]
        return user, email

    def user_object_from_credentials(
                                    self,
                                    user_email: str,
                                    user_pwd: str
                                    ) -> TypeVar('User'):
        """check the user password and email
        if not found user create new user

        Args:
            user_email (str): the email user
            user_pwd (str): the password user
        """
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None
        try:
            exist_user = User.search({'email': user_email})
            if not exist_user or exist_user == []:
                return None
            for users in exist_user:
                if users.is_valid_password(user_pwd):
                    return users
            return None
        except Exception:
            return None
