from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.dojo import Dojo
from flask_app.models.ninja import Ninja

@app.route('/new_ninja')
def new_ninja():
    dojos = Dojo.get_all()
    return render_template('new_ninja.html', dojos = dojos)

@app.route('/process_ninja', methods = ['POST'])
def process_ninja():
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'age': request.form.get('age'),
        'dojo_id': request.form.get('dojo'),
    }
    Ninja.save(data)
    return redirect(f"/dojo_show/{data['dojo_id']}")

@app.route('/delete_ninja/<int:id>')
def delete_ninja(id):
    data = {'id': id}
    dojo_id = Ninja.get_one(data).dojo_id
    Ninja.delete(data)
    return redirect(f"/dojo_show/{dojo_id}")

@app.route('/edit_ninja/<int:id>')
def edit_ninja(id):
    data = {'id': id}
    ninja = Ninja.get_one(data)
    dojos = Dojo.get_all()
    return render_template('edit_ninja.html', ninja = ninja, dojos = dojos)

@app.route('/update_ninja/<int:id>', methods = ['POST'])
def update_ninja(id):
    data = {
        'id': id,
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'age': request.form.get('age'),
        'dojo_id': request.form.get('dojo'),
    }
    Ninja.update(data)
    return redirect(f"/dojo_show/{data['dojo_id']}")