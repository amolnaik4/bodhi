# main folder - forms

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired("Please enter your email address.")])
	password = PasswordField('Password', validators=[DataRequired("Please enter your password.")])
	submit = SubmitField("Sign in")

class AddChallInfo(FlaskForm):
	title = StringField('title')
	description = StringField('description')
	vuln_request = StringField('vuln_request')
	link = StringField('link')
	chall = StringField('chall')
	submit = SubmitField("Add Info")

class AddUsersDBNew(FlaskForm):
	username = StringField('username')
	password = PasswordField('Password')
	isAdmin = StringField('isAdmin')
	chall = StringField('chall')
	submit = SubmitField("Add New User")

class AddFlag(FlaskForm):
	flag_value = StringField('flag_value')
	chall = StringField('chall')
	submit = SubmitField("Add New Flag")


class ReadDB(FlaskForm):
	table_name = StringField('table_name')
	submit = SubmitField('Get Table Details')