from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
try:
    from wtforms.fields.html5 import EmailField
except:
    from wtforms import EmailField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from paste.models import User


class Register(FlaskForm):
    def validate_username(self, username):
        username_check = User.query.filter_by(username=username.data).first()
        if username_check:
            raise ValidationError('Username already taken, try another one')
    username = StringField(label="UserName", validators=[Length(min=4, max=240), DataRequired()])
    email = EmailField(label="Email", validators=[Length(min=4, max=240), DataRequired()])
    password = PasswordField(label="Password", validators=[Length(min=4, max=240), DataRequired()])
    password_check = PasswordField(label="Confirm Password", validators=[Length(min=4, max=240), EqualTo('password'), DataRequired()])
    submit = SubmitField(label="Submit")

class Login(FlaskForm):
    username = StringField(label="UserName", validators=[Length(min=4, max=240), DataRequired()])
    password = PasswordField(label="Password", validators=[Length(min=4, max=240), DataRequired()])
    submit = SubmitField(label="Submit")
