from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class TodoForm(FlaskForm):
    todo_title =StringField('title', validators=[DataRequired()], render_kw={
        "placeholder": 'Enter todo-title...'
    })