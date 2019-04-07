from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL 

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_HOST'] = 'localhost'

mysql = MySQL(app)

SQLALCHEMY_DATABASE_URI = 'postgresql://postgress:root@localhost/test'
SQLALCHEMY_TRACK_MODIFICATION = False
SECRET_KEY = '1234567890'
app.config.from_object(__name__)

db = SQLAlchemy(app)

from app import views