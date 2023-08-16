from flask_app import app
from flask import render_template,redirect,request, session
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if check_session():
        return redirect('/success')
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
    set_session(result, True)
    print(result)
    return redirect('/success')

@app.route('/success')
def success():
    if check_session():
        data = {
            'id': session['user_id']
        }
        posts = Post.get_all()
        posts.reverse()
        return render_template('wall_page.html', posts = posts)
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
    set_session(user.id, True)
    return redirect('/success')

def check_session():
    if 'logged_in' in session and 'user_id' in session:
        return True
    return False

def set_session(id, logged_in):
    session['user_id'] = id
    session['logged_in'] = logged_in