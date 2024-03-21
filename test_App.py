import unittest
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

    ## Tests endpoint: /json
    def test_json(self):
        response = self.client.get('/json')
        assert response.status_code == 200

        data = json.loads(response.get_data())
        assert data["name"] == "Chan Tai Man"
        assert data["is_alive"] is True
        assert data["age"] == 56

        work_days_expected = [ "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        assert data["work_days"] == work_days_expected
    
    # Tests endpoint: /timestwo; happy path
    def test_multiply_by_two_normal(self):
        response = self.client.post('/timestwo', data={"num" : 3})
        assert response.status_code == 200

        data = json.loads(response.get_data())
        assert data["num"] == 3
        assert data["result"] == 6

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
