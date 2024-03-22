from flask import request
from flaskapp import create_app
from swagger_ui import flask_api_doc
from markupsafe import escape
import json
from enum import Enum


application = create_app()
flask_api_doc(application, config_path='./api/doc/swagger.yaml', url_prefix='/api/doc', title='python-webservice-demo | API doc')

@application.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'

@application.route('/<name>')
def personal_greeting(name):
    return f"Hello, {escape(name)}!";

days_of_week = { "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY" }

@application.route('/getWorkers', methods=["POST"])
def get_workers():
    with open("data/worker_list.json", encoding="utf8") as data_file:
        worker_list = json.load(data_file)

    work_days = set([] if "work_days" not in request.json else request.json["work_days"])
    application.logger.debug(f"Request param work_days: {work_days}")
    application.logger.debug(request.json)
    if len(work_days) > 0:
        if not work_days.issubset(days_of_week): # "work_days" includes an invalid value
            application.logger.error(f"Invalid value(s) in work_days!\nRequest: {request.json}")
            return "Invalid value for parameter work_days!", 400
        return {
            "workers" : [
                worker for worker in worker_list["workers"] if work_days.issubset(worker["work_days"])
            ]
        }
    return worker_list

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
