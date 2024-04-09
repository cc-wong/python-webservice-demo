from flask import Flask
from logging.config import dictConfig

import configparser
from dotenv import load_dotenv
import os


def create_app():
    """
    The application factory.
    """

    load_dotenv()

    config = configparser.ConfigParser()
    config.read('config.ini')

    log_level = os.environ.get('LOG_LEVEL', config['Logging'].get('log_level'))
    log_format = config['Logging'].get('format')

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': log_format,
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': log_level,
            'handlers': ['wsgi']
        }
    })
    
    app = Flask(__name__)
    app.logger.debug(os.environ)
    app.logger.debug(f'Configurations:-\nLog level: {log_level}\nLog format: {log_format}')
    return app