from . import transaction

from .forms import IssueBookForm, ReturnBookForm

from .. import db

from ..models import Transaction, Member, Book

from flask import render_template, redirect, url_for, flash

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

            return {"Message": "Member or Book not found"}, 404
        
        # Check if transaction exists
        transaction = Transaction.query\
            .filter_by(member_id=member_id, book_id=book_id, return_date=None)\
            .first()

        if transaction:

            flash(
                message=f"{member.first_name} already has this book", 
                category="error"
                )
            
            return redirect(url_for(".issue_book"))
        
        # Check if book is available
        if book.available_copies <= 0:

            flash(
                message="Book is not available for issuance",
                category="error")
            
            return redirect(url_for('transaction.issue_book'))
        
        expected_return_date = datetime.utcnow() + timedelta(days=14)

        book.available_copies -= 1

        new_transaction = Transaction(
            book_id = book.id,
            member_id = member.id,
            issue_date = datetime.utcnow(),
            expected_return_date = expected_return_date,
            status = "Borrowed"
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
        book_status = "Returned"

        # Check if member, book, and transaction exist
        member = Member.query.get(member_id)
        
        book = Book.query.get(book_id)
        
        transaction = Transaction.query\
                    .filter_by(member_id=member_id, book_id=book_id, return_date=None)\
                    .first()

        if not member or not book or not transaction:
            
            return ({"message": "Member, Book, or Transaction not found"}), 404

        # Update book and transaction information
        book.available_copies += 1
        transaction.return_date = return_date
        transaction.status = book_status
        rent_fee = transaction.calculate_rent_fee()
        transaction.rent_fee = rent_fee
        db.session.commit()

        return ({"message": "Book returned successfully", "rent_fee": rent_fee})
    
    return render_template("transactions/return_book.html", form=form)


@transaction.route('/view_transactions')
def view_transactions():

    transactions = Transaction.query.all()

    transactions_data = []

    for transaction in transactions:

        member_name = transaction.member.first_name + " " + transaction.member.last_name

        book_title = transaction.book.title

        transaction_data = {
            'id': transaction.id,
            'member_name': member_name,
            'book_title': book_title,
            'issue_date': transaction.issue_date,
            'return_date': transaction.return_date,
            'rent_fee': transaction.rent_fee,
            'expected_return_date': transaction.expected_return_date,
            'status': transaction.status
        }

        transactions_data.append(transaction_data)

    return render_template("transactions/view_transactions.html", transactions=transactions_data)