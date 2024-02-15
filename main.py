from app import create_app, db, fake

from flask_migrate import Migrate

from flask import render_template, redirect, url_for

from app.models import Book, Member, Transaction


app = create_app('default')
migrate = Migrate(app, db)

@app.route("/")
def index():
    return redirect(url_for('home'))

@app.route("/home")
def home():

    total_books = Book.query.count()
    total_members = Member.query.count()
    total_borrowed = Transaction.query.filter_by(status="Borrowed").count()
    total_returned = Transaction.query.filter_by(status="Returned").count()

    recent_books = Book.query.order_by(Book.created_at.desc()).limit(4).all()
    
    recent_members = Member.query.order_by(Member.created_at.desc()).limit(4).all()
    
    recent_issues = Transaction.query.join(Book, Transaction.book_id == Book.id) \
                                  .join(Member, Transaction.member_id == Member.id) \
                                  .filter(Transaction.status == "Borrowed") \
                                  .order_by(Transaction.issue_date.desc()) \
                                  .limit(4) \
                                  .all()
    
    recent_returns = Transaction.query.filter_by(status = "Returned")\
                        .order_by(Transaction.issue_date.desc())\
                        .limit(4)\
                        .all()

    return render_template("index.html", 
                           total_books=total_books, total_members=total_members,
                           total_borrowed=total_borrowed, total_returned=total_returned,
                           recent_books=recent_books, recent_members=recent_members, recent_issues=recent_issues, recent_returns=recent_returns
                           )

@app.errorhandler(404)
def page_not_found(error):

    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(error):

    return render_template("500.html"), 500

@app.shell_context_processor
def make_shell_processor():
    return dict(db=db, fake=fake)

if __name__ == "__main__":
    app.run(debug=True)