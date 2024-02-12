from flask_wtf import FlaskForm

from wtforms import StringField, DateField, IntegerField, SubmitField

from wtforms.validators import DataRequired, NumberRange, Optional


class NewBookForm(FlaskForm):

    title = StringField('Title', 
                        validators=[
                            DataRequired()
                        ])

    author = StringField('Author', 
                         validators=[
                            DataRequired()
                        ])
    
    publication_date = DateField('Publication Date ', 
                                 format='%Y-%m-%d', 
                                 validators=[
                                    Optional()
                                ])
    
    isbn = StringField('ISBN', 
                       validators=[
                           Optional()
                        ])
    
    total_copies = IntegerField('Total Copies', 
                                validators=[
                                    DataRequired(), 
                                    NumberRange(min=0)
                                ])

