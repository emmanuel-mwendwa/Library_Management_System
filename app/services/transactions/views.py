from . import transaction

from .forms import IssueBookForm, ReturnBookForm

from app import db

from app.models import Book, Member, Transaction

from flask import render_template, redirect, url_for, flash, request, current_app, abort

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

        if not member:

            flash("Member does not exist", category="error")

            return redirect(url_for(".issue_book"))
        
        if not book:

            flash("Book does not exist", category="error")

            return redirect(url_for(".issue_book"))
        
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

        Transaction.create(
            book_id = book.id,
            member_id = member.id,
            issue_date = datetime.utcnow(),
            expected_return_date = expected_return_date,
            status = "Borrowed"
        )

        return redirect(url_for("transaction.view_transactions"))

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

        if not member:
            
            flash(message="Member not found", category="error")

            return redirect(url_for('transaction.return_book'))
        
        elif not book:
            
            flash(message="Book not found", category="error")

            return redirect(url_for('transaction.return_book'))
        
        elif not transaction:

            flash(message="Transaction not found", category="error")

            return redirect(url_for('transaction.return_book'))
            

        # Update book and transaction information
        book.available_copies += 1
        transaction.return_date = return_date
        transaction.status = book_status
        rent_fee = transaction.calculate_rent_fee()
        transaction.rent_fee = rent_fee
        db.session.commit()

        flash(f"Book returned successfully. Rent fee {rent_fee}", category="success")

        return redirect(url_for("transaction.view_transactions"))
    
    return render_template("transactions/return_book.html", form=form)


@transaction.route('/view_transactions')
def view_transactions():

    search_term = request.args.get('search_term', None) 
    page = request.args.get('page', 1, type=int)
    
    if search_term == 'Borrowed':

        pagination = Transaction.query.filter_by(status='Borrowed').paginate(page=page, per_page=current_app.config["RECORDS_PER_PAGE"], error_out=False)

        transactions = pagination.items
    
    elif search_term == 'Returned':
        
        pagination = Transaction.query.filter_by(status='Returned').paginate(page=page, per_page=current_app.config["RECORDS_PER_PAGE"], error_out=False)

        transactions = pagination.items
    
    else:

        pagination = Transaction.query.paginate(page=page, per_page=current_app.config["RECORDS_PER_PAGE"], error_out=False)

        transactions = pagination.items


    return render_template("transactions/view_transactions.html", transactions=transactions, pagination=pagination, page=page, search_term=search_term)