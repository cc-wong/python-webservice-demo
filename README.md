# Python Web Service Demo
A simple demonstration web service app with Python and Flask.

This project also demonstrates:
1. API documentation by Swagger UI / OpenAPI
2. Support for deployment to Docker
3. Unit tests for the Python application
4. GitHub workflow configurations to run unit tests, build and push the image to Docker

Wiki page: <https://github.com/cc-wong/python-webservice-demo/wiki>

## Deployment and startup
Dependencies:
* `Flask`
  - See [the installation instructions at Flask's homepage](https://flask.palletsprojects.com/en/3.0.x/installation/#install-flask).
* `flask_cors`
  - Required for handling Cross Origin Resource Sharing (CORS),
  to allow the webservices to be called from external sites.
   - Used for adding response header `Access-Control-Allow-Origin: *` to webservice calls.
  - Reference: <https://flask-cors.readthedocs.io/en/latest/#>
* `swagger-ui-py`
  - Installation command: `pip3 install swagger-ui-py`
  - Reference: <https://pypi.org/project/swagger-ui-py/>

### Run the app locally
1. Go to the root directory of this project at the terminal.
2. (Only required for the first time)\
   Install the dependencies by running:
   * `pip install -r requirements.txt`, or
   * `pip3 install <dependency name>` for each dependency
3. Run one of the following to start:
   * `python3 -m flask --app App.py run`
   *  `flask --app App.py run`

### Deploy to Docker Desktop
This app may be deployed to Docker Desktop by either of the following methods:
1. Local deployment at the terminal
   - Command: `docker compose up --build -d`
2. Search for image `ccwong4869/python-webservice-demo`, select the tag name that matches the branch you wish to use, and click Pull or Run.
   - See [this wiki page](https://github.com/cc-wong/python-webservice-demo/wiki/Docker-Images) for details.

Reference: <https://docs.docker.com/language/python/containerize/>

#### Testing the deployment with Kubernetes
For commands at the terminal, see: <https://docs.docker.com/language/python/deploy/>

Curl command for verification: `curl http://localhost:30001/`

## Developers' notes
### URLs for local development/testing
| Name | URL |
| ---: | :--- |
| Webservice base URL | <http://localhost:5000/> |
| API documentation<br/>(OpenAPI a.k.a. Swagger UI) | <http://localhost:5000/api/doc> |

### Run unit tests
1. Go to the root directory of this project in the terminal.
2. Run the command: `pytest`
   - To populate application logs to the console, use `pytest -o log_cli=true`

#### Coverage report
> [!IMPORTANT]
> The pytest-cov plugin is required.\
> For details and installation instructions, see: <https://pypi.org/project/pytest-cov/>

> [!NOTE]
> The commands below are run at the root directory of this project unless otherwise stated.

Summary-level coverage report to the console:
```
pytest --cov
```
To generate a detailed HTML coverage report (output at directory `htmlcov/`):
```
pytest --cov --cov-report=html
```
pytest's help command includes options of coverage reporting after the plugin is installed:
```
pytest --help
```
A usage guide for the plugin is also available at:
https://pytest-cov.readthedocs.io/en/latest/reporting.html