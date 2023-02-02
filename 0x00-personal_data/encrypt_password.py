#!/usr/bin/env python3
""" Hash a password with bcrypt package"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Function to has a password"""
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pw


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Function to validate a hashed password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
