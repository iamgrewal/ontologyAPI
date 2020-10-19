from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField, FormField, FieldList
from wtforms.validators import DataRequired

class FeedbackEntryForm(FlaskForm):
    name = BooleanField()


class FeedbackForm(FlaskForm):
    skills = FieldList(FormField(FeedbackEntryForm, ), min_entries=1)
    #submit = SubmitField('Finish')