from flask_restful import Resource
import pymysql

class Users(Resource):    
    def db_init(self):
        db = pymysql.connect('localhost', 'root', 'zyhdEx-3timma-rotsiv', 'apitest')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor