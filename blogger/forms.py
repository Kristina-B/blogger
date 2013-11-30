
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, EqualTo


class RegistrationForm(Form):
    __tablename__ = 'registrationForm'

    username = TextField('username', [Required()])
    password = PasswordField('password', [
        Required(),
        EqualTo('password_2', message='Passwords must match')])
    password_2 = PasswordField('repeat Password')


class LoginForm(Form):
    __tablename__ = 'loginForm'

    username = TextField('username', [Required()])
    password = PasswordField('password', [Required()])


class PostForm(Form):
    __tablename__ = 'postForm'

    title = TextField('title', [Required()])
    content = TextField('content', [Required()])


class CommentForm(Form):
    __tablename__ = 'commentForm'

    content = TextField('content', [Required()])
