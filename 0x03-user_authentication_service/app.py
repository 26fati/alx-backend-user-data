#!/usr/bin/env python3
'''
This module contains a Flask application
that provides user authentication services.
'''

from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth
from sqlalchemy.exc import NoResultFound


app = Flask(__name__)
auth = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home() -> str:
    """
    Home route of the application.

    Returns:
        str: A JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """
    Register a new user.

    Returns:
        JSON: A JSON response with the user's email and a success message.
    """
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)
    try:
        user = auth.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """
    Log in a user.

    Returns:
        JSON: A JSON response with the user's email and a success message.
    """
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(401)
    if not auth.valid_login(email, password):
        abort(401)
    else:
        session_id = auth.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Log out a user.

    Returns:
        redirect: Redirects the user to the home route.
    """
    session_id = request.cookies.get('session_id')
    user = auth.get_user_from_session_id(session_id)
    if user:
        auth.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    Get the user's profile.

    Returns:
        JSON: A JSON response with the user's email.
    """
    session_id = request.cookies.get('session_id')
    user = auth.get_user_from_session_id(session_id)
    if user is not None:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """
    Get a reset password token for a user.

    Returns:
        JSON: A JSON response with
        the user's email and the reset password token.
    """
    try:
        email = request.form['email']
    except KeyError:
        abort(403)
    token = auth.get_reset_password_token(email)
    return jsonify({"email": email, "reset_token": token}), 200


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """
    Update the user's password.

    Returns:
        JSON: A JSON response with the user's email and a success message.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        auth.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
