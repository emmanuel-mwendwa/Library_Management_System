from flask_wtf import FlaskForm

from wtforms import IntegerField

from wtforms.validators import DataRequired


class IssueBookForm(FlaskForm):

    member_id = IntegerField("Member ID", validators=[
        DataRequired()
    ])
    book_id = IntegerField("Book ID", validators=[
        DataRequired()
    ])