# clickjack folder - routes
from flask import Flask, render_template, request, session, Blueprint, current_app
from clickjack.forms import UpdateUser
from models import User2, db, Flag
import os
from werkzeug.utils import secure_filename

clickjack = Blueprint('clickjack', __name__)


@clickjack.route("/clickjack")
def clickjacking_intro():
	return render_template("clickjack/clickjack.html")


@clickjack.route("/update_user", methods=['GET','POST'])
def update_user():
	if 'username' in session:
		if  session['chall'] == 'click1':
			db_user = User2.query.filter_by(username='testuser7').first()
			form = UpdateUser(obj=db_user)
			if request.method == 'POST':
				if form.validate():
					if session['admin'] == 'yes':
						db_user.isAdmin = 'yes'
						db.session.commit()
					msg = "User updated"
					return render_template("clickjack/single_click_update.html",form=form, msg=msg)
			elif request.method == 'GET':
				return render_template("clickjack/single_click_update.html",form=form)

		if session['chall'] == 'click2':
			db_user2 = User2.query.filter_by(username='testuser8').first()
			form = UpdateUser(obj=db_user2)
			if request.method == 'POST':
				if form.validate():
					if session['admin'] == 'yes':
						admin_data = form.isAdmin.data
						if admin_data:
							db_user2.isAdmin = admin_data
						else:
							db_user2.isAdmin = 'no'
						db.session.commit()
					msg = "User updated"
					return render_template("clickjack/double_click_update.html",form=form, msg=msg)
			elif request.method == 'GET':
				return render_template("clickjack/double_click_update.html",form=form)

@clickjack.route("/flag2")
def get_flag():
	# only for admin user
	if 'username' in session and session['admin'] == 'yes':
		chall_info = session['chall']
		flag_data = Flag.query.filter_by(chall=chall_info).first()
		return render_template("clickjack/flag.html", flag=flag_data)
	else:
		return redirect(url_for('main.login'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@clickjack.route("/upload2", methods=['GET','POST'])
def file_upload():
	if 'username' in session and session['chall'] is not 'None':
		if request.method == 'POST':
			if 'file' not in request.files:
				msg =  'No file part'
				return render_template('clickjack/upload.html', msg=msg)
			file = request.files['file']
			if file.filename == '':
				msg =  'No selected file'
				return render_template('clickjack/upload.html', msg=msg)

			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
				link_file =  "%s%s.txt" % (current_app.config['PAGE_LINK_FILE'], session['chall'])
				f = open(link_file,'a')
				f.write('/%s\n' %(filename))
				f.close()
				msg = 'File uploaded successfully !'
				return render_template('clickjack/upload.html', msg=msg)

		return render_template('clickjack/upload.html')

	else:
		return redirect(url_for("main.login"))

