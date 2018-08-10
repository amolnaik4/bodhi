from flask import Flask, render_template, request, session, redirect, url_for
from forms import LoginForm, SendMessageForm, AddAdminUserForm, AddAdminUserForm2
import os
from models import db, Message, ChallInfo, Flag, User2
import xml.etree.ElementTree as ET
from werkzeug.utils import secure_filename



app = Flask(__name__)



project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "app_database.db"))
UPLOAD_FOLDER = os.path.join(project_dir, "uploads/")
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','html','htm','js'])
page_link_file = os.path.join(project_dir, "another_server/")


app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db.init_app(app)

app.secret_key = "afb46675-3f80-41df-8420-20ec9a6a13f6"

@app.route("/")
def index():
	if not os.path.isfile(project_dir+'/bot_ip.txt'):
		return render_template("setup_bot.html")
	else:
		return render_template("index.html")


@app.route("/bot", methods=['GET','POST'])
def bot():
	if request.method == 'POST':
		f = open(project_dir+'/bot_ip.txt','w')
		ip_addr = request.form['ip']
		f.write(ip_addr)
		f.close()
		return redirect(url_for("index"))
	
	elif request.method == 'GET':
		return render_template("setup_bot.html")


@app.route("/csrf")
def csrf_intro():
	return render_template("csrf.html")


@app.route("/home")
def home():
	if 'username' in session:
		chall = session['chall']
		chall_data = ChallInfo.query.filter_by(chall=chall).first()
		return render_template("home.html",chall_data=chall_data)
	else:
		return redirect(url_for("login"))
	

@app.route("/login", methods=['GET','POST'])
def login():
	if 'username' in session:
		return redirect(url_for("home"))

	form = LoginForm()

	if request.method == "POST":
		if form.validate() == False:
			return render_template("login.html", form=form)
		else:
			user = form.username.data
			password = form.password.data
			
			db_user = User2.query.filter_by(username=user).first()
			if db_user is not None and db_user.check_password(password) and db_user.chall == session['chall']:
				session['username'] = user
				session['admin'] = db_user.isAdmin
				return redirect(url_for("home"))
			else:
				msg = "Username/Password Incorrect"
				return render_template("login.html", msg=msg, form=form)

	elif request.method == "GET":
		return render_template("login.html", form=form)


@app.route("/send_message", methods=['GET','POST'])
def send_message():
	if 'username' in session:
		form = SendMessageForm()

		if request.method == 'POST':
			newmsg = Message(session['username'],form.msg.data, session['chall'])
			db.session.add(newmsg)
			db.session.commit()
			user_msg = "Message sent to Admin"

			return render_template("send_message.html", form=form, msg=user_msg)

		elif request.method == 'GET':
			return render_template("send_message.html", form=form)

	else:
		return redirect(url_for("login"))


@app.route("/add_admin",methods=['GET','POST'])
def add_admin():
	# only for admin user
	if 'username' in session and session['admin'] == 'yes':
		form = AddAdminUserForm()
		form2 = AddAdminUserForm2()

		if request.method == 'POST':
			print "in POST, cehcking session['chall']: %s" % (session['chall'])
			if session['chall'] == 'csrf2':
			
				newuser = User2(form.username.data, form.password.data, form.isAdmin.data, session['chall'])
				db.session.add(newuser)
				db.session.commit()
				return render_template("add_admin_post.html", form=form)

			elif session['chall'] == 'csrf3':
				data = request.get_json()
				
				username = data.get('username')
				password = data.get('password')
				isAdmin = data.get('isAdmin')

				newuser2 = User2(username,password,isAdmin,session['chall'])
				db.session.add(newuser2)
				db.session.commit()
				return render_template("add_admin_json.html", form=form)

			elif session['chall'] == 'csrf4':
				data = request.data
				tree = ET.fromstring(data)
				data1 = tree.find('.//{tns}username').text
				data2 = tree.find('.//{tns}password').text
				data3 = tree.find('.//{tns}isAdmin').text
				
				newuser3 = User2(data1, data2, data3, session['chall'])
				db.session.add(newuser3)
				db.session.commit()
				return render_template("add_admin_xml.html", form=form)

			elif session['chall'] == 'csrf5':
				# step 1, display username, password form
				if 'step' not in request.form:
					return render_template("add_admin_multi_steps.html", step="one")
				# step 2, accepts username/password & display isAdmin
				elif request.form["step"] == "two":
					user = request.form['username']
					pwd = request.form['password']
					return render_template("add_admin_multi_steps.html", step="two", user=user, pwd=pwd)
				# step 3, accepts username/password/isAdmin  from form, display message
				elif request.form["step"] == "final":
					user = request.form['username']
					pwd = request.form['password']
					isAdmin = request.form['isAdmin']
					newuser4 = User2(user,pwd,isAdmin, session['chall'])
					db.session.add(newuser4)
					db.session.commit()
					msg = "user creatd"
					return render_template("add_admin_multi_steps.html", step="final", msg=msg)

			elif session['chall'] == 'csrf6':
				if form2.validate():
					newuser = User2(form2.username.data, form2.password.data, form2.isAdmin.data, session['chall'])
					print newuser
					db.session.add(newuser)
					db.session.commit()
					return render_template("add_admin_post_token.html", form=form2)
				else:
					msg = "Form tampered, please send again"
					return render_template("add_admin_post_token.html", form=form2, msg=msg)

		elif request.method == 'GET':
			if request.args:
				newuser1 = User2(request.args.get('username'), request.args.get('password'), request.args.get('isAdmin'), session['chall'])
				db.session.add(newuser1)
				db.session.commit()
				return render_template("add_admin_get.html", form=form)
			else:
				print "checking session['chall'] in GET else: %s" % (session['chall'])
				if session['chall'] == 'csrf1':
					return render_template("add_admin_get.html", form=form)
				elif session['chall'] == 'csrf2':
					return render_template("add_admin_post.html", form=form)
				elif session['chall'] == 'csrf3':
					return render_template("add_admin_json.html", form=form)
				elif session['chall'] == 'csrf4':
					return render_template("add_admin_xml.html", form=form)
				elif session['chall'] == 'csrf5':
					return render_template("add_admin_multi_steps.html", form=form, step="one")
				elif session['chall'] == 'csrf6':
					return render_template("add_admin_post_token.html", form=form2)
	else:
		return redirect(url_for("login"))

