from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo

class DataTrainForm(FlaskForm):
    tweet = TextAreaField('Tweet', validators=[DataRequired()], render_kw={"placeholder": "Input new tweet"})
    sentiment = SelectField('Sentimen', choices=[('0', 'Negatif'), ('1', 'Positif')], validators=[DataRequired()])
    submit = SubmitField('Save')
