from . import transaction

from .forms import IssueBookForm

from .. import db

from ..models import Transaction, Member, Book

from flask import render_template, redirect, url_for

from datetime import datetime, timedelta


@transaction.route("/issue_book", methods=["GET", "POST"])
def issue_book():

    form = IssueBookForm()

    if form.validate_on_submit():

        member_id = form.member_id.data
        book_id = form.book_id.data

        # Check if member and book exist

        member = Member.query.get(member_id)
        book = Book.query.get(book_id)

        if not member or not book:

            return {"Message": "Member or Book not found"}
        
        # Check if book is available
        if book.available_copies <= 0:

            return {"Message": "Book is not available for issuance"}
        
        expected_return_date = datetime.utcnow() + timedelta(days=14)

        book.available_copies -= 1

        new_transaction = Transaction(
            book_id = book.id,
            member_id = member.id,
            issue_date = datetime.utcnow(),
            expected_return_date = expected_return_date
        )

        db.session.add(new_transaction)

        db.session.commit()

        return redirect(url_for("book.view_books"))

    return render_template("transactions/issue_book.html", form=form)