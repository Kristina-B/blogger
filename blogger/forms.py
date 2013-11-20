
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, EqualTo


class RegistrationForm(Form):
    __tablename__ = 'registrationForm'

    name = TextField('Username', [Required()])
    password = PasswordField('Password', [Required()])
    confirm = PasswordField('Repeat Password', [Required(), EqualTo('password', message='Passwords must match')])
