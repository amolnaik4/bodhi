# cors folder - routes

from flask import Flask, render_template, request, session, Blueprint, current_app, redirect, url_for, jsonify
from models import Flag
import os
from werkzeug.utils import secure_filename
from flask_cors import cross_origin


cors = Blueprint('cors', __name__)


@cors.route("/cors")
def cors_intro():
	return render_template("cors/cors.html")

@cors.route("/flag_file")
def flag_file():
	if 'username' in session:
		return render_template("cors/flag_file.html")
	else:
		return redirect(url_for('main.login'))


@cors.route("/flag3")
@cross_origin(supports_credentials=True)
def get_flag():
	# only for admin user
	if 'username' in session and session['admin'] == 'yes':
		chall_info = session['chall']
		flag_data = Flag.query.filter_by(chall=chall_info).first()
		return jsonify({"flag": flag_data.flag_value})
		
	else:
		return jsonify({"error":"You need to be Admin"}), 401


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@cors.route("/upload3", methods=['GET','POST'])
def file_upload():
	if 'username' in session and session['chall'] is not 'None':
		if request.method == 'POST':
			if 'file' not in request.files:
				msg =  'No file part'
				return render_template('cors/upload.html', msg=msg)
			file = request.files['file']
			if file.filename == '':
				msg =  'No selected file'
				return render_template('cors/upload.html', msg=msg)

			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
				link_file =  "%s%s.txt" % (current_app.config['PAGE_LINK_FILE'], session['chall'])
				f = open(link_file,'a')
				f.write('/%s\n' %(filename))
				f.close()
				msg = 'File uploaded successfully !'
				return render_template('cors/upload.html', msg=msg)

		return render_template('cors/upload.html')

	else:
		return redirect(url_for("main.login"))

