# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the ninja table from our database
class Ninja:
    DB = 'dojos_and_ninjas'
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.dojo_id = data['dojo_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM ninjas;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.DB).query_db(query)
        # Create an empty list to append our instances of ninjas
        ninjas = []
        # Iterate over the db results and create instances of ninjas with cls.
        for ninja in results:
            ninjas.append( cls(ninja) )
        return ninjas

    @classmethod
    def save(cls, data):
        query = """INSERT INTO ninjas (first_name, last_name, age, dojo_id)
            VALUES (%(first_name)s, %(last_name)s, %(age)s, %(dojo_id)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        print(result)
        return result
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM ninjas WHERE id=%(id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM ninjas WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    @classmethod
    def update(cls, data):
        query = """UPDATE ninjas SET first_name = %(first_name)s, last_name = %(last_name)s,
        age = %(age)s, dojo_id = %(dojo_id)s, updated_at = NOW()
        WHERE id = %(id)s;"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result