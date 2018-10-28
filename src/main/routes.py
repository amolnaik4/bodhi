# main folder - routes
from flask import render_template, request, session, redirect, url_for, Blueprint
from main.forms import LoginForm, AddChallInfo, AddUsersDBNew, AddFlag, ReadDB
import os, re
from models import db, ChallInfo, User2, Flag


main = Blueprint('main', __name__)

file_path = os.path.dirname(os.path.abspath(__file__))
project_dir = file_path +"/../"
print project_dir

@main.route("/")
def index():
	if not os.path.isfile(project_dir+'/bot_ip.txt'):
		return render_template("main/setup_bot.html")
	else:
		return render_template("main/index.html")


@main.route("/bot", methods=['GET','POST'])
def bot():
	if request.method == 'POST':
		f = open(project_dir+'/bot_ip.txt','w')
		ip_addr = request.form['ip']
		f.write(ip_addr)
		f.close()
		return redirect(url_for("main.index"))
	
	elif request.method == 'GET':
		return render_template("main/setup_bot.html")


@main.route("/home")
def home():
	print session['chall']
	if 'username' in session:
		chall = session['chall']
		chall_data = ChallInfo.query.filter_by(chall=chall).first()
		if re.match(r"csrf[0-9]", chall):
			return render_template("csrf/home.html",chall_data=chall_data)
		elif re.match(r"click[0-9]", chall):
			return render_template("clickjack/home.html",chall_data=chall_data)
	else:
		return redirect(url_for("main.login"))



@main.route("/login", methods=['GET','POST'])
def login():
	if 'username' in session:
		return redirect(url_for("main.home"))

	form = LoginForm()

	if request.method == "POST":
		if form.validate() == False:
			return render_template("main/login.html", form=form)
		else:
			user = form.username.data
			password = form.password.data
			
			db_user = User2.query.filter_by(username=user).first()
			if db_user is not None and db_user.check_password(password) and db_user.chall == session['chall']:
				session['username'] = user
				session['admin'] = db_user.isAdmin
				return redirect(url_for("main.home"))
			else:
				msg = "Username/Password Incorrect"
				return render_template("main/login.html", msg=msg, form=form)

	elif request.method == "GET":
		session['chall'] = request.args.get("chall")
		return render_template("main/login.html", form=form)



@main.route("/logout")
def logout():
	session.pop('username', None)
	session.pop('isAdmin', None)
	session.pop('chall', None)
	return redirect(url_for("main.index"))


@main.route("/info/<chall>")
def info_chall(chall):
	chall_data = ChallInfo.query.filter_by(chall=chall).first()
	return render_template("main/info.html", chall_data=chall_data)
