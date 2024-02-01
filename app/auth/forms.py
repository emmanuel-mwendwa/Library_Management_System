from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField

from wtforms.validators import DataRequired, Length, Email, EqualTo

from wtforms import ValidationError

from ..models import User


class SignupForm(FlaskForm):

    email = StringField('Email', 
                        validators=[
                            DataRequired(), 
                            Length(1, 56), 
                            Email(message="This field requires a valid email address.")
                            ])
    
    first_name = StringField('First name', 
                             validators=[
                                 Length(0, 64)
                            ])
    
    last_name = StringField('Last name', 
                            validators=[
                                Length(0, 64)
                            ])

    password = PasswordField('Password', 
                             validators=[
                                DataRequired(), 
                                EqualTo('password2', message='Passwords must match.')
                            ])
    
    password2 = PasswordField('Confirm password', 
                              validators=[
                                  DataRequired()
                            ])
    
    submit = SubmitField('Sign Up')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
        

class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[
                            DataRequired(), 
                            Length(1, 78), Email()
                        ])
    
    password = PasswordField('Password', 
                             validators=[
                                DataRequired()
                            ])
    
    submit = SubmitField('Log In')