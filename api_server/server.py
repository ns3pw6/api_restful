from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zyhdEx-3timma-rotsiv@localhost:3306/apitest'
db = SQLAlchemy(app)