from flask_restful import Resource, reqparse
from flask import jsonify, make_response
import traceback
from server import db
from models import AccountModel

#
# Create a parser for handling request arguments
# Preventing SQL injection in Python, only accept these field
#
parser = reqparse.RequestParser()
parser.add_argument('balance')
parser.add_argument('account_number')
parser.add_argument('user_id')

#
# Define a class for handling individual account resources
#
class Account(Resource):    
    #
    # Handle HTTP GET request to retrieve account details by user_id and id_number
    #
    def get(self, user_id, id):
        ls = []
        account = AccountModel.query.filter_by(id = id, user_id = user_id, deleted = None).first()
        ls.append(account)
        return jsonify({'data' : list(map(lambda account : account.serialize(), ls))})
    
    #
    # Handle HTTP PATCH request to update account details by user_id and id_number
    #
    def patch(self, user_id, id):
        arg = parser.parse_args()
        account = AccountModel.query.filter_by(id = id, user_id = user_id, deleted = None).first()
        if arg['balance'] != None:
            account.balance = arg['balance']
        if arg['user_id'] != None:
            account.user_id = arg['user_id']
        if arg['account_number'] != None:
            account.account_number = arg['account_number']   
 
        response = {}
        status_code = 200
        try:
            db.session.commit()
            response['msg'] = 'Success'
        except:
            status_code = 400
            traceback.print_exc()
            response['msg'] = 'Failed'
        
        return make_response(jsonify(response), status_code)
    
    #
    # Handle HTTP DELETE request to mark an account as deleted by user_id and id_number
    # This is hard delete
    #
    def delete(self, user_id, id):
        account = AccountModel.query.filter_by(id = id, user_id = user_id, deleted = None).first()
        
        response = {}
        status_code = 200
        try:
            db.session.delete(account)
            db.session.commit()
            response['msg'] = 'Success'
        except:
            status_code = 400
            traceback.print_exc()
            response['msg'] = 'Failed'
            
        return make_response(jsonify(response), status_code)


#
# Define a class for handling multiple accounts of a user
#
class Accounts(Resource):
    #
    # Handle HTTP GET request to retrieve all accounts of a user
    #
    def get(self, user_id):
        accounts = AccountModel.query.filter_by(user_id = user_id, deleted = None).all()
        return jsonify({'data' : list(map(lambda accounts : accounts.serialize(), accounts))})
    
    #
    # Handle HTTP POST request to create a new account for a user
    #
    def post(self, user_id):
        arg = parser.parse_args()
        account = {
            'balance' : arg['balance'],
            'account_number' : arg['account_number'],
            'user_id' : arg['user_id']
        }
        
        response = {}
        status_code = 200
        try:
            new_account = AccountModel(user_id = account['user_id'], balance = account['balance'], account_number = account['account_number'])
            db.session.add(new_account)
            db.session.commit()
            response['msg'] = 'Success'
        except:
            status_code = 400
            traceback.print_exc()
            response['msg'] = 'Failed'
            
        return make_response(jsonify(response), status_code)
            