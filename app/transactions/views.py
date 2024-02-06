from . import transaction

from .forms import IssueBookForm, ReturnBookForm

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
        
        # Check if transaction exists
        transaction = Transaction.query.filter_by(member_id=member_id, book_id=book_id, return_date=None).first()

        if transaction:

            return {"Message": "Member already has book"}
        
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


@transaction.route('/return_book', methods=["GET", "POST"])
def return_book():

    form = ReturnBookForm()

    if form.validate_on_submit():

        member_id = form.member_id.data
        book_id = form.book_id.data
        return_date = form.return_date.data

        # Check if member, book, and transaction exist
        member = Member.query.get(member_id)
        book = Book.query.get(book_id)
        transaction = Transaction.query.filter_by(member_id=member_id, book_id=book_id, return_date=None).first()

        if not member or not book or not transaction:
            return ({"message": "Member, Book, or Transaction not found"}), 404

        # Update book and transaction information
        book.available_copies += 1
        transaction.return_date = return_date
        rent_fee = transaction.calculate_rent_fee()
        transaction.rent_fee = rent_fee
        db.session.commit()

        return ({"message": "Book returned successfully", "rent_fee": rent_fee})
    
    return render_template("transactions/return_book.html", form=form)