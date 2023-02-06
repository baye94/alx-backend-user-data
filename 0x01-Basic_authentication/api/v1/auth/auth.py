#!/usr/bin/env python3
"""
Authentication module
"""

from flask import request
import re
from typing import List, TypeVar


class Auth():
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if path requires authentication"""
        if not path or not excluded_paths:
            return True
        for ex_path in excluded_paths:
            if ex_path[-1] == '*':
                pat = ex_path.split('*')
                pat = pat[0] + '.*'
                match = re.search(pat, path)
                if match:
                    return False
        if path[-1] != '/':
            path = path + '/'
        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        if not request:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        return None
