from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import DataRequired, ValidationError
from con_fig import Config


class ContactForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    message = StringField("Message", validators=[DataRequired()])
