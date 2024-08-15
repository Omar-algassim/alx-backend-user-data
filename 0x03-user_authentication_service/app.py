#!/usr/bin/env python3
"""basic flask app"""
from flask import Flask, jsonify, request, abort
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
