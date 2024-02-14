from flask import render_template, redirect, url_for, flash, request, current_app

from flask_login import login_required

from datetime import datetime

from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm.exc import UnmappedInstanceError

from . import book

from .forms import NewBookForm

from app import db

from app.models import Book


@book.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = NewBookForm()

    if form.validate_on_submit():
        
        Book.create(

            title=form.title.data,
            author=form.author.data,
            publication_date=form.publication_date.data,
            isbn=form.isbn.data,
            available_copies=form.total_copies.data,
            total_copies=form.total_copies.data
        )

        return redirect(url_for('book.view_books'))
    
    form_heading = "Add a New Book"
    submit_button_text = "Add Book"

    return render_template('books/add_book.html', form=form, submit_button_text=submit_button_text)


@book.route("/view_books", methods=["GET"])
def view_books():

    search_term = request.args.get("search_term", "")

    page = int(request.args.get('page', '1'))

    if search_term:
        # Perform search query based on the search term
        pagination = Book.query.filter(
            Book.title.ilike(f"%{search_term}%") | 
            Book.author.ilike(f"%{search_term}%"))\
        .paginate(
            page=page, 
            per_page=current_app.config["RECORDS_PER_PAGE"], 
            error_out=False
            )

        books = pagination.items
        
    else:

        pagination = Book.query.paginate(
            page=page, 
            per_page=current_app.config["RECORDS_PER_PAGE"], 
            error_out=False
            )

        books = pagination.items

    return render_template("books/view_books.html", books=books, pagination=pagination, page=page)


@book.route("/view_book/<int:book_id>")
def view_book(book_id):

    try:

        book = Book.get(book_id)

        if book is None:
            
            raise Exception("Book not found")

        return render_template("books/view_book.html", book=book)
    
    except Exception as e:

        flash(f"Error: {str(e)}", category="error")

        return render_template("error.html")



@book.route('/update_book/<int:book_id>', methods=["GET", "POST", "PUT"])
def update_book(book_id):

    form = NewBookForm()

    book = Book.get(book_id)

    if book is None:

        flash("Book not found", category="error")

    if form.validate_on_submit():
        # Update the book attributes based on the data received in the request

        book.update(
            title = form.title.data,
            author = form.author.data,
            publication_date = form.publication_date.data,
            isbn = form.isbn.data,
            available_copies = form.total_copies.data,
            total_copies = form.total_copies.data,

            # Update the 'updated_at' attribute
            updated_at = datetime.utcnow()
        )


        return redirect(url_for('book.view_book', book_id=book.id))
    
    form.title.data = book.title
    form.author.data = book.author
    form.publication_date.data = book.publication_date
    form.isbn.data = book.isbn
    form.total_copies.data = book.total_copies

    form_heading = "Update Book"
    submit_button_text = "Update Book"

    return render_template("books/add_book.html", form=form, submit_button_text=submit_button_text, form_heading=form_heading)


@book.route('/delete_book/<int:book_id>', methods=["GET", "DELETE"])
def delete_book(book_id):
    
    book = Book.get(book_id)

    if book is None:

        flash("Book not found", category="error")

    try:

        book.delete()

        flash(f"Book deleted successfully", category="success")

    except IntegrityError as e:

        db.session.rollback()

        flash(f"Cannot delete book as transactions with this book exist", category="error")

    except UnmappedInstanceError as e:

        flash(f"Error occurred while deleting book '{book.title}'", category="error")

    return redirect(url_for("book.view_books"))
