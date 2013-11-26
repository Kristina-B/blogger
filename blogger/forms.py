
from flask_wtf import Form
from wtforms import TextField, PasswordField, DateTimeField, IntegerField
from wtforms.validators import Required, EqualTo

from wtforms.ext.dateutil import *

class RegistrationForm(Form):
    __tablename__ = 'registrationForm'

    username = TextField('username', [Required()])
    password = PasswordField('password', [Required(), EqualTo('password_2', message='Passwords must match')])
    password_2 = PasswordField('repeat Password')

class LoginForm(Form):
    __tablename__ = 'loginForm'

    username = TextField('username', [Required()])
    password = PasswordField('password', [Required()])


class PostForm(Form):
    __tablename__ = 'postForm'

    title = TextField('title', [Required()])
    content = TextField('content', [Required()])
    author_id = IntegerField('author_id')
    created_at = DateTimeField(auto_now_add='True', display_format='%Y-%m-%d %H:%M:%S')
    updated_at = DateTimeField(auto_now='True', display_format='%Y-%m-%d %H:%M:%S')

class CommentForm(Form):
    __tablename__ = 'commentForm'

    content = TextField('content', [Required()])
    created_at = DateTimeField(auto_now_add='True', display_format='%Y-%m-%d %H:%M:%S')

