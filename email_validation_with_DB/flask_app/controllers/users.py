from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.models.user import User

@app.route('/')
def index():
    session.clear()
    users = User.get_all()
    return render_template('index.html', users = users)

@app.route('/create_user')
def create_user():
    return render_template('create_user.html')

@app.route('/process_create_user', methods = ['POST'])
def process_create_user():
    session['form_data'] = request.form
    if not User.validate_user(request.form):
        return redirect('/create_user')
    session.clear()
    result = User.save(request.form)
    return redirect(f'/read_one/{result}')

@app.route('/edit/<int:id>')
def edit(id):
    data = {'id':id}
    user = User.get_one(data)
    return render_template('edit.html', user = user)

@app.route('/process_edit', methods = ['POST'])
def process_edit():
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'id': request.form['id'],
    }
    result = User.update(data)
    return redirect(f"/read_one/{data['id']}")

@app.route('/read_one/<int:id>')
def read_one(id):
    data = {'id':id}
    user = User.get_one(data)
    return render_template('/read_one.html', user = user)

@app.route('/delete/<int:id>')
def delete(id):
    data = {'id':id}
    user = User.delete(data)
    return redirect('/')