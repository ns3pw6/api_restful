from flask import Flask
from flask_restful import Api
from resources.user import Users, User
from resources.account import Accounts, Account

app = Flask(__name__)
api = Api(app)

api.add_resource(Users, '/users')
api.add_resource(User, '/user/<id>')
api.add_resource(Accounts, '/user/<user_id>/accounts')
api.add_resource(Account, '/user/<user_id>/account/<id>')

@app.route('/')
def index():
    return 'Hello World'

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port = 8000)