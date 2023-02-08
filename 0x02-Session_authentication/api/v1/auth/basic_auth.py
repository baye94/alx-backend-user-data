#!/usr/bin/env python3
"""
Basic Authentication module
"""

from typing import TypeVar
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """Basic authentication class"""

    def extract_base64_authorization_header(self, authorization_header: str)\
            -> str:
        """Extract base 64 part of Authorization header"""
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None
        check_basic = authorization_header.split(' ')
        if (check_basic)[0] != 'Basic':
            return None
        return check_basic[1]

    def decode_base64_authorization_header(
                                            self,
                                            base64_authorization_header: str
                                            ) -> str:
        """Decode Base 64 string"""
        if not base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
                                    self,
                                    decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """Extract user credentials"""
        if not decoded_base64_authorization_header:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        credentials = decoded_base64_authorization_header.split(':', 1)
        if len(credentials) == 1:
            return (None, None)
        return (credentials[0], credentials[1])

    def user_object_from_credentials(
                                        self,
                                        user_email: str,
                                        user_pwd: str
                                    ) -> TypeVar('User'):
        """Get user object from the database"""
        from models.user import User
        if not isinstance(user_email, str):
            return None
        if not isinstance(user_pwd, str):
            return None
        user = User()
        current_user = user.search({'email': user_email})
        if not current_user:
            return None
        valid_password = (current_user[0]).is_valid_password(user_pwd)
        if valid_password:
            return current_user[0]
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        auth = BasicAuth()
        b64_auth = None
        b64_decoded = None
        user_cred = None
        usr = None
        auth_header = self.authorization_header(request)
        if auth_header:
            b64_auth = auth.extract_base64_authorization_header(auth_header)
        if b64_auth:
            b64_decoded = auth.decode_base64_authorization_header(b64_auth)
        if b64_decoded:
            user_cred = auth.extract_user_credentials(b64_decoded)
        if user_cred:
            usr = auth.user_object_from_credentials(user_cred[0], user_cred[1])
        print(usr)
        return usr
