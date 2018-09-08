from flask import Flask
import os
from models import db


app = Flask(__name__)


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "app_database.db"))
UPLOAD_FOLDER = os.path.join(project_dir, "uploads/")
page_link_file = os.path.join(project_dir, "another_server/")


app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','html','htm','js'])
app.config['PAGE_LINK_FILE'] = page_link_file
db.init_app(app)

app.secret_key = "afb46675-3f80-41df-8420-20ec9a6a13f6"


from main.routes import main
from csrf.routes import csrf
from clickjack.routes import clickjack


app.register_blueprint(main)
app.register_blueprint(csrf)
app.register_blueprint(clickjack)




@main.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error))
    return render_template('500.htm'), 500

@main.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error('Unhandled Exception: %s', (e))
    return render_template('500.htm'), 500



if __name__ == "__main__":
	app.run(debug=False, threaded=True, host='0.0.0.0', port='80')

