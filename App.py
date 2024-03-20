from flask import Flask
from swagger_ui import flask_api_doc
from markupsafe import escape
import datetime

app = Flask(__name__)
flask_api_doc(app, config_path='./api/doc/swagger.yaml', url_prefix='/api/doc', title='python-webservice-demo | API doc')

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
