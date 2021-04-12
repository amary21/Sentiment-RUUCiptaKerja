from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField, TextAreaField, SelectField, HiddenField, StringField
from wtforms.validators import DataRequired


class DataTrainForm(FlaskForm):
    tweet = TextAreaField('Tweet', validators=[DataRequired()], render_kw={
        "placeholder": "Input new tweet"})
    sentiment = SelectField('Sentimen', choices=[(
        '0', 'Negatif'), ('1', 'Positif')], validators=[DataRequired()])
    submit = SubmitField('Save')


class UpdateDataTrainForm(FlaskForm):
    update_id = HiddenField('Id')
    update_tweet = TextAreaField('Tweet', validators=[DataRequired()], render_kw={
        "placeholder": "Input new tweet"})
    update_sentiment = SelectField('Sentimen', choices=[(
        '0', 'Negatif'), ('1', 'Positif')], validators=[DataRequired()])
    update_submit = SubmitField('Save')

class DataCSVForm(FlaskForm):
    csv_file = FileField('File CSV', validators=[FileRequired(), FileAllowed(['csv', 'CSVs only!'])])
    csv_submit = SubmitField('Save')


class ViewDataTrainForm(FlaskForm):
    view_id = HiddenField('Id')
    view_account = StringField('Twitter Account')
    view_tweet = TextAreaField('Tweet')
    view_clean = TextAreaField('Clean Tweet')
    view_sentiment = StringField('Sentimen')

