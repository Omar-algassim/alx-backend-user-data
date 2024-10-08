#!/usr/bin/env python3
"""session auth class"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def auth_session_login():
    """handles all routes for the Session authentication"""
    email = request.form.get("email")
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if not password:
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            user = user.to_json()
            ret = jsonify(user)
            ret.set_cookie(getenv("SESSION_NAME"), session_id)
            return ret
    return jsonify({"error": "wrong password"}), 401


@app_views.route("/auth_session/logout",
                 methods=["DELETE"], strict_slashes=False)
def logout():
    """logout and delete session"""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