@app.route("/add_admin_demo",methods=['GET','POST'])
def add_admin_demo():
	if 'username' in session:
		form = AddAdminUserForm()
		form2 = AddAdminUserForm2()

		if request.method == 'POST':
			print "in POST, cehcking session['chall']: %s" % (session['chall'])
			if session['chall'] == 'csrf2':
			
				return render_template("add_admin_post.html", form=form)

			elif session['chall'] == 'csrf3':
				data = request.get_json()
				
				username = data.get('username')
				password = data.get('password')
				isAdmin = data.get('isAdmin')

				return render_template("add_admin_json.html", form=form)

			elif session['chall'] == 'csrf4':
				data = request.data
				tree = ET.fromstring(data)
				data1 = tree.find('.//{tns}username').text
				data2 = tree.find('.//{tns}password').text
				data3 = tree.find('.//{tns}isAdmin').text
				
				return render_template("add_admin_xml.html", form=form)

			elif session['chall'] == 'csrf5':
				if 'step' not in request.form:
					return render_template("add_admin_multi_steps2.html", step="one")
				# step 2, accepts username/password & display isAdmin
				elif request.form["step"] == "two":
					user = request.form['username']
					pwd = request.form['password']
					msg = "Note: change form action as '/add_admin' in payload "
					return render_template("add_admin_multi_steps2.html", step="two", user=user, pwd=pwd, msg=msg)
				# step 3, accepts username/password/isAdmin  from form, display message
				elif request.form["step"] == "final":
					user = request.form['username']
					pwd = request.form['password']
					isAdmin = request.form['isAdmin']
					msg = "user creatd"
					return render_template("add_admin_multi_steps2.html", step="final", msg=msg)

			elif session['chall'] == 'csrf6':
				if form2.validate():
					return render_template("add_admin_post_token.html", form=form2)
				else:
					msg = "Form tampered, please send again"
					return render_template("add_admin_post_token.html", form=form2, msg=msg)

		elif request.method == 'GET':
			if request.args:
				return render_template("add_admin_get.html", form=form)
			else:
				print "checking session['chall'] in GET else: %s" % (session['chall'])
				if session['chall'] == 'csrf1':
					return render_template("add_admin_get.html", form=form)
				elif session['chall'] == 'csrf2':
					return render_template("add_admin_post.html", form=form)
				elif session['chall'] == 'csrf3':
					return render_template("add_admin_json.html", form=form)
				elif session['chall'] == 'csrf4':
					return render_template("add_admin_xml.html", form=form)
				elif session['chall'] == 'csrf5':
					msg = "Note: change form action as '/add_admin' in payload "
					return render_template("add_admin_multi_steps2.html", form=form, step="one", msg=msg)
				elif session['chall'] == 'csrf6':
					return render_template("add_admin_post_token.html", form=form2)
	else:
		return redirect(url_for("login"))

@app.route("/flag")
def get_flag():
	# only for admin user
	if 'username' in session and session['admin'] == 'yes':
		chall_info = session['chall']
		flag_data = Flag.query.filter_by(chall=chall_info).first()
		return render_template("flag.html", flag=flag_data)

@app.route("/admin_messages")
def admin_messages():
	# only for admin user
	if 'username' in session and session['admin'] == 'yes':
		messages = Message.query.filter_by(chall=session['chall']).all()
		return render_template("admin_messages.html", messages = messages)
	else:
		return redirect(url_for('login'))

@app.route("/logout")
def logout():
	session.pop('username', None)
	session.pop('isAdmin', None)
	session.pop('chall', None)
	return redirect(url_for("index"))


@app.route("/info/<chall>")
def info_chall(chall):
	chall_data = ChallInfo.query.filter_by(chall=chall).first()
	session['chall'] = chall
	return render_template("info.html", chall_data=chall_data)


@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error))
    return render_template('500.htm'), 500

@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error('Unhandled Exception: %s', (e))
    return render_template('500.htm'), 500


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=['GET','POST'])
def file_upload():
	if 'username' in session and session['chall'] is not 'None':
		if request.method == 'POST':
			if 'file' not in request.files:
				msg =  'No file part'
				return render_template('upload.html', msg=msg)
			file = request.files['file']
			if file.filename == '':
				msg =  'No selected file'
				return render_template('upload.html', msg=msg)

			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				link_file =  "%s%s.txt" % (page_link_file, session['chall'])
				f = open(link_file,'a')
				f.write('/%s\n' %(filename))
				f.close()
				msg = 'File uploaded successfully !'
				return render_template('upload.html', msg=msg)

		return render_template('upload.html')

	else:
		return redirect(url_for("login"))

if __name__ == "__main__":
	app.run(debug=False, threaded=True, host='0.0.0.0', port='80')

