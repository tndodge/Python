from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
import re
DATE_REGEX = re.compile(r'^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$')
DB = "recipes"
class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under_thirty = data['under_thirty']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(DB).query_db(query)
        recipes = []
        for recipe in results:
            recipes.append( cls(recipe) )
        return recipes
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        results = connectToMySQL(DB).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO recipes (user_id,name,description,instructions,
        date_cooked,under_thirty)
            VALUES (%(user_id)s,%(name)s,%(description)s,%(instructions)s,
            %(date_cooked)s,%(under_thirty)s);"""
        result = connectToMySQL(DB).query_db(query,data)
        return result
    
    @classmethod
    def update(cls,data):
        query = """UPDATE recipes 
                SET name=%(name)s,description=%(description)s,instructions=%(instructions)s,
                date_cooked=%(date_cooked)s, under_thirty=%(under_thirty)s, updated_at=NOW() 
                WHERE id = %(id)s;"""
        return connectToMySQL(DB).query_db(query,data)
    
    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        all_fields_required = False
        if not recipe['name']:
            is_valid = False
            all_fields_required = True
        elif len(recipe['name']) < 3:
            is_valid = False
            flash('Name must be at least 3 characters', 'recipe')

        if not recipe['description']:
            is_valid = False
            all_fields_required = True
        elif len(recipe['description']) < 3:
            is_valid = False
            flash('Description must be at least 3 characters', 'recipe')

        if not recipe['instructions']:
            is_valid = False
            all_fields_required = True
        elif len(recipe['instructions']) < 3:
            is_valid = False
            flash('Instructions must be at least 3 characters', 'recipe')

        if not recipe['date_cooked']:
            is_valid = False
            all_fields_required = True
        elif not DATE_REGEX.match(recipe['date_cooked']):
            is_valid = False
            flash('Please enter a valid date', 'recipe')

        if all_fields_required:
            flash('All fields are required', 'recipe')

        return is_valid
    
    @staticmethod
    def validate_action(recipe):
        is_valid = True
        if recipe['user_id'] != session['user_id']:
            is_valid = False
            flash('You cannot edit or delete other users\' recipes', 'action')
        return is_valid