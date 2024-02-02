from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField

from wtforms.validators import DataRequired, Length, Email

class AddMemberForm(FlaskForm):

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
    
    submit = SubmitField('Add Member')