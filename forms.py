from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired

class SignUpForm(FlaskForm):
    inputFirstName = StringField('First Name', 
        [DataRequired(message="Please enter your first name!")])
    inputLastName = StringField('Last Name', 
        [DataRequired(message="Please enter your last name!")])
    inputEmail = StringField('Email address',
        [Email(message="Not a valid email address!"),
        DataRequired(message="Please enter your email address!")])
    inputPassword =  PasswordField('Password',
        [InputRequired(message="Please enter your password!"),
        EqualTo('inputConfirmPassword', message="Password does not match!")])
    inputConfirmPassword =  PasswordField('Confirm Password')
    submit = SubmitField('Sign Up')

class SignInForm(FlaskForm):
    inputEmail = StringField('Email address',
        [Email(message="Not a valid email address!"),
        DataRequired(message="Please enter your email address!")])
    inputPassword =  PasswordField('Password',
        [InputRequired(message="Please enter your password!")])
    submit = SubmitField('Sign In')

class TaskForm(FlaskForm):
    inputDescription =  StringField('Task Description',
        [DataRequired(message="Please enter your task content!")])
    inputPriority = SelectField('Priority', coerce = int)

    submitAddTask = SubmitField('Create Task')

class ProjectForm(FlaskForm):
    Name = StringField('Name', validators=[
        DataRequired(message='Please enter a name'),
    ])

    Description = StringField('Description', validators=[
        DataRequired(message='Please enter a description'),
    ])

    Deadline = DateField('Deadline', validators=[
        DataRequired(message='Please choose a deadline'),
    ])

    Status = SelectField('Status', coerce=int)

    submitAddProject = SubmitField('Add Project')
    submitUpdateProject = SubmitField('Update Project')

