from flask_restful import Resource, reqparse
from flask import jsonify
import pymysql
import traceback

parser = reqparse.RequestParser()
parser.add_argument('balance')
parser.add_argument('account_number')
parser.add_argument('user_id')

class Account(Resource):
    def db_init(self):
        db = pymysql.connect(host = 'localhost', user = 'root', password = 'zyhdEx-3timma-rotsiv', db = 'apitest')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    
    def get(self, user_id, id):
        db, cursor = self.db_init()
        sql = """
            SELECT * FROM apitest.account WHERE user_id = '{}' AND id = '{}'
        """.format(user_id, id)
        
        cursor.execute(sql)
        
        db.commit()
        account = cursor.fetchone()
        db.close()
        return jsonify({'data' : account})
    
    def patch(self, user_id, id):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        account = {
            'user_id' : arg['user_id'],
            'balance' : arg['balance'],
            'account_number' : arg['account_number']
        }
        query = []
        for key, value in account.items():
            if value != None:
                query.append(key + " = " + "'{}' ".format(value))
        query = ','.join(query)

        sql = """
            UPDATE `apitest`.`account` SET {} WHERE (`user_id` = '{}' AND `id` = '{}')
        """.format(query, user_id, id)
        
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
    
    def delete(self, user_id, id):
        db, cursor = self.db_init()
        sql = """
            UPDATE `apitest`.`account` SET deleted = TRUE WHERE (`id` = '{}' AND `user_id` = '{}'); 
        """.format(id, user_id)
        
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


class Accounts(Resource):
    def db_init(self):
        db = pymysql.connect(host = 'localhost', user = 'root', password = 'zyhdEx-3timma-rotsiv', db = 'apitest')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    
    def get(self, user_id):
        db, cursor = self.db_init()
        sql = """
            SELECT * FROM apitest.account WHERE user_id = "{}" AND deleted IS NOT TRUE
        """.format(user_id)
        cursor.execute(sql)
        
        db.commit()
        accounts = cursor.fetchall()
        db.close()
        return jsonify(accounts)
    
    def post(self, user_id):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        account = {
            'balance' : arg['balance'],
            'account_number' : arg['account_number'],
            'user_id' : arg['user_id']
        }
        sql = """
            INSERT INTO `apitest`.`account` (`user_id`, `balance`, `account_number`) VALUES ('{}', '{}', '{}');
        """.format(account['user_id'], account['balance'], account['account_number'])
        
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
            