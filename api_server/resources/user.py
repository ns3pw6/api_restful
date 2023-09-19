from flask_restful import Resource
from flask import jsonify
import pymysql

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