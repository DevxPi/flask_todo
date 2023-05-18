from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from os import environ, path
from dotenv import load_dotenv

from forms import TodoForm

BASEDIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASEDIR, ".env"))

app = Flask(__name__)
app.config["SECRET_KEY"] = environ.get("SECRET_KEY")


# /// = relative path, //// = absolute path
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

"""Model class"""


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


"""Route """


@app.route("/", methods=("GET", "POST"))
def index():
    form = TodoForm()

    if request.method == "POST":
        if form.validate_on_submit():
            new_todo = Todo(title=form.todo_title.data, complete=False)
            db.session.add(new_todo)
            db.session.commit()
            flash("New data added...")

            return redirect(url_for("index"))

    todo_list = Todo.query.all()
    return render_template("index.html", todo_list=todo_list, form=form)


"""Update method for update existing data"""


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()

    flash(f"{todo.title} updated...")

    return redirect(url_for("index"))


"""Delete method for delete existing data"""


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()

    if todo:
        db.session.delete(todo)
        db.session.commit()
        flash(f"{todo.title} deleted...")
    else:
        flash("Data not available...")

    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
