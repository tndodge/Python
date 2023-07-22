from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.dojo import Dojo

@app.route('/')
def index():
    dojos = Dojo.get_all()
    return render_template('index.html', dojos = dojos)

@app.route('/process_dojo', methods = ['POST'])
def process_dojos():
    data = {
        'name': request.form['name']
    }
    Dojo.save(data)
    return redirect('/')

@app.route('/dojo_show/<int:id>')
def dojo_show(id):
    data = {'id': id}
    dojo = Dojo.get_dojo_with_users(data)
    print(dojo.ninjas)
    return render_template('dojo_show.html', dojo = dojo)