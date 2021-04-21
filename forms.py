from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired


class TodoForm(FlaskForm):
    # id = IntegerField('id', validators=[DataRequired()])
    title = StringField('title', validators=[DataRequired()])
    description = TextAreaField('description')
    done = BooleanField('done')
