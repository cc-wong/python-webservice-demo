from flask import Flask
from markupsafe import escape
import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'

@app.route('/<name>')
def personal_greeting(name):
    return f"Hello, {escape(name)}!";

@app.route('/json')
def get_json_data():
    return {
        "name" : "Chan Tai Man",
        "date" : datetime.datetime.today()
    }

if __name__ == "__main__":
    app.run(debug=True)
