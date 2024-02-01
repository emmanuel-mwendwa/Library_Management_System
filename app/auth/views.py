from flask import render_template, redirect, url_for, flash, request

from flask_login import login_user, logout_user, current_user, login_required

from . import auth

from .forms import SignupForm, LoginForm

from .. import db

from ..models import User


@auth.route('/signup', methods=["GET", "POST"])
def signup():

    signup_form = SignupForm()

    if signup_form.validate_on_submit():

        new_user = User(
            first_name=signup_form.first_name.data,
            last_name=signup_form.last_name.data,
            email=signup_form.email.data.lower(),
            password=signup_form.password.data
        )

        db.session.add(new_user)

        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template("auth/signup.html", signup_form=signup_form)


@auth.route('/login', methods=["GET", "POST"])
def login():

    login_form = LoginForm()

    if login_form.validate_on_submit():

        user = User.query.filter_by(email=login_form.email.data.lower()).first()

        if user is not None and user.verify_password(login_form.password.data):
            
            login_user(user)

            next = request.args.get('next')

            if next is None or not next.startswith('/'):

                next = url_for('book.view_books')

            return redirect(next)
        
        flash("Invalid username or password", category="error")
        
    return render_template("auth/login.html", login_form=login_form)


@auth.route('/logout')
@login_required
def logout():

    logout_user()

    flash("You have been logged out!!", category="success")

    return redirect(url_for('auth.login'))
    