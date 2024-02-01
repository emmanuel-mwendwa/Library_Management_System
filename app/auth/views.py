from flask import render_template, redirect, url_for, request, jsonify

from flask_pydantic import validate

from . import auth

from .. import db, schemas

from ..models import User


@auth.route('/signup', methods=["POST"])
@validate(body=schemas.UserIn)
def signup():

    user = request.get_json()

    new_user = User(**user)

    db.session.add(new_user)

    db.session.commit()

    db.session.refresh(new_user)

    user_out = schemas.UserOut.from_orm(new_user)

    return jsonify(user_out.dict())