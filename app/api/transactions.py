from flask import request, jsonify, current_app

from datetime import datetime, timedelta

from ..models import Transaction, Book, Member

from . import api

from .. import db

from .auth import basic_auth


@api.route("/issue_book", methods=["POST"])
@basic_auth.login_required
def issue_book():

    data = request.json
    member_id = data.get('member_id')
    book_id = data.get('book_id')

    # Check if member and book exist
    member = Member.query.get(member_id)
    book = Book.query.get(book_id)

    if not member or not book:
        return jsonify({'message': 'Member or book does not exist'}), 404

    # Check if transaction exists
    if Transaction.query.filter_by(member_id=member_id, book_id=book_id, return_date=None).first():
        return jsonify({'message': 'Transaction already exists'}), 400

    # Check if book is available
    if book.available_copies <= 0:
        return jsonify({'message': 'Book is not available for issuance'}), 400

    expected_return_date = datetime.utcnow() + timedelta(days=14)
    book.available_copies -= 1

    new_transaction = Transaction(
        book_id=book_id,
        member_id=member_id,
        issue_date=datetime.utcnow(),
        expected_return_date=expected_return_date,
        status="Borrowed"
    )

    db.session.add(new_transaction)
    db.session.commit()

    return jsonify({'message': 'Book issued successfully'}), 201


@api.route('/return_book', methods=["POST"])
@basic_auth.login_required
def return_book():

    data = request.json

    member_id = data.get('member_id')
    book_id = data.get('book_id')
    return_date = datetime.utcnow()

    member = Member.query.get(member_id)
    book = Book.query.get(book_id)
    transaction = Transaction.query.filter_by(member_id=member_id, book_id=book_id, return_date=None).first()

    if not member or not book or not transaction:
        return jsonify({'message': 'Member, book, or transaction not found'}), 404

    # Update book and transaction information
    book.available_copies += 1
    transaction.return_date = return_date
    transaction.status = "Returned"
    rent_fee = transaction.calculate_rent_fee()
    transaction.rent_fee = rent_fee
    db.session.commit()

    return jsonify({'message': f'Book returned successfully. Rent fee {rent_fee}'}), 200


@api.route('/view_transactions')
@basic_auth.login_required
def view_transactions():

    search_term = request.args.get('search_term', None)
    page = request.args.get('page', 1, type=int)

    if search_term == 'Borrowed':

        pagination = Transaction.query.filter_by(status='Borrowed').paginate(page=page, per_page=current_app.config["RECORDS_PER_PAGE"], error_out=False)

    elif search_term == 'Returned':

        pagination = Transaction.query.filter_by(status='Returned').paginate(page=page, per_page=current_app.config["RECORDS_PER_PAGE"], error_out=False)

    else:

        pagination = Transaction.query.paginate(page=page, per_page=current_app.config["RECORDS_PER_PAGE"], error_out=False)

    transactions = pagination.items

    transaction_list = [{
        'id': t.id, 
        'book_id': t.book_id, 
        'member_id': t.member_id, 
        'issue_date': t.issue_date, 
        'expected_return_date': t.expected_return_date, 
        'return_date': t.return_date, 
        'status': t.status, 
        'rent_fee': t.rent_fee
        } 
        for t in transactions
        ]

    return jsonify({
        'transactions': transaction_list, 
        'pagination': {
            'total_pages': pagination.pages, 'current_page': page, 'total_records': pagination.total
            }
        })