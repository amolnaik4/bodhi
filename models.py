from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User2(db.Model):
	__tablename__ = 'appusers'
	uid = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(100))
	pwdhash = db.Column(db.String(54))
	isAdmin = db.Column(db.String(100))
	chall = db.Column(db.String(100))

	def __init__(self, username, password, isAdmin, chall):
		self.username = username
		self.isAdmin = isAdmin
		self.chall = chall
		self.set_password(password)

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)

class Message(db.Model):
	__tablename__ = 'admin_messages'
	id = db.Column(db.Integer, primary_key = True)
	sender = db.Column(db.String(100))
	msg = db.Column(db.String(500))
	chall = db.Column(db.String(100))

	def __init__(self, sender, msg, chall):
		self.sender = sender
		self.msg = msg
		self.chall = chall


class ChallInfo(db.Model):
	__tablename__ = 'chall_info'
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100))
	description = db.Column(db.String(500))
	vuln_request = db.Column(db.String(100))
	link = db.Column(db.String(100))
	chall = db.Column(db.String(100))

	def __init__(self, title, description, vuln_request, link, chall):
		self.title = title
		self.description = description
		self.vuln_request = vuln_request
		self.link = link
		self.chall = chall

class Flag(db.Model):
	__tablename__ = 'flags'
	id = db.Column(db.Integer, primary_key = True)
	flag_value = db.Column(db.String(100))
	chall = db.Column(db.String(100))

	def __init__(self, flag_value, chall):
		self.flag_value = flag_value
		self.chall = chall
