#!/usr/bin/env python3
"""
Basic flask application
"""

from flask import Flask, jsonify, request, make_response, abort, redirect
from flask import url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'], strict_slashes=False)
def home():
    """Basic payload response"""
    return jsonify({"message": "Bienvenue"}), 200


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """Endpoint to register a user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email,
                       "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    """Endpoint to login a user"""
    email = request.form.get('email')
    password = request.form.get('password')
    valid = AUTH.valid_login(email, password)
    if valid:
        session_id = AUTH.create_session(email)
        response = make_response({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response, 200
    else:
        return abort(401)


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """Endpoint to logout a user"""
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if not user:
            return abort(403)
        AUTH.destroy_session(user.id)
        return redirect('/')
    return abort(403)


@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile():
    """Function to return a user profile"""
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200
    return abort(403)


@app.route("/reset_password", methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """Endpoint to get a password reset token"""
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except Exception:
        return abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """Endpoint to update a user password"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    session_id = request.cookies.get('session_id')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception:
        return abort(403)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
