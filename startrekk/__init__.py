from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY']= 'fdsfdasfdsafrqgopmtbombbgrer'
db = SQLAlchemy(app)

from startrekk import routes