from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, PasswordField
from wtforms.validators import Email, InputRequired, Length

class RegistrationForm(FlaskForm):
  """Registration form"""

  username = StringField("Username", validators=[InputRequired()])
  password = PasswordField("Password", validators=[InputRequired(), Length(min=8)])
  email = StringField("Email", validators=[InputRequired(), Email()])

class LoginForm(FlaskForm):
  """Login form"""

  username = StringField("Username", validators=[InputRequired()])
  password = PasswordField("Password", validators=[InputRequired()])