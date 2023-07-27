from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DB = "users_schema"
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DB).query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO users (first_name,last_name,email)
            VALUES (%(first_name)s,%(last_name)s,%(email)s);"""
        result = connectToMySQL(DB).query_db(query,data)
        return result
    
    @classmethod
    def update(cls,data):
        query = """UPDATE users 
                SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s,updated_at=NOW() 
                WHERE id = %(id)s;"""
        return connectToMySQL(DB).query_db(query,data)
    
    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT email FROM users;"
        email_dicts = connectToMySQL(DB).query_db(query)
        key_to_retrieve = 'email'
        emails = [d.get(key_to_retrieve) for d in email_dicts]
        if not user['first_name']:
            flash('First name is required')
            is_valid = False
        if not user['last_name']:
            flash('Last name is required')
            is_valid = False
        if not user['email']:
            flash('Email is required')
            is_valid = False
        else:
            if not EMAIL_REGEX.match(user['email']):
                flash('Please enter a valid email adress')
                is_valid = False
            elif user['email'] in emails:
                flash('Please enter a unique email adress')
                is_valid = False
        return is_valid