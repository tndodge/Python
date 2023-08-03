from flask_app import app
from flask import render_template,redirect,request, session
from flask_app.models.post import Post
from flask_app.controllers.users import check_session, log_out

@app.route('/publish_post', methods=['POST'])
def publish_post():
    if not check_session():
        return log_out()
    data = {
        'content': request.form['content'],
        'user_id': session['user_id']
    }
    if not Post.validate_post(data):
        return redirect('success')
    post = Post.save(data)
    return redirect('/success')

@app.route('/delete_post', methods=['GET'])
def delete_post():
    print('POST ID: ',request.args.get('post-id'))
    post_id = request.args.get('post-id')
    data = {'id': post_id}
    if not Post.validate_delete(data):
        return redirect('/success')
    result = Post.delete(data)
    return redirect('/success')