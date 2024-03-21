from . import api

from .. import db

from ..models import User

from flask import request, jsonify, g

from flask_login import login_user, logout_user


@api.route('/register', methods=['POST'])
def register():

    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()

    if user:

        return jsonify({'message': 'Email already registered.'}), 400
    
    new_user = User(
        first_name = data['first_name'],
        last_name = data['last_name'],
        email = data['email'],
        password = data['password']
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully.'}), 201


@api.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()

    if user and user.verify_password(data['password']):

        login_user(user)

        return jsonify({'message': 'Logged in successfully.'}), 200
    return jsonify({'message': 'Invalid username or password.'}), 401


@api.route('/logout')
def logout():
    logout_user()
    return jsonify({'message': 'You have been logged out.'}), 200

