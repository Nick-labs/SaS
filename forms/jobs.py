from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    salary = IntegerField('Зарплата', validators=[DataRequired()])
    contacts = StringField('Контакты', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    submit = SubmitField('Применить')
