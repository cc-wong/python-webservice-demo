from flask import request
from flaskapp import create_app
from swagger_ui import flask_api_doc
from markupsafe import escape


application = create_app()
flask_api_doc(application, config_path='./api/doc/swagger.yaml', url_prefix='/api/doc', title='python-webservice-demo | API doc')

@application.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'

@application.route('/<name>')
def personal_greeting(name):
    return f"Hello, {escape(name)}!";

@application.route('/getWorkers')
def get_workers():
    return {
        "workers" : [
            {
                "name" : "Chan Tai Man",
                "sex" : "M",
                "is_reg_member" : True,
                "age" : 56,
                "work_days" : [ "Monday", "Tuesday", "Wednesday", "Thursday", "Friday" ]
            },
            {
                "name" : "Ma Siu Ling",
                "sex" : "F",
                "is_reg_member" : False,
                "age" : 22,
                "work_days" : [ "Monday", "Wednesday", "Friday" ]
            }
        ]
    }

@application.route('/timestwo', methods=["POST"])
def multiply_by_two():
    if 'num' not in request.form:
        application.logger.error("'num' not present in request parameters.\n request.form: %s", request.form)
        return "'num' not present in request parameters.", 400
    
    try:
        num = int(request.form['num'])
    except ValueError as e:
        application.logger.exception("Value error thrown.")
        return "'num' must be an integer.", 400
    result = num * 2
    application.logger.info(f"result = {num} * 2 = {result}")
    return {
        "num" : num,
        "result" : result
    }

if __name__ == "__main__":
    application.run(debug=True)
