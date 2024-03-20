# Python Web Service Demo
A simple demonstration web service app with Python and Flask.

Includes:
1. API documentation by Swagger UI
2. Configuration files for deployment to Docker

## Pre-requisites
* Flask
  - See [the installation instructions at Flask's homepage](https://flask.palletsprojects.com/en/3.0.x/installation/#install-flask).
* swagger-ui-py
  - Installation command: `pip3 install swagger-ui-py`
  - Reference: <https://pypi.org/project/swagger-ui-py/>

## Usage
### Startup

The app must be up and running in order for web service calls and the link to the API documentation to work.

#### Run locally at the terminal
1. Go to the root directory of this project in the terminal.
2. Run with one of the following commands:
* `python3 -m flask --app App.py run`
* `flask --app App.py run`

#### Deploy to Docker

You should have Docker Desktop installed at your machine.

Command: `docker compose up --build -d`

Reference: <https://docs.docker.com/language/python/containerize/>

### To call the services
Base URL: <http://localhost:5000/>

### Swagger UI documentation
<http://localhost:5000/api/doc>