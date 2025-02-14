from ast import Pass
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectMultipleField, DateTimeLocalField
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
)


from .models import User




class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    CLIFTON_STRENGTHS = [
        ('achiever', 'Achiever'),
        ('activator', 'Activator'),
        ('adaptability', 'Adaptability'),
        ('analytical', 'Analytical'),
        ('arranger', 'Arranger'),
        ('belief', 'Belief'),
        ('command', 'Command'),
        ('communication', 'Communication'),
        ('competition', 'Competition'),
        ('connectedness', 'Connectedness'),
        ('consistency', 'Consistency'),
        ('context', 'Context'),
        ('deliberative', 'Deliberative'),
        ('developer', 'Developer'),
        ('discipline', 'Discipline'),
        ('empathy', 'Empathy'),
        ('focus', 'Focus'),
        ('futuristic', 'Futuristic'),
        ('harmony', 'Harmony'),
        ('ideation', 'Ideation'),
        ('includer', 'Includer'),
        ('individualization', 'Individualization'),
        ('input', 'Input'),
        ('intellection', 'Intellection'),
        ('learner', 'Learner'),
        ('maximizer', 'Maximizer'),
        ('positivity', 'Positivity'),
        ('relator', 'Relator'),
        ('responsibility', 'Responsibility'),
        ('restorative', 'Restorative'),
        ('self_assurance', 'Self-Assurance'),
        ('significance', 'Significance'),
        ('strategic', 'Strategic'),
        ('woo', 'Woo')
    ]
    
    select_field = SelectMultipleField(
        'Select Your Strengths', 
        choices=CLIFTON_STRENGTHS, 
        validators=[InputRequired()]
    )
    group = StringField("Group", validators=[InputRequired(), Length(min=1, max=40)])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")
    
    # def validate_group(self, group):
    #     group = Group.objects(group_name=group.data).first()
    #     if group is not None:
    #         raise ValidationError("Group is taken")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=40)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=1, max=40)])
    submit = SubmitField("Login")

class LogMeeting(FlaskForm):
    members = StringField("Members (space-seperated usernames)", validators=[InputRequired(), Length(min=1, max=400)])
    # meeting_time = DateTimeLocalField("Meeting Time", format="%Y-%m-%dT%H:%M", validators=[InputRequired()])
    submit = SubmitField("Log")

class CreateGroup(FlaskForm):
    group = StringField("Group name", validators=[InputRequired(), Length(min=1, max=40)])
    members = StringField("Members (space-seperated usernames)", validators=[InputRequired(), Length(min=1, max=400)])
    submit = SubmitField("Create")

# class AddStrengthForm(FlaskForm):
#     CLIFTON_STRENGTHS = [
#         ('achiever', 'Achiever'),
#         ('activator', 'Activator'),
#         ('adaptability', 'Adaptability'),
#         ('analytical', 'Analytical'),
#         ('arranger', 'Arranger'),
#         ('belief', 'Belief'),
#         ('command', 'Command'),
#         ('communication', 'Communication'),
#         ('competition', 'Competition'),
#         ('connectedness', 'Connectedness'),
#         ('consistency', 'Consistency'),
#         ('context', 'Context'),
#         ('deliberative', 'Deliberative'),
#         ('developer', 'Developer'),
#         ('discipline', 'Discipline'),
#         ('empathy', 'Empathy'),
#         ('focus', 'Focus'),
#         ('futuristic', 'Futuristic'),
#         ('harmony', 'Harmony'),
#         ('ideation', 'Ideation'),
#         ('includer', 'Includer'),
#         ('individualization', 'Individualization'),
#         ('input', 'Input'),
#         ('intellection', 'Intellection'),
#         ('learner', 'Learner'),
#         ('maximizer', 'Maximizer'),
#         ('positivity', 'Positivity'),
#         ('relator', 'Relator'),
#         ('responsibility', 'Responsibility'),
#         ('restorative', 'Restorative'),
#         ('self_assurance', 'Self-Assurance'),
#         ('significance', 'Significance'),
#         ('strategic', 'Strategic'),
#         ('woo', 'Woo')
#     ]
    
#     select_field = SelectMultipleField(
#         'Select Your Strengths', 
#         choices=CLIFTON_STRENGTHS, 
#         validators=[InputRequired()]
#     )
#     submit_add_course = SubmitField("Add Strengths!")
