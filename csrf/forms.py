# csrf folder - forms

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class SendMessageForm(FlaskForm):
	msg = StringField('Send Message to Admin', validators=[DataRequired("Let Admin know what you want to say !!")])
	submit = SubmitField("Send")

class AddAdminUserForm(FlaskForm):
	username = StringField('Username')
	password = PasswordField('Password')
	isAdmin = HiddenField('isAdmin')
	submit = SubmitField("Add User")

class AddAdminUserForm2(FlaskForm):
	username = StringField('Username')
	password = PasswordField('Password')
	isAdmin = StringField('isAdmin')
	submit = SubmitField("Add User")