from flask import request, jsonify

from flask_login import login_required

from datetime import datetime

from ..models import Book

from . import api

from .. import db

from .auth import basic_auth


@api.route('/books', methods=['POST'])
@basic_auth.login_required
def create_book():

    data = request.json

    new_book = Book(
        title=data['title'],
        author=data['author'],
        publication_date=datetime.strptime(data['publication_date'], '%Y-%m-%d') if 'publication_date' in data else None,
        isbn=data['isbn'] if 'isbn' in data else None,
        available_copies=data['available_copies'] if 'available_copies' in data else 1,
        total_copies=data['total_copies'] if 'total_copies' in data else 1
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify({'message': 'Book created successfully'}), 201


@api.route('/books', methods=['GET'])
@basic_auth.login_required
def get_all_books():

    books = Book.query.all()

    result = []

    for book in books:
        result.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'publication_date': str(book.publication_date) if book.publication_date else None,
            'isbn': book.isbn,
            'available_copies': book.available_copies,
            'total_copies': book.total_copies,
            'created_at': str(book.created_at),
            'updated_at': str(book.updated_at)
        })

    return jsonify(result), 200


@api.route('/books/<int:book_id>', methods=['GET'])
@basic_auth.login_required
def get_book(book_id):

    book = Book.query.get(book_id)

    if book:
        return jsonify({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'publication_date': str(book.publication_date) if book.publication_date else None,
            'isbn': book.isbn,
            'available_copies': book.available_copies,
            'total_copies': book.total_copies,
            'created_at': str(book.created_at),
            'updated_at': str(book.updated_at)
        })
    
    else:

        return jsonify({'message': 'Book not found'}), 404


@api.route('/books/<int:book_id>', methods=['PUT'])
@basic_auth.login_required
def update_book(book_id):

    book = Book.query.get(book_id)

    if book:

        data = request.json
        book.title = data['title'] if 'title' in data else book.title
        book.author = data['author'] if 'author' in data else book.author

        if 'publication_date' in data:
            book.publication_date = datetime.strptime(data['publication_date'], '%Y-%m-%d')

        book.isbn = data['isbn'] if 'isbn' in data else book.isbn
        book.available_copies = data['available_copies'] if 'available_copies' in data else book.available_copies
        book.total_copies = data['total_copies'] if 'total_copies' in data else book.total_copies
        book.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify({'message': 'Book updated successfully'})
    
    else:
        
        return jsonify({'message': 'Book not found'}), 404



@api.route('/books/<int:book_id>', methods=['DELETE'])
@basic_auth.login_required
def delete_book(book_id):

    book = Book.query.get(book_id)

    if book:

        db.session.delete(book)
        db.session.commit()

        return jsonify({'message': 'Book deleted successfully'})
    
    else:

        return jsonify({'message': 'Book not found'}), 404