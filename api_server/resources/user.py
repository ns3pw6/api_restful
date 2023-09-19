from flask_restful import Resource, reqparse
from flask import jsonify
import pymysql
import traceback

# 
# Preventing SQL injection in Python, only accept these fields
# 
parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

class Users(Resource):    
    def db_init(self):
        db = pymysql.connect(host = 'localhost', user = 'root', password = 'zyhdEx-3timma-rotsiv', db = 'apitest')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    
    def get(self):
        db, cursor = self.db_init()
        sql = 'SELECT * FROM apitest.users'
        cursor.execute(sql)
        db.commit()
        users = cursor.fetchall()
        db.close()
        return jsonify({'data' : users})
    
    def post(self):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            'name' : arg['name'],
            'gender' : arg['gender'],
            'birth' : arg['birth'],
            'note' : arg['note']
        }
        sql = """
            INSERT INTO `apitest`.`users` (`name`, `gender`, `birth`, `note`) VALUES ('{}', '{}', '{}', '{}');
        """.format(user['name'], user['gender'], user['birth'], user['note'])
        
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