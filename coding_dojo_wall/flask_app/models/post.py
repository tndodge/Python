from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.user import User
from flask import flash, session
DB = "coding_dojo_wall"
class Post:
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.display_date = ''

    @classmethod
    def save(cls, data):
        query = """INSERT INTO posts (content,user_id)
            VALUES (%(content)s,%(user_id)s);"""
        result = connectToMySQL(DB).query_db(query,data)
        return result
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM posts;"
        results = connectToMySQL(DB).query_db(query)
        posts = []
        for post in results:
            posts.append( cls(post) )
        return posts
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM posts WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query,data)
        if len(result) == 0:
            return False
        return cls(result[0])
    
    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM posts WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
    @staticmethod
    def validate_post(post):
        is_valid = True
        if not post['content']:
            flash('* Post content must not be blank.', 'post')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_delete(delete):
        is_valid = True
        data = {'id': delete['id']}
        post = Post.get_by_id(data)
        if post:
            data = {'id': post.user_id}
            user = User.get_user_by_id(data)
            if user.id != session['user_id']:
                flash('* You are not allowed to delete other users\' posts', 'delete')
                is_valid = False
        else:
            flash('* The post you tried to delete does not exist', 'delete')
            is_valid = False
        return is_valid