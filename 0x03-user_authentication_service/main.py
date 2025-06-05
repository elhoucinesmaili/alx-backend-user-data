#!/usr/bin/env python3
"""
End-to-end integration test for the authentication service
"""
import requests


def register_user(email: str, password: str) -> None:
    """
    Test user registration
    
    Args:
        email: User email
        password: User password
    """
    url = "http://0.0.0.0:5000/users"
    body = {"email": email, "password": password}
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}
    res = requests.post(url, data=body)
    assert res.status_code == 400
    assert res.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Test login with wrong password
    
    Args:
        email: User email
        password: Wrong password
    """
    url = "http://0.0.0.0:5000/sessions"
    body = {"email": email, "password": password}
    res = requests.post(url, data=body)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Test successful login
    
    Args:
        email: User email
        password: Correct password
        
    Returns:
        Session ID from cookie
    """
    url = "http://0.0.0.0:5000/sessions"
    body = {"email": email, "password": password}
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    return res.cookies.get("session_id")


def profile_unlogged() -> None:
    """
    Test profile access without login
    """
    url = "http://0.0.0.0:5000/profile"
    res = requests.get(url)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Test profile access with valid session
    
    Args:
        session_id: Valid session ID
    """
    url = "http://0.0.0.0:5000/profile"
    cookies = {"session_id": session_id}
    res = requests.get(url, cookies=cookies)
    assert res.status_code == 200
    assert "email" in res.json()


def log_out(session_id: str) -> None:
    """
    Test user logout
    
    Args:
        session_id: Session ID to destroy
    """
    url = "http://0.0.0.0:5000/sessions"
    cookies = {"session_id": session_id}
    res = requests.delete(url, cookies=cookies)
    assert res.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Test password reset token generation
    
    Args:
        email: User email
        
    Returns:
        Reset token
    """
    url = "http://0.0.0.0:5000/reset_password"
    body = {"email": email}
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert "email" in res.json()
    assert "reset_token" in res.json()
    return res.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Test password update
    
    Args:
        email: User email
        reset_token: Valid reset token
        new_password: New password
    """
    url = "http://0.0.0.0:5000/reset_password"
    body = {"email": email, "reset_token": reset_token, "new_password": new_password}
    res = requests.put(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}


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
