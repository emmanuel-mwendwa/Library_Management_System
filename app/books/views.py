from flask import render_template, redirect, url_for, flash

from flask_login import login_required

from datetime import datetime

from . import book

from .forms import NewBookForm

from .. import db

from ..models import Book


@book.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = NewBookForm()

    if form.validate_on_submit():
        new_book = Book(

            title=form.title.data,
            author=form.author.data,
            publication_date=form.publication_date.data,
            isbn=form.isbn.data,
            available_copies=form.available_copies.data,
            total_copies=form.total_copies.data
        )

        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('book.view_books'))
    
    form_heading = "Add a New Book"
    submit_button_text = "Add Book"

    return render_template('books/add_book.html', form=form, submit_button_text=submit_button_text)


@book.route("/view_books")
@login_required
def view_books():

    books = Book.query.all()

    return render_template("books/view_books.html", books=books)


@book.route("/view_book/<int:book_id>")
def view_book(book_id):

    try:

        book = Book.query.filter_by(id=book_id).first()

        if book is None:
            
            raise Exception("Book not found")

        return render_template("books/view_book.html", book=book)
    
    except Exception as e:

        flash(f"Error: {str(e)}", category="error")

        return render_template("error.html")



@book.route('/update_book/<int:book_id>', methods=["GET", "POST", "PUT"])
def update_book(book_id):

    form = NewBookForm()

    book = Book.query.get(book_id)

    if book is None:

        flash("Book not found", category="error")

    if form.validate_on_submit():
        # Update the book attributes based on the data received in the request
        book.title = form.title.data
        book.author = form.author.data
        book.publication_date = form.publication_date.data
        book.isbn = form.isbn.data
        book.available_copies = form.available_copies.data
        book.total_copies = form.total_copies.data

        # Update the 'updated_at' attribute
        book.updated_at = datetime.utcnow()

        db.session.commit()

        return redirect(url_for('book.view_book', book_id=book.id))
    
    form.title.data = book.title
    form.author.data = book.author
    form.publication_date.data = book.publication_date
    form.isbn.data = book.isbn
    form.available_copies.data = book.available_copies
    form.total_copies.data = book.total_copies

    form_heading = "Update Book"
    submit_button_text = "Update Book"

    return render_template("books/add_book.html", form=form, submit_button_text=submit_button_text, form_heading=form_heading)


@book.route('/delete_book/<int:book_id>', methods=["GET", "DELETE"])
def delete_book(book_id):
    
    book = Book.query.get(book_id)

    if book is None:

        flash("Book not found", category="error")

    db.session.delete(book)

    db.session.commit()

    return redirect(url_for("book.view_books"))
