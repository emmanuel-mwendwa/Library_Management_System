from app import create_app, db

from app.models import User

from flask_migrate import Migrate


app = create_app('default')
migrate = Migrate(app, db)

@app.route("/")
def home():
    return {"message": "Welcome to my library management system"}

@app.shell_context_processor
def make_shell_processor():
    return dict(db=db)

if __name__ == "__main__":
    app.run(debug=True)