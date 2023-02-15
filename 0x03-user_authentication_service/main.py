#!/usr/bin/env python3
"""
End to End Integration tests for user authentication service
"""

import requests


REQUEST_COOKIE = None


def register_user(email: str, password: str) -> None:
    """Test register user function"""
    url = "http://localhost:5000/users"
    obj = {'email': email, 'password': password}
    res = requests.post(url, json=obj)
    exp_res = {'email': email, 'message': 'user created'}
    assert res.json() == exp_res
    assert res.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """Test login with incorrect credentials"""
    url = "http://localhost:5000/sessions"
    obj = {'email': email, 'password': password}
    res = requests.post(url, obj)
    REQUEST_COOKIE = res.cookies.get('session_id')
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test login with correct credentials"""
    url = "http://localhost:5000/sessions"
    obj = {'email': email, 'password': password}
    res = requests.post(url, obj)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """Test an action without a user logged in"""
    url = "http://localhost:5000/profile"
    cookies = {'sesion_id': ''}
    res = requests.get(url, cookies=cookies)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test profile info with user logged in"""
    url = "http://localhost:5000/profile"
    cookies = {'sesion_id': session_id}
    res = requests.get(url, cookies=cookies)
    assert res.status_code == 200
    assert res.json() == {"email": "guillaume@holberton.io"}


def log_out(session_id: str) -> None:
    """Test user logout"""
    url = "http://localhost:5000/logout"
    cookies = {'session_id': session_id}
    res = requests.delete(url, cookies=cookies)
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Test for password reset token"""
    url = "http://localhost:5000/reset_password"
    obj = {'email': email}
    res = requests.post(url, json=obj)
    assert res.status_code == 200
    return (res.json()).get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test update user password"""
    url = "http://localhost:5000/reset_password"
    obj = {
            'email': email,
            'reset_token': reset_token,
            'new_password': new_password
        }
    res = requests.put(url, obj)
    assert res.status_code == 200
    assert res.json == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
