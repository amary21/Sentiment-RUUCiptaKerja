from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class DataTrainForm(FlaskForm):
    tweet = TextAreaField('Tweet', validators=[DataRequired()], render_kw={
        "placeholder": "Input new tweet"})
    sentiment = SelectField('Sentimen', choices=[(
        '0', 'Negatif'), ('1', 'Positif')], validators=[DataRequired()])
    submit = SubmitField('Save')
