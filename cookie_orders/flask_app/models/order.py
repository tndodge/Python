# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# model the class after the order table from our database
class Order:
    DB = 'cookie_orders'
    def __init__( self , data ):
        self.id = data['id']
        self.customer_name = data['customer_name']
        self.cookie_type = data['cookie_type']
        self.number_of_boxes = data['number_of_boxes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM orders;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.DB).query_db(query)
        # Create an empty list to append our instances of orders
        orders = []
        # Iterate over the db results and create instances of orders with cls.
        for order in results:
            orders.append( cls(order) )
        return orders

    @classmethod
    def save(cls, data):
        query = """INSERT INTO orders (customer_name, cookie_type, number_of_boxes)
            VALUES (%(customer_name)s,%(cookie_type)s,%(number_of_boxes)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    @classmethod
    def get_one(cls, data):
        query = """SELECT * FROM orders WHERE id = %(id)s"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result[0]
    
    @classmethod
    def update(cls, data):
        query = """UPDATE orders SET customer_name=%(customer_name)s, cookie_type=%(cookie_type)s,
        number_of_boxes=%(number_of_boxes)s, updated_at=NOW() WHERE id=%(id)s;"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    @staticmethod
    def validate_order(order):
        is_valid = True
        if not order['customer-name'] or not order['cookie-type'] or not order['number-of-boxes']:
            flash('All fields are required')
            is_valid = False
        else:
            if len(order['customer-name']) < 2:
                flash('Customer name must be at least 2 characters')
                is_valid = False
            if len(order['cookie-type']) < 2:
                flash('Cookie type must be at least 2 characters')
                is_valid = False
            if int(order['number-of-boxes']) < 0:
                flash('Number of boxes must be a positive number')
                is_valid = False

        return is_valid