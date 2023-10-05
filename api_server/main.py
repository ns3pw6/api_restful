from flask import request, jsonify, make_response
from flask_restful import Api
from resources.user import Users, User
from resources.account import Accounts, Account
from dotenv import load_dotenv
from server import app, db
from models import AccountModel
import traceback


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

#
# Define a route for depositing money into an account       
#
@app.route('/user/<user_id>/account/<id>/deposit', methods = ['POST'])
def deposit(user_id, id):
    account = AccountModel.query.filter_by(user_id = user_id, id = id).first()
    money = int(request.get_json()['money'])
    response = {}
    status_code = 200

    if money > 0:
        account.balance += money
    else:
        status_code = 400
        response['msg'] = 'Invalid number'
        return make_response(jsonify(response), status_code)
    

    try:
        db.session.commit()
        response['msg'] = 'Success'
    except:
        status_code = 400
        traceback.print_exc()
        response['msg'] = 'Failed'

    return make_response(jsonify(response), status_code)


#
# Define a route for withdrawing money from an account       
#
@app.route('/user/<user_id>/account/<id>/withdraw', methods = ['POST'])
def withdraw(user_id, id):
    account = AccountModel.query.filter_by(user_id = user_id, id = id).first()
    money = int(request.get_json()['money'])
    response = {}
    status_code = 200

    if money > 0:
        if account.balance < money:
            status_code = 400
            response['msg'] = 'No sufficient money'
            return make_response(jsonify(response), status_code)
        account.balance -= money
    else:
        status_code = 400
        response['msg'] = 'Invalid number'
        return make_response(jsonify(response), status_code)
    
    
    try:
        db.session.commit()
        response['msg'] = 'Success'
    except:
        status_code = 400
        traceback.print_exc()
        response['msg'] = 'Failed'
    print('here')
    return make_response(jsonify(response), status_code)
 
if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port = 8000)