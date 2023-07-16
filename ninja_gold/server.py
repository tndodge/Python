from flask import Flask, render_template, redirect, request, session
import random
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'Keep it secret. Keep it safe.'

@app.route('/')
def index():
    if not 'gold' in session:
        session['gold'] = 0
    if not 'activity_logs' in session:
        session['activity_logs'] = []
    return render_template('index.html')

@app.route('/process_money', methods = ['POST'])
def process_money():
    if not 'gold' in session:
        session['gold'] = 0
    if not 'activity_logs' in session:
        session['activity_logs'] = []
    
    gold_earned = 0
    property = request.form['property']
    if property == 'farm':
        gold_earned = random.randint(10, 20)
    elif property == 'cave':
        gold_earned = random.randint(5, 10)
    elif property == 'house':
        gold_earned = random.randint(2, 5)
    elif property == 'casino':
        gold_earned = random.randint(-50, 50)
    session['gold'] += gold_earned
    
    date_time = datetime.now()
    hour = date_time.hour
    time_modifier = 'am'
    if hour > 12:
        hour -= 12
        time_modifier = 'pm'
    if hour < 1:
        hour = 1
    minute = f'{date_time.minute}'
    if date_time.minute < 10:
        minute = f'0{date_time.minute}'
    date_time_string = f'{date_time.month}/{date_time.day}/{date_time.year} {hour}:{minute}{time_modifier}'
    style_string = 'color:green;'
    if property == 'casino':
        if gold_earned > 0:
            message = f'Entered a casino and won {gold_earned} golds!'
        elif gold_earned < 0:
            message = f'Entered a casino and lost {gold_earned} golds... Ouch..'
            style_string = 'color:red;'
        else:
            message = f'Entered a casino and broke even'
            style_string = 'color:darkgoldenrod;'
    else:
        message = f'Earned {gold_earned} golds from {property}'
    
    session['activity_logs'].append(f'<p style = {style_string}>{message} {date_time_string}</p>')
    return redirect('/')

@app.route('/destroy_session')
def destroy_session():
    session.clear()
    return redirect('/')

if __name__=="__main__":   
    app.run(debug=True, host="localhost", port=8000)