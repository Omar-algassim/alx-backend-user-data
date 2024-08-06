#!/usr/bin/env python3
"""basic auth class"""
from api.v1.auth.auth import Auth
import base64


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
