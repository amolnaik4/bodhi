# csrf folder - routes
from flask import render_template, request, session, redirect, url_for, Blueprint, current_app
from csrf.forms import SendMessageForm, AddAdminUserForm, AddAdminUserForm2
from models import db, Message, Flag, User2
import xml.etree.ElementTree as ET
from werkzeug.utils import secure_filename
import os

csrf = Blueprint('csrf', __name__)


@csrf.route("/csrf")
def csrf_intro():
	return render_template("csrf/csrf.html")


@csrf.route("/send_message", methods=['GET','POST'])
def send_message():
	if 'username' in session:
		form = SendMessageForm()

		if request.method == 'POST':
			newmsg = Message(session['username'],form.msg.data, session['chall'])
			db.session.add(newmsg)
			db.session.commit()
			user_msg = "Message sent to Admin"

			return render_template("csrf/send_message.html", form=form, msg=user_msg)

		elif request.method == 'GET':
			return render_template("csrf/send_message.html", form=form)

	else:
		return redirect(url_for("main.login"))


@csrf.route("/add_admin",methods=['GET','POST'])
def add_admin():
	if 'username' in session:
		form = AddAdminUserForm()
		form2 = AddAdminUserForm2()

		if request.method == 'POST':
			if session['chall'] == 'csrf2':
				if session['admin'] == 'yes':
					try:
						newuser = User2(form.username.data, form.password.data, form.isAdmin.data, session['chall'])
						db.session.add(newuser)
						db.session.commit()
					except:
						print "This username already exists"

				msg = "User Created"
				return render_template("csrf/add_admin_post.html", form=form, msg=msg)

			elif session['chall'] == 'csrf3':
				data = request.get_json()
				
				username = data.get('username')
				password = data.get('password')
				isAdmin = data.get('isAdmin')

				if session['admin'] == 'yes':
					try:
						newuser2 = User2(username,password,isAdmin,session['chall'])
						db.session.add(newuser2)
						db.session.commit()
					except:
						print "This username already exists"

				msg = "User Created"
				return msg

			elif session['chall'] == 'csrf4':
				data = request.data
				tree = ET.fromstring(data)
				data1 = tree.find('.//{tns}username').text
				data2 = tree.find('.//{tns}password').text
				data3 = tree.find('.//{tns}isAdmin').text
				
				if session['admin'] == 'yes':
					try:
						newuser3 = User2(data1, data2, data3, session['chall'])
						db.session.add(newuser3)
						db.session.commit()
					except:
						print "This username already exists"

				msg = "User Created"
				return msg

			elif session['chall'] == 'csrf5':
				# step 1, display username, password form
				if 'step' not in request.form:
					return render_template("csrf/add_admin_multi_steps.html", step="one")
				# step 2, accepts username/password & display isAdmin
				elif request.form["step"] == "two":
					user = request.form['username']
					pwd = request.form['password']
					return render_template("csrf/add_admin_multi_steps.html", step="two", user=user, pwd=pwd)
				# step 3, accepts username/password/isAdmin  from form, display message
				elif request.form["step"] == "final":
					user = request.form['username']
					pwd = request.form['password']
					isAdmin = request.form['isAdmin']
					if session['admin'] == 'yes':
						try:
							newuser4 = User2(user,pwd,isAdmin, session['chall'])
							db.session.add(newuser4)
							db.session.commit()
						except:
							print "This username already exists"

					msg = "User Created"
					return render_template("csrf/add_admin_multi_steps.html", step="final", msg=msg)

			elif session['chall'] == 'csrf6':
				if form2.validate():
					if session['admin'] == 'yes':
						try:
							newuser = User2(form2.username.data, form2.password.data, form2.isAdmin.data, session['chall'])
							db.session.add(newuser)
							db.session.commit()
						except:
							print "This username already exists"

					msg = "User Created"
					return render_template("csrf/add_admin_post_token.html", form=form2, msg=msg)
				else:
					msg = "Form tampered, please send again"
					return render_template("csrf/add_admin_post_token.html", form=form2, msg=msg)

		elif request.method == 'GET':
			if request.args:
				if session['admin'] == 'yes':
					try:
						newuser1 = User2(request.args.get('username'), request.args.get('password'), request.args.get('isAdmin'), session['chall'])
						db.session.add(newuser1)
						db.session.commit()
					except:
						print "This username already exists"
						
				msg = "User Created"
				return render_template("csrf/add_admin_get.html", form=form, msg=msg)
			else:
				print "checking session['chall'] in GET else: %s" % (session['chall'])
				if session['chall'] == 'csrf1':
					return render_template("csrf/add_admin_get.html", form=form)
				elif session['chall'] == 'csrf2':
					return render_template("csrf/add_admin_post.html", form=form)
				elif session['chall'] == 'csrf3':
					return render_template("csrf/add_admin_json.html", form=form)
				elif session['chall'] == 'csrf4':
					return render_template("csrf/add_admin_xml.html", form=form)
				elif session['chall'] == 'csrf5':
					return render_template("csrf/add_admin_multi_steps.html", form=form, step="one")
				elif session['chall'] == 'csrf6':
					return render_template("csrf/add_admin_post_token.html", form=form2)
	else:
		return redirect(url_for("main.login"))


@csrf.route("/flag")
def get_flag():
	# only for admin user
	if 'username' in session and session['admin'] == 'yes':
		chall_info = session['chall']
		flag_data = Flag.query.filter_by(chall=chall_info).first()
		return render_template("csrf/flag.html", flag=flag_data)
	else:
		return redirect(url_for('main.login'))


@csrf.route("/admin_messages")
def admin_messages():
	# only for admin user
	if 'username' in session and session['admin'] == 'yes':
		messages = Message.query.filter_by(chall=session['chall']).all()
		return render_template("csrf/admin_messages.html", messages = messages)
	else:
		return redirect(url_for('main.login'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@csrf.route("/upload", methods=['GET','POST'])
def file_upload():
	if 'username' in session and session['chall'] is not 'None':
		if request.method == 'POST':
			if 'file' not in request.files:
				msg =  'No file part'
				return render_template('csrf/upload.html', msg=msg)
			file = request.files['file']
			if file.filename == '':
				msg =  'No selected file'
				return render_template('csrf/upload.html', msg=msg)

			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
				link_file =  "%s%s.txt" % (current_app.config['PAGE_LINK_FILE'], session['chall'])
				f = open(link_file,'a')
				f.write('/%s\n' %(filename))
				f.close()
				msg = 'File uploaded successfully !'
				return render_template('csrf/upload.html', msg=msg)

		return render_template('csrf/upload.html')

	else:
		return redirect(url_for("main.login"))


