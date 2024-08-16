#!/usr/bin/env python3
"""
Main module for the project
"""

import requests


def register_user(email: str, password: str) -> None:
    """Testing the register functionality"""
    url = "http://127.0.0.1:5000/users"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """Testing the login functionality with wrong password"""
    url = "http://127.0.0.1:5000/sessions"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Testing the login functionality"""
    url = "http://127.0.0.1:5000/sessions"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    session_id = response.cookies.get("session_id")
    return session_id


def profile_unlogged() -> None:
    """Testing the profile functionality when unlogged"""
    url = "http://127.0.0.1:5000/profile"
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Testing the profile functionality when logged"""
    url = "http://127.0.0.1:5000/profile"
    response = requests.get(url, cookies={"session_id": session_id})
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """Testing the logout functionality"""
    url = "http://127.0.0.1:5000/sessions"
    response = requests.delete(url, cookies={"session_id": session_id})
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """Testing the reset password token functionality"""
    url = "http://127.0.0.1:5000/reset_password"
    response = requests.post(url, json={"email": email})
    assert response.status_code == 200
    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Testing the update password functionality"""
    url = "http://127.0.0.1:5000/reset_password"
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(url, json=data)
    assert response.status_code == 200


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
