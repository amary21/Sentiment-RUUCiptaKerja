from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# import mysql.connector
from flask_login import LoginManager
from flask_jsglue import JSGlue

app = Flask(__name__)
app.config['SECRET_KEY'] = '19f714e604daf22d7689ebd80964265f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:''@localhost/ruu_ciptaker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'
login_manager.login_message = 'Anda belum login!'

jsglue = JSGlue()
jsglue.init_app(app)

from apps import routes
