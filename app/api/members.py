from flask import request, jsonify, make_response

from datetime import datetime

from . import api

from .auth import basic_auth

from .. import db

from ..models import Member


@api.route('/members', methods=["POST"])
@basic_auth.login_required
def create_member():

    data = request.get_json()

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')

    if not first_name or not last_name or not email:

        return jsonify({'message': 'Missing data'}), 400
    
    new_member = Member(
        first_name=first_name,
        last_name=last_name,
        email=email
    )
    
    db.session.add(new_member)
    db.session.commit()

    return jsonify({'message': 'Member created successfully'}), 201


@api.route('/members', methods=["GET"])
@basic_auth.login_required
def get_members():

    members = Member.query.all()

    return jsonify([
        {
            'id': member.id, 
            'first_name': member.first_name, 
            'last_name': member.last_name, 
            'email': member.email
            } 
            for member in members
    ]), 200


@api.route('/members/<int:id>', methods=["GET"])
@basic_auth.login_required
def get_member(id):

    member = Member.query.get_or_404(id)

    if member:
        return jsonify({
            'id': member.id,
            'first_name': member.first_name,
            'last_name': member.last_name,
            'email': member.email
        }), 200
    
    else:

        return jsonify({'message': 'Member not found'}), 404


@api.route('/members/<int:id>', methods=["PUT"])
@basic_auth.login_required
def update_member(id):
    member = Member.query.get(id)
    data = request.get_json()
    
    if member:

        member.first_name = data.get('first_name', member.first_name)
        member.last_name = data.get('last_name', member.last_name)
        member.email = data.get('email', member.email)
        
        db.session.commit()

        return jsonify({'message': 'Member updated successfully'}), 200
    
    else:

        return jsonify({'message': 'Member not found'}), 404


@api.route('/members/<int:id>', methods=['DELETE'])
@basic_auth.login_required
def delete_member(id):
    member = Member.query.get(id)
    
    if member:
        db.session.delete(member)
        db.session.commit()
    
        return jsonify({'message': 'Member deleted successfully'}), 200
    
    else:

        return jsonify({'message': 'Member not found'}), 404