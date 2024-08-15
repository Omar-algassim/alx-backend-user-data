#!/usr/bin/env python3
"""basic flask app"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def message() -> str:
    """GET / route
    Return:
      - JSON payload: {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """create new user if not exist"""
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """create new session"""
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            resp = jsonify({"email": email, "message": "logged in"})
            resp.set_cookie('session_id', session_id)
            return resp
        else:
            abort(401)
    except NoResultFound:
        return jsonify({"message": "no user found"}), 404


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """delete session"""

    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """get profile"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/rest_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """get reset password token"""
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
