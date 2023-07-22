# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.ninja import Ninja
# model the class after the dojo table from our database
class Dojo:
    DB = 'dojos_and_ninjas'
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ninjas = []
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.DB).query_db(query)
        # Create an empty list to append our instances of dojos
        dojos = []
        # Iterate over the db results and create instances of dojos with cls.
        for dojo in results:
            dojos.append( cls(dojo) )
        return dojos

    @classmethod
    def save(cls, data):
        query = """INSERT INTO dojos (name)
            VALUES (%(name)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM dojos WHERE id=%(id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def get_dojo_with_users(cls, data):
        query = "SELECT * FROM dojos LEFT JOIN ninjas ON dojos.id = ninjas.dojo_id WHERE dojos.id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        dojo = cls(result[0])
        if result[0]['ninjas.id']:
            for dict in result:
                data = {
                    'id': dict['ninjas.id'],
                }
                ninja = Ninja.get_one(data)
                dojo.ninjas.append(ninja)
        
        return dojo