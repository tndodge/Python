from flask import Flask, render_template, request, redirect, session
import random
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'
@app.route('/')
def root_route():

    if not 'number' in session:
        session['number'] = random.randint(1, 100)

    if not 'display_text' in session:
        session['display_text'] = ''

    return render_template("index.html")

@app.route('/guess', methods = ['POST'])
def guess():

    if not 'number' in session:
        session['number'] = random.randint(1, 100)

    if int(request.form['guess']) > session['number']:
        session['display_text'] = 'Too high'
    elif int(request.form['guess']) < session['number']:
        session['display_text'] = 'Too low'
    else:
        session['display_text'] = 'Correct!'

    return redirect('/')

@app.route('/clear_session')
def clear_session():

    session.clear()

    return redirect('/')

if __name__=="__main__":
    app.run(debug=True, host="localhost", port=8000)