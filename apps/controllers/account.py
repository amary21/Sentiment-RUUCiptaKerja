from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(
        min=6, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)], render_kw={"placeholder": "Password"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class UpdateUsernameForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(
        min=6, max=20)], render_kw={"placeholder": "Enter new username"})
    submit = SubmitField('Update')


class UpdatePasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired()], render_kw={"placeholder": "Enter new password"})
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), Length(
        min=6, max=20), EqualTo('new_password')], render_kw={"placeholder": "Enter confirm new password"})
    submit = SubmitField('Change')

