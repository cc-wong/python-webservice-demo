from flask import Flask
from flaskapp import create_app
from swagger_ui import flask_api_doc
from markupsafe import escape
import datetime

application = create_app()
flask_api_doc(application, config_path='./api/doc/swagger.yaml', url_prefix='/api/doc', title='python-webservice-demo | API doc')

@application.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'

@application.route('/<name>')
def personal_greeting(name):
    return f"Hello, {escape(name)}!";

@application.route('/json')
def get_json_data():
    return {
        "name" : "Chan Tai Man",
        "is_alive" : True,
        "age" : 56,
        "work_days" : [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday"
        ]
    }

if __name__ == "__main__":
    application.run(debug=True)
