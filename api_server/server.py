from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
pwd = os.getenv("db_password")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:'+ pwd +'@localhost:3306/apitest'
db = SQLAlchemy(app)