from flask_app import app
from flask import render_template,redirect,request, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if check_session():
        return redirect('/dashboard')
    users = User.get_all()
    return render_template('index.html', users = users)

@app.route('/register_user', methods = ['POST'])
def register_user():
    data = {
        'first_name': request.form['first-name'],
        'last_name': request.form['last-name'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirm_password': request.form['confirm-password'],
    }
    if not User.validate_user(data):
        return redirect('/')

    data['password'] = bcrypt.generate_password_hash(request.form['password'])
    del data['confirm_password']
    result = User.save(data)
    set_session(result, data['first_name'], True)
    print(result)
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if check_session():
        data = {
            'id': session['user_id']
        }
        user = User.get_user_by_id(data)
        recipes = Recipe.get_all()
        recipe_dicts = []
        for recipe in recipes:
            data = {'id': recipe.user_id}
            recipe_user = User.get_user_by_id(data)
            recipe_dicts.insert(0,{'recipe': recipe, 'user': recipe_user})
        return render_template('dashboard.html', user = user, recipe_dicts = recipe_dicts)
    return redirect('/')

@app.route('/log_out')
def log_out():
    session.clear()
    return redirect('/')

@app.route('/login_user', methods = ['POST'])
def login_user():
    data = {
        'email': request.form['email'],
        'password': request.form['password'],
    }
    if not User.validate_login(data):
        return redirect('/')
    user = User.get_user_by_email({'email': data['email']})
    set_session(user.id, user.first_name, True)
    return redirect('/dashboard')

def check_session():
    if 'logged_in' in session and 'user_id' in session and 'first_name' in session:
        return True
    return False

def set_session(id, first_name, logged_in):
    session['user_id'] = id
    session['first_name'] = first_name
    session['logged_in'] = logged_in