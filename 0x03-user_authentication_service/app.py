#!/usr/bin/env python3
"""
Flask app for user authentication service
"""
from flask import Flask, jsonify, request, abort, make_response, redirect

from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """
    GET /
    Return welcome message
    
    Returns:
        JSON response with welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """
    POST /users
    Register a new user
    
    Returns:
        JSON response with user creation status
    """
    email = request.form.get("email")
    password = request.form.get("password")
    
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """
    POST /sessions
    Log in a user and create a session
    
    Returns:
        JSON response with login status and sets session cookie
    """
    email = request.form.get("email")
    password = request.form.get("password")
    
    if not AUTH.valid_login(email, password):
        abort(401)
    
    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """
    DELETE /sessions
    Log out a user and destroy session
    
    Returns:
        Redirect to home page or 403 if user not found
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    
    if user is None:
        abort(403)
    
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """
    GET /profile
    Get user profile information
    
    Returns:
        JSON response with user email or 403 if not authenticated
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    
    if user is None:
        abort(403)
    
    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    POST /reset_password
    Generate reset password token
    
    Returns:
        JSON response with reset token or 403 if user not found
    """
    email = request.form.get("email")
    
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """
    PUT /reset_password
    Update user password using reset token
    
    Returns:
        JSON response with update status or 403 if token invalid
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
