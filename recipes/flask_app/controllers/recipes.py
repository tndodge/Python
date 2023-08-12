from flask_app import app
from flask import render_template,redirect,request, session
from flask_app.controllers.users import check_session
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    if check_session():
        data = {'id': recipe_id}
        recipe = Recipe.get_by_id(data)
        data = {'id': recipe.user_id}
        user = User.get_user_by_id(data)
        user_name = user.first_name
        return render_template('view_recipe.html', recipe = recipe, user_name = user_name)
    return redirect('/')

@app.route('/create_recipe')
def create_recipe():
    if check_session():
        return render_template('create_recipe.html')
    return redirect('/')

@app.route('/process_recipe', methods = ['POST'])
def process_recipe():
    if check_session():
        data = {
            'user_id': session['user_id'],
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'date_cooked': request.form.get('date-cooked'),
            'under_thirty': (request.form.get('under-thirty') == 'yes'),
        }
        if Recipe.validate_recipe(data):
            result = Recipe.save(data)
            return redirect('/')
        return redirect('/create_recipe')
    return redirect('/')

@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    if check_session():
        data = {'id': recipe_id}
        recipe = Recipe.get_by_id(data)
        session['recipe_id'] = recipe_id
        data = {'user_id': recipe.user_id}
        if Recipe.validate_action(data):
            return render_template('edit_recipe.html', recipe = recipe)
    return redirect('/')

@app.route('/update_recipe', methods = ['POST'])
def update_recipe():
    if check_session():
        data = {
            'id': session['recipe_id'],
            'user_id': session['user_id'],
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'date_cooked': request.form.get('date-cooked'),
            'under_thirty': (request.form.get('under-thirty') == 'yes'),
        }
        if Recipe.validate_recipe(data):
            result = Recipe.update(data)
            return redirect('/')
        return redirect(f'/edit_recipe/{session["recipe_id"]}')
    return redirect('/')

@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    if check_session():
        data = {'id': recipe_id}
        recipe = Recipe.get_by_id(data)
        data = {'user_id': recipe.user_id}
        if Recipe.validate_action(data):
            data = {'id': recipe_id}
            result = Recipe.delete(data)
    return redirect('/')