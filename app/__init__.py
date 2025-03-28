# app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Set the path for the templates folder
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
# Set the path for the static folder
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static')

# Initialize the Flask app with both template and static folder paths
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'inventory.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ENV']="development"
app.config['DEBUG']=True

db = SQLAlchemy(app)

from app import routes, auth, users, locations, items, reports
