
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, EqualTo


class RegistrationForm(Form):
    __tablename__ = 'registrationForm'

    username = TextField('Username', [Required()])
    password = PasswordField('Password', [
        Required(),
        EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('Confirm password')


class LoginForm(Form):
    __tablename__ = 'loginForm'

    username = TextField('Username', [Required()])
    password = PasswordField('Password', [Required()])


class PostForm(Form):
    __tablename__ = 'postForm'

    title = TextField('title', [Required()])
    content = TextField('content', [Required()])


class CommentForm(Form):
    __tablename__ = 'commentForm'

    content = TextField('content', [Required()])
