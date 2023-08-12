from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[A-Z]).+$')
DB = "recipes"
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
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
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DB).query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO users (first_name,last_name,email,password)
            VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"""
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
        invalid_email_password = False
        query = "SELECT email FROM users;"
        email_dicts = connectToMySQL(DB).query_db(query)
        key_to_retrieve = 'email'
        emails = [d.get(key_to_retrieve) for d in email_dicts]
        if not user['first_name']:
            flash('First name is required', 'register')
            is_valid = False
        else:
            if not NAME_REGEX.match(user['first_name']):
                flash('First name must be only letters', 'register')
            if len(user['first_name']) < 2:
                flash('First name must be at least 2 characters', 'register')
        if not user['last_name']:
            flash('Last name is required', 'register')
            is_valid = False
        else:
            if not NAME_REGEX.match(user['last_name']):
                flash('Last name must be only letters', 'register')
            if len(user['last_name']) < 2:
                flash('Last name must be at least 2 characters', 'register')
        if not user['email']:
            invalid_email_password = True
            is_valid = False
        else:
            if not EMAIL_REGEX.match(user['email']):
                invalid_email_password = True
                is_valid = False
            elif user['email'] in emails:
                invalid_email_password = True
                is_valid = False
        if not user['password']:
            invalid_email_password = True
            is_valid = False
        else:
            if len(user['password']) < 8:
                invalid_email_password = True
                is_valid = False
            if not PASSWORD_REGEX.match(user['password']):
                invalid_email_password = True
                is_valid = False
            elif user['password'] != user['confirm_password']:
                flash('Passwords do not match', 'register')
                is_valid = False
        if invalid_email_password:
            flash('Invalid email or password', 'register')
        return is_valid
    
    @staticmethod
    def validate_login(login):
        is_valid = True
        query = "SELECT password FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DB).query_db(query,login)
        if len(result) > 0:
            password = result[0]['password']
        else:
            password = None
        print('db password: ',password, 'input password: ', login['password'])
        if not login['email']:
            flash('Email is required', 'login')
            is_valid = False
        if not login['password']:
            flash('Password is required', 'login')
            is_valid = False
        if login['email'] and login['password'] and password:
            if not (bcrypt.check_password_hash(password, login['password'])):
                flash('Invalid email or password', 'login')
                is_valid = False
        else:
            flash('Invalid email or password', 'login')
            is_valid = False
        return is_valid