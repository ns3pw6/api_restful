from server import db

#
# Define a class representing the UserModel which maps to the 'users' table in the database
#
class UserModel(db.Model):
    __tablename__ = 'users'
    
    #
    # Define the columns of the 'users' table
    #
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(45))
    gender = db.Column(db.Integer)
    birth = db.Column(db.DateTime)
    note = db.Column(db.Text)
    deleted = db.Column(db.Boolean)
    
    #
    # Constructor to initialize a user object
    #
    def __init__(self, name, gender, birth, note, deleted = None):
        self.name = name
        self.gender = gender
        self.birth = birth
        self.note = note
        self.deleted = deleted
    
    #
    # Method to serialize a user object into a dictionary
    #
    def serialize(self):
        return{
            "name" : self.name,
            "gender" : self.gender,
            "birth" : self.birth,
            "note" : self.note,
            "deleted" : self.deleted
        }