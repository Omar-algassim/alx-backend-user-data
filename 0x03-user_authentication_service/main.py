#!/usr/bin/env python3
"""
Main file
"""
from flask import abort
import requests
from auth import Auth


def register_user(email: str, password: str) -> None:
    """register user post request"""
    resp = requests.post(
        'http://localhost:5000/users',
        data={'email': email, 'password': password}
        )
    assert resp.json, {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """log in with wrong password"""
    resp = requests.post(
        'http://localhost:5000/sessions',
        data={'email': email, 'password': password}
        )
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """succeful log in"""
    resp = requests.post(
        'http://localhost:5000/sessions',
        data={'email': email, 'password': password}
        )
    assert resp.status_code == 200
    return resp.cookies['session_id']


def profile_unlogged() -> None:
    """test profile unlogged"""
    resp = requests.get('http://localhost:5000/profile')
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """login and test profile"""
    resp = requests.get(
        'http://localhost:5000/profile',
        cookies={'session_id': session_id}
        )
    assert resp.json, {"email": EMAIL}


def log_out(session_id: str) -> None:
    """delete session"""
    resp = requests.delete(
        'http://localhost:5000/sessions',
        cookies={'session_id': session_id}
        )
    assert resp.json, {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """make token to reset password"""
    resp = requests.post(
        'http://localhost:5000/reset_password',
        data={'email': email}
        )
    assert resp.status_code == 200
    return resp.json()['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """update password"""
    resp = requests.put(
        'http://localhost:5000/reset_password',
        data={
            'email': email,
            'reset_token': reset_token,
            'new_password': new_password
            }
        )
    assert resp.json, {"email": email, "message": "Password updated"}


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
