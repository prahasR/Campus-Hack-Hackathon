from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class QueryForm(FlaskForm):
    query = StringField(validators=[DataRequired(), Length(min=0, max=50)])
    #email = StringField('Email',
    #                    validators=[DataRequired(), Email()])
    #password = PasswordField('Password', validators=[DataRequired()])
    #confirm_password = PasswordField('Confirm Password',
    #                                 validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Go')
class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=0, max=20)])
    
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class CourseForm(FlaskForm):
    sem = StringField('SEMESTER(eg. 2002)',
                               validators=[DataRequired(), Length(min=0, max=50)])
    cour = StringField('COURSE(eg. PYL101) ', validators=[DataRequired()])
    #remember = BooleanField('Remember Me')
    submit = SubmitField('Go') 

class SelectionForm(FlaskForm):
    ans = IntegerField(validators=[DataRequired()])
    #email = StringField('Email',
    #                    validators=[DataRequired(), Email()])
    #password = PasswordField('Password', validators=[DataRequired()])
    #confirm_password = PasswordField('Confirm Password',
    #validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Go')


class TaskForm(FlaskForm):
    task = IntegerField(validators=[DataRequired(), Length(min=0, max=20)])
    
    submit = SubmitField('Go')

class DateForm(FlaskForm):
    date = StringField('Date(01-31)',
                        validators=[DataRequired(), Length(min=0, max=20)])
    mon = StringField('Month(eg. January)',
                        validators=[DataRequired()])
    submit = SubmitField('Go')
#class RegistrationForm(FlaskForm):
#    username = StringField('Username',
#                           validators=[DataRequired(), Length(min=2, max=20)])
#    email = StringField('Email',
#                        validators=[DataRequired(), Email()])
#    password = PasswordField('Password', validators=[DataRequired()])
#    confirm_password = PasswordField('Confirm Password',
#                                     validators=[DataRequired(), EqualTo('password')])
#    submit = SubmitField('Sign Up')
