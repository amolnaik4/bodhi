# clickjack folder - forms

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class UpdateUser(FlaskForm):
	username = StringField('Username')
	isAdmin = StringField('isAdmin')
	submit = SubmitField("Update User")