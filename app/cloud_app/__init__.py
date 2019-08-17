from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# FLASK_APP=app.py
# FLASK_DEBUG=1

app = Flask(__name__)
app.config['SECRET_KEY'] = '2dfb5258eda9b125e3252bfc43c71ed1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # relative path
db = SQLAlchemy(app)

from cloud_app import routes