from flask_app import app
from flask_app.controllers import order

if __name__=="__main__":   
    app.run(debug=True, host="localhost", port=8000)