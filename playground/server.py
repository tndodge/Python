from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/play')
def play_route():
    return render_template('index.html', times = 3, color = 'blue')

@app.route('/play/<int:times>')
def play_route2(times):
    return render_template('index.html', times = times, color = 'blue')

@app.route('/play/<int:times>/<string:color>')
def play_route3(times, color):
    return render_template('index.html', times = times, color = color)

if __name__=="__main__":
    app.run(debug=True, host="localhost", port=8000)