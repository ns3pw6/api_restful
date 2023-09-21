from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

#
# Retrieve the database password from environment variables
#
pwd = os.getenv("db_password")

#
# Configure the SQLAlchemy database URI
#
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:'+ pwd +'@localhost:3306/apitest'

#
# Create a SQLAlchemy database instance
#
db = SQLAlchemy(app)