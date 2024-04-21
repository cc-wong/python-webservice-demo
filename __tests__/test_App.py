import unittest
from unittest.mock import patch, mock_open
from App import application
from honbasho_calendar import HonbashoCalendar
import json
from datetime import date
import calendar


class TestWebApp(unittest.TestCase):
    """
    Test cases on the webservice endpoints in `App.py`.
    """

    def setUp(self):
        """
        Setup before test run.
        """

        self.appctx = application.app_context()
        self.appctx.push()
        self.client = application.test_client()
    
    def tearDown(self):
        """
        Tear down after test run.
        """

        self.appctx.pop()
        self.appctx = None
    
    def test_hello_world(self):
        """
        Test case on default endpoint (`/`).
        """

        response = self.client.get('/')
        assert response.status_code == 200

        message = response.get_data(as_text=True)
        assert message == "<h1>Hello World!</h1>"

    def test_personal_greeting(self):
        """
        Test case on endpoint `/<name>`.
        """

        name = "Lulu"

        response = self.client.get(f'/{name}')
        assert response.status_code == 200

        message = response.get_data(as_text=True)
        assert message == f"Hello, {name}!"
    
    def test_healthcheck_getrequest(self):
        """
        Test case on a GET request to endpoint `/healthcheck`.
        """
        response = self.client.get('/healthcheck')
        assert response.status_code == 200
        message = response.get_data(as_text=True)
        assert message == "OK"
    
    def test_healthcheck_headrequest(self):
        """
        Test case on a HEAD request to endpoint `/healthcheck`.
        """
        response = self.client.head('/healthcheck')
        assert response.status_code == 200

    # Mock JSON data in test cases on `/getWorkers`.
    workers = {
        "workers" : [
            {
                "name" : "Chan Tai Man",
                "sex" : "M",
                "is_reg_member" : True,
                "age" : 56,
                "work_days" : [ "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY" ]
            },
            {
                "name" : "Three Cheung",
                "sex" : "M",
                "is_reg_member" : False,
                "age" : 31,
                "work_days" : [ "SATURDAY", "SUNDAY" ]
            },
            {
                "name" : "Ma Siu Ling",
                "sex" : "F",
                "is_reg_member" : False,
                "age" : 22,
                "work_days" : [ "MONDAY", "WEDNESDAY", "FRIDAY" ]
            }
        ]
    }
    workers_json_text = json.dumps(workers)

    def test_get_workers_paramset_empty(self):
        """
        Test case on endpoint `/getWorkers` where the request parameter set is empty.
        """
        calendar.MONDAY

        self.run_test_get_workers({}, 200, TestWebApp.workers)

    def test_get_workers_workdays_param_empty(self):
        """
        Test case on endpoint `/getWorkers`
        where the `work_days` request parameter is an empty list.
        """

        self.run_test_get_workers({ "work_days" : [] }, 200, TestWebApp.workers)

    def test_get_workers_workdays_param_nonempty(self):
        """
        Test case on endpoint `/getWorkers`
        where the `work_days` request parameter is non-empty.
        """

        self.run_test_get_workers({ "work_days" : [ "MONDAY", "WEDNESDAY" ] }, 200, {
            "workers" : [
                TestWebApp.workers["workers"][0],
                TestWebApp.workers["workers"][2]
            ]
        })

    def test_get_workers_workdays_param_invalid(self):
        """
        Test case on endpoint `/getWorkers`
        where the `work_days` request parameter contains invalid values.
        """

        self.run_test_get_workers({ "work_days" : [ "MONDAY", "INVALID" ] },
                                  400, 
                                  self.get_expected_response_body(400,
                                                                  error_message="Invalid value for parameter work_days!"))

    @patch("builtins.open", new_callable=mock_open, read_data=workers_json_text)
    def run_test_get_workers(self,
                             param_work_days,
                             expected_status_code,
                             expected_data,
                             mock_file):
        """
        Runs a test case on endpoint `/getWorkers`.
        """
        filename = "data/worker_list.json"
        response = self.client.post('/getWorkers', json=param_work_days)
        self.verify_endpoint_with_json_response_data(response, expected_status_code, expected_data)

        assert open(filename, "utf8").read() == TestWebApp.workers_json_text
        mock_file.assert_called_with(filename, "utf8")

    def test_multiply_by_two_normal(self):
        """
        Happy path test case on endpoint `/timestwo`.
        """
        response = self.client.post('/timestwo', data={"num" : 3})
        assert response.status_code == 200
        data = json.loads(response.get_data())
        self.assertEqual({
            "num" : 3,
            "result" : 6
        }, data)

    def test_multiply_by_two_noninteger_param(self):
        """
        Test case on endpoint: `/timestwo` where request parameter `num` is not an integer.
        """
        response = self.client.post('/timestwo', data={"num" : "not-a-number"})
        assert response.status_code == 400
        data = json.loads(response.get_data())
        self.assertEqual({
                "code" : 400,
                "message" : "'num' must be an integer."
            }, data)

    def test_multiply_by_two_no_request_param(self):
        """
        Test case on endpoint `/timestwo` where request parameter `num` does not exist.
        """
        response = self.client.post('/timestwo', data={})
        assert response.status_code == 400
        data = json.loads(response.get_data())
        self.assertEqual({
                "code" : 400,
                "message" : "'num' not present in request parameters."
            }, data)

    def test_calculate_date_future(self):
        """
        Test case on endpoint `/calculateDate` for calculating future date.
        """
        request_data = {
            "date" : "2024-05-27",
            "weeks" : 10
        }
        self.run_test_calculate_date(request_data, 200, expected_data={
            "result" : "2024-08-05"
        })
    
    def test_calculate_date_past(self):
        """
        Test case on endpoint `/calculateDate` for calculating past date.
        """
        request_data = {
            "date" : "2024-03-24",
            "weeks" : -2
        }
        self.run_test_calculate_date(request_data, 200, expected_data={
            "result" : "2024-03-10"
        })
    
    def test_calculate_date_weeks_is_zero(self):
        """
        Tests endpoint `/calculateDate` where `weeks` is equal to 0 (zero).
        """

        request_data = {
            "date" : "2024-05-27",
            "weeks" : 0
        }
        self.run_test_calculate_date(request_data, 200, expected_data={
            "result" : "2024-05-27"
        })

    def test_calculate_date_missing_date(self):
        """
        Test case on endpoint `/calculateDate`
        where `date` is missing from the request data.
        """

        request_data = {
            "weeks" : 10
        }
        self.run_test_calculate_date(request_data, 400, expected_error_message="'date' is missing from request!")
    
    def test_calculate_date_invalid_date_format(self):
        """
        Test case on endpoint `/calculateDate`
        where the format of `date` in the request data is invalid.
        """
        request_data = {
            "date" : "2024/666/21",
            "weeks" : 10
        }
        self.run_test_calculate_date(request_data, 400, expected_error_message="'date' must be in YYYY-MM-DD format!")

    def test_calculate_date_missing_weeks(self):
        """
        Test case on endpoint `/calculateDate`
        where `weeks` is missing from the request data.
        """
        request_data = {
            "date" : "2024-05-27"
        }
        self.run_test_calculate_date(request_data, 400, expected_error_message="'weeks' is missing from request!")

    def test_calculate_date_weeks_is_not_integer(self):
        """
        Test case on endpoint `/calculateDate` where `weeks` is not an integer.
        """
        request_data = {
            "date" : "2024-05-27",
            "weeks" : 10.7
        }
        self.run_test_calculate_date(request_data, 400, expected_error_message="'weeks' must be an integer!")

    def test_calculate_date_weeks_is_not_numeric(self):
        """
        Test case on endpoint `/calculateDate` where `weeks` is not numeric.
        """
        request_data = {
            "date" : "2024-05-27",
            "weeks" : "asdf10"
        }
        self.run_test_calculate_date(request_data, 400, expected_error_message="'weeks' must be an integer!")

    def run_test_calculate_date(self, request_data,
                                expected_status_code,
                                expected_error_message=None,
                                expected_data={}):
        """
        Runs a test case on endpoint `/calculateDate`.
        """
        response = self.client.post('/calculateDate', json=request_data)
        self.verify_endpoint_with_json_response_data(response, expected_status_code,
                                                     self.get_expected_response_body(expected_status_code,
                                                                                     expected_error_message,
                                                                                     expected_data))

    @patch('honbasho_calendar.HonbashoCalendar.calculate_schedule')
    def test_get_honbasho_schedule(self, mock_calculate):
        """
        Normal test case on endpoint /getSumoHonbashoSchedule.
        """
        year = 2020
        mock_schedule = [
            {
                "basho": HonbashoCalendar.Basho.HATSU,
                "dates": [date(2020, 1, 12), date(2020, 1, 13), date(2020, 1, 14), date(2020, 1, 15), date(2020, 1, 16), date(2020, 1, 17), date(2020, 1, 18),
                          date(2020, 1, 19), date(2020, 1, 20), date(2020, 1, 21), date(2020, 1, 22), date(2020, 1, 23), date(2020, 1, 24), date(2020, 1, 25),
                          date(2020, 1, 26)]
            },
            {
                "basho": HonbashoCalendar.Basho.HARU,
                "dates": [date(2020, 3, 8), date(2020, 3, 9), date(2020, 3, 10), date(2020, 3, 11), date(2020, 3, 12), date(2020, 3, 13), date(2020, 3, 14),
                          date(2020, 3, 15), date(2020, 3, 16), date(2020, 3, 17), date(2020, 3, 18), date(2020, 3, 19), date(2020, 3, 20), date(2020, 3, 21),
                          date(2020, 3, 22)]
            },
            {
                "basho": HonbashoCalendar.Basho.NAGOYA,
                "dates": [date(2020, 7, 12), date(2020, 7, 13), date(2020, 7, 14), date(2020, 7, 15), date(2020, 7, 16), date(2020, 7, 17), date(2020, 7, 18),
                          date(2020, 7, 19), date(2020, 7, 20), date(2020, 7, 21), date(2020, 7, 22), date(2020, 7, 23), date(2020, 7, 24), date(2020, 7, 25),
                          date(2020, 7, 26)]
            },
            {
                "basho": HonbashoCalendar.Basho.AKI,
                "dates": [date(2020, 9, 13), date(2020, 9, 14), date(2020, 9, 15), date(2020, 9, 16), date(2020, 9, 17), date(2020, 9, 18), date(2020, 9, 19),
                          date(2020, 9, 20), date(2020, 9, 21), date(2020, 9, 22), date(2020, 9, 23), date(2020, 9, 24), date(2020, 9, 25), date(2020, 9, 26),
                          date(2020, 9, 27)]
            },
            {
                "basho": HonbashoCalendar.Basho.KYUSHU,
                "dates": [date(2020, 11, 8), date(2020, 11, 9), date(2020, 11, 10), date(2020, 11, 11), date(2020, 11, 12), date(2020, 11, 13), date(2020, 11, 14),
                          date(2020, 11, 15), date(2020, 11, 16), date(2020, 11, 17), date(2020, 11, 18), date(2020, 11, 19), date(2020, 11, 20), date(2020, 11, 21),
                          date(2020, 11, 22)]
            }
        ]
        expected_data = {
            "result" : [
                {
                    "basho": "HATSU",
                    "month": 1,
                    "month_name": calendar.month_name[1],
                    "dates": ["2020-01-12", "2020-01-13", "2020-01-14", "2020-01-15", "2020-01-16", "2020-01-17", "2020-01-18",
                            "2020-01-19", "2020-01-20", "2020-01-21", "2020-01-22", "2020-01-23", "2020-01-24", "2020-01-25",
                            "2020-01-26"]
                },
                {
                    "basho": "HARU",
                    "month": 3,
                    "month_name": calendar.month_name[3],
                    "dates": ["2020-03-08", "2020-03-09", "2020-03-10", "2020-03-11", "2020-03-12", "2020-03-13", "2020-03-14",
                            "2020-03-15", "2020-03-16", "2020-03-17", "2020-03-18", "2020-03-19", "2020-03-20", "2020-03-21",
                            "2020-03-22"]
                },
                {
                    "basho": "NAGOYA",
                    "month": 7,
                    "month_name": calendar.month_name[7],
                    "dates": ["2020-07-12", "2020-07-13", "2020-07-14", "2020-07-15", "2020-07-16", "2020-07-17", "2020-07-18",
                            "2020-07-19", "2020-07-20", "2020-07-21", "2020-07-22", "2020-07-23", "2020-07-24", "2020-07-25",
                            "2020-07-26"]
                },
                {
                    "basho": "AKI",
                    "month": 9,
                    "month_name": calendar.month_name[9],
                    "dates": ["2020-09-13", "2020-09-14", "2020-09-15", "2020-09-16", "2020-09-17", "2020-09-18", "2020-09-19",
                            "2020-09-20", "2020-09-21", "2020-09-22", "2020-09-23", "2020-09-24", "2020-09-25", "2020-09-26",
                            "2020-09-27"]
                },
                {
                    "basho": "KYUSHU",
                    "month": 11,
                    "month_name": calendar.month_name[11],
                    "dates": ["2020-11-08", "2020-11-09", "2020-11-10", "2020-11-11", "2020-11-12", "2020-11-13", "2020-11-14",
                            "2020-11-15", "2020-11-16", "2020-11-17", "2020-11-18", "2020-11-19", "2020-11-20", "2020-11-21",
                            "2020-11-22"]
                }
            ]
        }
        mock_calculate.return_value = mock_schedule
        self.run_get_honbasho_schedule(args={ "year": year }, expected_data=expected_data)
        mock_calculate.assert_called_once_with(year)

    @patch('honbasho_calendar.HonbashoCalendar.calculate_schedule')
    def test_get_honbasho_schedule_noargs(self, mock_calculate):
        """
        Test case on /getSumoHonbashoSchedule where the argument "year" is not provided.
        """
        self.run_get_honbasho_schedule(expected_status_code=400,
                                       expected_error_message="'year' must be provided in the request arguments!")
        mock_calculate.assert_not_called()

    @patch('honbasho_calendar.HonbashoCalendar.calculate_schedule')
    def test_get_honbasho_schedule_year_not_integer(self, mock_calculate):
        """
        Test case on /getSumoHonbashoSchedule where the value of argument "year" is not an integer.
        """
        self.run_get_honbasho_schedule(args={ "year": 20027.7 },
                                       expected_status_code=400,
                                       expected_error_message="Request argument 'year' must be an integer!")
        mock_calculate.assert_not_called()

    @patch('honbasho_calendar.HonbashoCalendar.calculate_schedule')
    def test_get_honbasho_schedule_year_before_2012(self, mock_calculate):
        """
        Test case on /getSumoHonbashoSchedule where the "year" is before 2012.
        """
        self.run_get_honbasho_schedule(args={ "year": 2011 },
                                       expected_status_code=400,
                                       expected_error_message="Request argument 'year' cannot be before 2012!")
        mock_calculate.assert_not_called()

    @patch('honbasho_calendar.HonbashoCalendar.calculate_schedule')
    def test_get_honbasho_schedule_exceed_max_year(self, mock_calculate):
        """
        Test case on /getSumoHonbashoSchedule
        where "year" is greater than the maximum allowed year value.
        """
        self.run_get_honbasho_schedule(args={ "year": 10000 },
                                        expected_status_code=400,
                                        expected_error_message="Request argument 'year' exceeded maximum allowed year value!")
        mock_calculate.assert_not_called()

    def run_get_honbasho_schedule(self, args={},
                                  expected_status_code=200, expected_error_message=None,
                                  expected_data={}):
        """
        Runs a test case on endpoint /getSumoHonbashoSchedule.
        """
        response = self.client.get('/getSumoHonbashoSchedule', query_string=args)
        self.verify_endpoint_with_json_response_data(response, expected_status_code,
                                                     self.get_expected_response_body(expected_status_code,
                                                                                     expected_error_message,
                                                                                     expected_data))
    
    def get_expected_response_body(self, status_code, error_message=None, data={}):
        '''
        Builds the expected response body for an endpoint that returns JSON response body
        for all status codes.\n
        If an error message is provided, build a JSON object with `code` as the status code
        and `message` as the provided message.
        '''
        if error_message == None:
            return data
        else:
            return {
                "code" : status_code,
                "message" : error_message
            }

    def verify_endpoint_with_json_response_data(self, response, expected_status_code, expected_data):
        """
        Verifies an endpoint where the normal response data is JSON.
        """
        assert response.status_code == expected_status_code
        data = json.loads(response.get_data())
        self.assertEqual(expected_data, data)