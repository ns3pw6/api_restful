from flask import request, jsonify
from flask_restful import Api
from resources.user import Users, User
from resources.account import Accounts, Account
from dotenv import load_dotenv
from server import app
import pymysql
import traceback
import os


# app = Flask(__name__)

#
# Create an API object for routing
#
api = Api(app)

#
# Load environment variables from a .env file
#
load_dotenv()

#
# Define API endpoints and link them to resources
#
api.add_resource(Users, '/users')
api.add_resource(User, '/user/<id>')
api.add_resource(Accounts, '/user/<user_id>/accounts')
api.add_resource(Account, '/user/<user_id>/account/<id>')

#
# Define error handling for exceptions
#
@app.errorhandler(Exception)
def handle_error(error):
    status_code = 500
    if type(error).__name__ == "NotFound":
        status_code = 404
    elif type(error).__name__ == "TypeError":
        status_code = 500
        
    return jsonify({'msg':type(error).__name__}), status_code

#
# Define a route for the root endpoint
#
@app.route('/')
def index():
    return 'Hello World'

@app.route('/user/<user_id>/account/<id>/deposit', methods = ['POST'])
def deposit(user_id, id):
    db, cursor, account = get_account(id)
    money = request.get_json()['money']
    balance = account['balance'] + int(money)
    sql = """
        UPDATE apitest.account SET balance = {} WHERE id = {} AND deleted IS NOT TRUE
    """.format(balance, id)
    
    response = {}
    try:
        cursor.execute(sql)
        response['msg'] = 'Success'
    except:
        traceback.print_exc()
        response['msg'] = 'Failed'
    
    db.commit()
    db.close()
    return jsonify(response)


#
# Define a route for depositing money into an account       
#
@app.route('/user/<user_id>/account/<id>/withdraw', methods = ['POST'])
def withdraw(user_id, id):
    db, cursor, account = get_account(id)
    money = request.get_json()['money']
    balance = account['balance'] - int(money)
    sql = """
        UPDATE apitest.account SET balance = {} WHERE id = {} AND deleted IS NOT TRUE
    """.format(balance, id)
    
    response = {}
    try:
        cursor.execute(sql)
        response['msg'] = 'Success'
    except:
        traceback.print_exc()
        response['msg'] = 'Failed'
    
    db.commit()
    db.close()
    return jsonify(response)
 

#
# Define a route for withdrawing money from an account
#
def get_account(id):
    db = pymysql.connect(host = 'localhost', user = 'root', password = os.getenv("db_password"), db = 'apitest')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """
        SELECT * FROM apitest.account WHERE id = '{}' AND deleted IS NOT TRUE
    """.format(id)
    
    cursor.execute(sql)
    return db, cursor, cursor.fetchone()

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port = 8000)