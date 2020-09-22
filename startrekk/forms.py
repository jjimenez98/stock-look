from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanForms
from wt.forms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2, max=10)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_pw = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('SignUp')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    remember = BooleanField('Remember Me')
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_pw = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('SignUp')
