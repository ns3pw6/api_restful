from flask import Flask, request, jsonify
from flask_restful import Api
from resources.user import Users, User
from resources.account import Accounts, Account
import pymysql
import traceback


app = Flask(__name__)
api = Api(app)

api.add_resource(Users, '/users')
api.add_resource(User, '/user/<id>')
api.add_resource(Accounts, '/user/<user_id>/accounts')
api.add_resource(Account, '/user/<user_id>/account/<id>')

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
 
        
def get_account(id):
    db = pymysql.connect(host = 'localhost', user = 'root', password = 'zyhdEx-3timma-rotsiv', db = 'apitest')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """
        SELECT * FROM apitest.account WHERE id = '{}' AND deleted IS NOT TRUE
    """.format(id)
    
    cursor.execute(sql)
    return db, cursor, cursor.fetchone()

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port = 8000)