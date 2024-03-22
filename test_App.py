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
    workers_json_text = json.dumps(workers)

    ## Tests endpoint: /getWorkers
    @patch("builtins.open", new_callable=mock_open, read_data=workers_json_text)
    def test_get_workers(self, mock_file):
        expected = TestWebApp.workers
        filename = "data/worker_list.json"

        response = self.client.get('/getWorkers')
        assert response.status_code == 200

        data = json.loads(response.get_data())
        self.assertEqual(expected, data)

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
