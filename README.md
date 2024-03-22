# Python Web Service Demo
A simple demonstration web service app with Python and Flask.

This project also demonstrates:
1. API documentation by Swagger UI
2. Support for deployment to Docker
3. Unit tests for the Python application
4. GitHub workflow configurations to run unit tests, build and push the image to Docker

## Pre-requisites
* Flask
  - See [the installation instructions at Flask's homepage](https://flask.palletsprojects.com/en/3.0.x/installation/#install-flask).
* swagger-ui-py
  - Installation command: `pip3 install swagger-ui-py`
  - Reference: <https://pypi.org/project/swagger-ui-py/>

## Usage

**IMPORTANT: The app must be up and running in order for these links to work.**

Root URL: <http://localhost:5000/>

For the list of endpoints, see the Swagger UI API documentation at <http://localhost:5000/api/doc>.

### Startup

#### Run locally at the terminal
1. Go to the root directory of this project in the terminal.
2. Run with one of the following commands:
* `python3 -m flask --app App.py run`
* `flask --app App.py run`

#### Deploy to Docker

**WARNING: This app was designed to be deployed to a machine with Docker Desktop installed. It has not been tested on cloud Docker services and thus is not guaranteed to work there.**

This app may be deployed by either of the following methods:
1. Local deployment at the terminal
   - Command: `docker compose up --build -d`
2. Search for image `ccwong4869/python-webservice-demo`, select the tag name that matches the branch you wish to use, and click Pull or Run.
   - Public view at Docker Hub: <https://hub.docker.com/r/ccwong4869/python-webservice-demo>

Reference: <https://docs.docker.com/language/python/containerize/>

### Testing the deployment with Kubernetes (Docker Desktop)

For commands at the terminal, see: <https://docs.docker.com/language/python/deploy/>

Curl command for verification: `curl http://localhost:30001/`

### Running unit tests

1. Go to the root directory of this project in the terminal.
2. Run the command: `pytest`
   - To populate application logs to the console, use `pytest -o log_cli=true`