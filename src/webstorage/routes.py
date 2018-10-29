# webstorate folder - routes

from flask import Flask, render_template, request, session, Blueprint, current_app, redirect, url_for, jsonify
from models import Flag, ChallInfo, Message, db
from csrf.forms import SendMessageForm
import os


webstorage = Blueprint('webstorage', __name__)


@webstorage.route("/webstorage")
def webstorage_intro():
	return render_template("webstorage/webstorage.html")

@webstorage.route("/home2")
def new_home():
	if 'username' in session:
		chall = session['chall']
		chall_info = ChallInfo.query.filter_by(chall=chall).first()
		if session['admin'] == 'yes':
			flag_data = Flag.query.filter_by(chall=chall).first()
			return render_template("webstorage/new_home.html", flag_data=flag_data.flag_value, chall_data=chall_info)
		else:
			flag = "THIS_IS_DUMMY_FLAG"
			return render_template("webstorage/new_home.html", flag_data=flag, chall_data=chall_info)
	else:
		return redirect(url_for("main.login"))


@webstorage.route("/flag4")
def get_flag():
	# only for admin user
	if 'username' in session:
		return render_template("webstorage/flag.html")
	else:
		return redirect(url_for("main.login"))


@webstorage.route("/send_message2", methods=['GET','POST'])
def send_message():
	if 'username' in session:
		form = SendMessageForm()

		if request.method == 'POST':
			newmsg = Message(session['username'],form.msg.data, session['chall'])
			db.session.add(newmsg)
			db.session.commit()
			user_msg = "Message sent to Admin"

			return render_template("webstorage/send_message.html", form=form, msg=user_msg)

		elif request.method == 'GET':
			return render_template("webstorage/send_message.html", form=form)

	else:
		return redirect(url_for("main.login"))

