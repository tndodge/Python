from flask_app import app
from flask import render_template,redirect,request
from flask_app.models.order import Order

@app.route('/')
def index():
    return redirect('/orders')

@app.route('/orders')
def orders():
    orders = Order.get_all()
    return render_template('orders.html', orders = orders)

@app.route('/new_order')
def new_order():
    return render_template('new_order.html')

@app.route('/edit_order/<int:id>')
def edit_order(id):
    data = {
        'id': id
    }
    order = Order.get_one(data)
    print(order)
    return render_template('edit_order.html', order = order)

@app.route('/update_order', methods = ['POST'])
def update_order():
    if not Order.validate_order(request.form):
        return redirect(f"/edit_order/{request.form.get('id')}")
    data = {
        'customer_name': request.form['customer-name'],
        'cookie_type': request.form['cookie-type'],
        'number_of_boxes': request.form['number-of-boxes'],
        'id': request.form.get('id'),
    }
    Order.update(data)
    return redirect('/orders')

@app.route('/process_order', methods = ['POST'])
def process_order():
    if not Order.validate_order(request.form):
        return redirect('/new_order')
    data = {
        'customer_name': request.form['customer-name'],
        'cookie_type': request.form['cookie-type'],
        'number_of_boxes': request.form['number-of-boxes'],
    }
    Order.save(data)
    return redirect('/orders')