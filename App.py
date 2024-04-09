from flask import request
from flaskapp import create_app
from flask_cors import CORS
from swagger_ui import flask_api_doc
from markupsafe import escape
import json
from datetime import datetime, timedelta, MAXYEAR
from honbasho_calendar import HonbashoCalendar
import time


application = create_app()
flask_api_doc(application, config_path='./api/doc/swagger.yaml', url_prefix='/api/doc', title='Python Web Service Demo | API doc')
CORS(application)

@application.route('/')
def hello_world():
    """
    Default endpoint. Prints a "Hello World" message.
    """

    return '<h1>Hello World!</h1>'

@application.route('/<name>')
def personal_greeting(name):
    """
    Prints a personalized greeting.

    :param name: The name to use for the greeting.
    """

    return f"Hello, {escape(name)}!";

@application.route('/healthcheck')
def healthcheck():
    """
    Healthcheck endpoint.
    """
    application.logger.debug("Healthcheck triggered.")
    return "OK";

days_of_week = { "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY" }

@application.route('/getWorkers', methods=["POST"])
def get_workers():
    """
    Retrieves a list of workers from a JSON file.

    If a set of work days (as day of week) is provided in the request data,
    only workers whose work days include all the specified days of week will be returned.
    """

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
    """
    Multiplies a given integer by 2.
    """

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

json_date_format = "%Y-%m-%d"

@application.route('/calculateDate', methods=["POST"])
def calculate_date():
    """
    Calculates the date a specified number of weeks
    before/after a given date.
    """

    try:
        orig_date = datetime.strptime(request.json["date"], json_date_format)
    except KeyError:
        return "'date' is missing from request!", 400
    except ValueError:
        return "'date' must be in YYYY-MM-DD format!", 400
    
    try:
        num_of_weeks = request.json["weeks"]
    except KeyError:
        return "'weeks' is missing from request!", 400
    if not isinstance(num_of_weeks, int):
        return "'weeks' must be an integer!", 400
    time_delta = timedelta(weeks=num_of_weeks)

    new_time = orig_date + time_delta
    return {
        "result" : new_time.strftime(json_date_format)
    }

honbasho_schedule_minyear = 2012
@application.route('/getSumoHonbashoSchedule', methods=["GET"])
def get_honbasho_schedule():
    """
    Calculates and returns the Grand Sumo Tournament schedule for a given year.

    Requires an argument "year", which is an year number (integer).
    The year must be between 2012 and 2100, inclusive.
    """

    time.sleep(70)

    if not "year" in request.args:
        return "'year' must be provided in the request arguments!", 400
    
    try:
        year = int(request.args["year"])
    except ValueError:
        return "Request argument 'year' must be an integer!", 400
    if year < honbasho_schedule_minyear:
        return f'Request argument \'year\' cannot be before {honbasho_schedule_minyear}!', 400
    if year > MAXYEAR:
        return "Request argument 'year' exceeded maximum allowed year value!", 400
    schedule = HonbashoCalendar.calculate_schedule(year)

    result = []
    for basho in schedule:
        label = basho["basho"]
        result.append({
            "basho" : label.get_name(),
            "month" : label.get_month(),
            "month_name": label.get_month_name(),
            "dates" : [ d .strftime(json_date_format) for d in basho["dates"] ]
        })
    return {
        "result" : result
    }


if __name__ == "__main__":
    application.run(debug=True)