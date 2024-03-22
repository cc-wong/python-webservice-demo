import unittest
from unittest.mock import patch, mock_open
from flaskapp import create_app
from App import application
import json

class TestWebApp(unittest.TestCase):

    ## Setup before test run.
    def setUp(self):
        self.appctx = application.app_context()
        self.appctx.push()
        self.client = application.test_client()

    ## Tear down after test run.
    def tearDown(self):
        self.appctx.pop()
        self.appctx = None
    
    ## Tests endpoint: /
    def test_hello_world(self):
        response = self.client.get('/')
        assert response.status_code == 200

        message = response.get_data(as_text=True)
        assert message == "<h1>Hello World!</h1>"

    ## Tests endpoint: /<name>
    def test_personal_greeting(self):
        name = "Lulu"

        response = self.client.get(f'/{name}')
        assert response.status_code == 200

        message = response.get_data(as_text=True)
        assert message == f"Hello, {name}!"

    # Mock JSON data in test cases on /getWorkers
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

    ## Tests endpoint /getWorkers where request parameter set is empty
    def test_get_workers_paramset_empty(self):
        self.run_test_get_workers({}, 200, TestWebApp.workers)

    ## Tests endpoint /getWorkers where the work_days request parameter is an empty list
    def test_get_workers_workdays_param_empty(self):
        self.run_test_get_workers({ "work_days" : [] }, 200, TestWebApp.workers)

    ## Tests endpoint /getWorkers where the work_days request parameter is non-empty
    def test_get_workers_workdays_param_nonempty(self):
        self.run_test_get_workers({ "work_days" : [ "MONDAY", "WEDNESDAY" ] }, 200, {
            "workers" : [
                TestWebApp.workers["workers"][0],
                TestWebApp.workers["workers"][2]
            ]
        })

    ## Tests endpoint /getWorkers where the work_days request parameter contains invalid values
    def test_get_workers_workdays_param_invalid(self):
        self.run_test_get_workers({ "work_days" : [ "MONDAY", "INVALID" ] },
                                  400, "Invalid value for parameter work_days!")

    ## Runs a test case on endpoint: /getWorkers
    @patch("builtins.open", new_callable=mock_open, read_data=workers_json_text)
    def run_test_get_workers(self, param_work_days, expected_status_code, expected_data, mock_file):
        filename = "data/worker_list.json"

        response = self.client.post('/getWorkers', json=param_work_days)
        assert response.status_code == expected_status_code

        if expected_status_code == 200:
            data = json.loads(response.get_data())
            self.assertEqual(expected_data, data)
        else:
            assert response.data.decode('utf-8') == expected_data

        assert open(filename, "utf8").read() == TestWebApp.workers_json_text
        mock_file.assert_called_with(filename, "utf8")

    # Tests endpoint: /timestwo; happy path
    def test_multiply_by_two_normal(self):
        response = self.client.post('/timestwo', data={"num" : 3})
        assert response.status_code == 200

        expected = {
            "num" : 3,
            "result" : 6
        }
        data = json.loads(response.get_data())
        self.assertEqual(expected, data)

    # Tests endpoint: /timestwo; request parameter "num" is not an integer
    def test_multiply_by_two_noninteger_param(self):
        response = self.client.post('/timestwo', data={"num" : "not-a-number"})
        assert response.status_code == 400
        assert response.data.decode('utf-8') == "'num' must be an integer."

    # Tests endpoint: /timestwo; request parameter "num" does not exist
    def test_multiply_by_two_no_request_param(self):
        response = self.client.post('/timestwo', data={})
        assert response.status_code == 400
        assert response.data.decode('utf-8') == "'num' not present in request parameters."
