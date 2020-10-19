from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired

class TestForm(FlaskForm):
    job_title_1 = StringField('Job Title One', validators=[DataRequired()])
    job_title_2 = StringField('Job Title Two')
    job_title_3 = StringField('Job Title Three')

    start_date_1 = DateField('Start Date One', validators=[DataRequired()])
    start_date_2 = DateField('Start Date Two')
    start_date_3 = DateField('Start Date Three')

    end_date_1 = DateField('End Date One', validators=[DataRequired()])
    end_date_2 = DateField('End Date Two')
    end_date_3 = DateField('End Date Three')

    myChoices = ["English","French"]
    skills_choices = ["10","15","20","30"]
    language = SelectField("SKILLS language",choices = myChoices, validators = [DataRequired()])
    number_of_skills = SelectField("SKILLS number",choices = skills_choices, validators = [DataRequired()])

    submit = SubmitField('Finish')