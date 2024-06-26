from flask import request
from flaskapp import create_app
from flask_cors import CORS
from swagger_ui import flask_api_doc
from markupsafe import escape
import json
from datetime import datetime, timedelta, MAXYEAR
from honbasho_calendar import HonbashoCalendar
from devtest_helper import DevtestHelper

application = create_app()
flask_api_doc(application, config_path='./api/doc/swagger.yaml', url_prefix='/api/doc', title='Python Web Service Demo | API doc')
CORS(application)

@application.route('/')
def hello_world():
    """
    Default endpoint. Prints a "Hello World" message.
    """

    return '<h1>Hello World!</h1>'

@application.route('/greeting/<name>')
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
    application.logger.debug(f"[get_workers] Request param work_days: {work_days}.\nRequest data: {request.json}")
    if len(work_days) > 0:
        if not work_days.issubset(days_of_week): # "work_days" includes an invalid value
            application.logger.error(f"[get_workers] Invalid value(s) in work_days!")
            return unsuccessful_response_json(400, "Invalid value for parameter work_days!")
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
        application.logger.error("[multiply_by_two] 'num' not present in request parameters.")
        return unsuccessful_response_json(400, "'num' not present in request parameters.")
    
    try:
        num = int(request.form['num'])
    except ValueError as e:
        application.logger.error(f'[multiply_by_two] Invalid value for parameter "num": {e}')
        return unsuccessful_response_json(400, "'num' must be an integer.")
    result = num * 2
    application.logger.debug(f"[multiply_by_two] result = {num} * 2 = {result}")
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
        return unsuccessful_response_json(400, "'date' is missing from request!")
    except ValueError:
        return unsuccessful_response_json(400, "'date' must be in YYYY-MM-DD format!")
    
    try:
        num_of_weeks = request.json["weeks"]
    except KeyError:
        return unsuccessful_response_json(400, "'weeks' is missing from request!")
    if not isinstance(num_of_weeks, int):
        return unsuccessful_response_json(400, "'weeks' must be an integer!")
    time_delta = timedelta(weeks=num_of_weeks)

    new_time = orig_date + time_delta
    application.logger.debug(f'[calculate_date] orig_date: {orig_date}, new_time: {new_time}\n(time_delta: {time_delta}))')
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

    DevtestHelper.simulate_delay("HONBASHO_SCHEDULE")

    if not "year" in request.args:
        return unsuccessful_response_json(400, "'year' must be provided in the request arguments!")
    
    try:
        year = int(request.args["year"])
    except ValueError as e:
        application.logger.error(f'[get_honbasho_schedule] Invalid value for parameter "year".\nMessage: {e}')
        return unsuccessful_response_json(400, "Request argument 'year' must be an integer!")
    if year < honbasho_schedule_minyear:
        application.logger.error(f'[get_honbasho_schedule] Invalid value for parameter "year": {year} < honbasho_schedule_minyear')
        return unsuccessful_response_json(400, f'Request argument \'year\' cannot be before {honbasho_schedule_minyear}!')
    if year > MAXYEAR:
        application.logger.error(f'[get_honbasho_schedule] Invalid value for parameter "year": {year} > MAXYEAR')
        return unsuccessful_response_json(400, "Request argument 'year' exceeded maximum allowed year value!")
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

def unsuccessful_response_json(status_code: int, message: str):
    '''
    Builds an unsuccessful response with a JSON response body.
    '''
    return {
        "code" : status_code,
        "message" : message
    }, status_code

if __name__ == "__main__":
    application.run(debug=True)