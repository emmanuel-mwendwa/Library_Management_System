from flask_wtf import FlaskForm

from wtforms import IntegerField, DateField

from wtforms.validators import DataRequired


class IssueBookForm(FlaskForm):

    member_id = IntegerField("Member ID", validators=[
        DataRequired()
    ])
    book_id = IntegerField("Book ID", validators=[
        DataRequired()
    ])


class ReturnBookForm(FlaskForm):
    member_id = IntegerField('Member ID', validators=[DataRequired()])
    book_id = IntegerField('Book ID', validators=[DataRequired()])
    return_date = DateField('Return Date', format='%Y-%m-%d', validators=[DataRequired()])