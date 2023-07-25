from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'
@app.route('/')
def base_route():
    if 'visits' in session:
        session['visits'] += 1
    else:
        session['visits'] = 1
    
    if not 'count' in session:
        session['count'] = 0

    return render_template("index.html")

@app.route('/destroy_session')
def destroy_session():
    session.clear()
    return redirect('/')

@app.route('/add_two')
def add_two():
    if 'count' in session:
        session['count'] += 2
    else:
        session['count'] = 2

    return redirect('/')

@app.route('/increment', methods=['POST'])
def increment():
    inc = int(request.form['increment'])
    if inc < 0:
        inc = 0
    if 'count' in session:
        session['count'] += inc
    else:
        session['count'] = inc
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True, host="localhost", port=8000)