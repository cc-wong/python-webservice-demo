from flask import Flask

## Application factory
def create_app():
    app = Flask(__name__)
    return app