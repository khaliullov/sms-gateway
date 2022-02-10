from waitress import serve
from flask import Flask
from flask_restx import Api, Resource, fields, apidoc
from flask_jwt_extended import (JWTManager)

import os
import logging
import datetime

from environment.instance import environment_config
from environment.instance import jwt_config
from environment.instance import database_config
from database.instance import init_db


class MyApi(Api):
    def _register_apidoc(self, app):
        conf = app.extensions.setdefault("restx", {})
        if not conf.get("apidoc_registered", False):
            apidoc.apidoc._static_url_path = app.config['API_PREFIX'] + 'swaggerui'
            app.register_blueprint(apidoc.apidoc)
        conf["apidoc_registered"] = True


class Server(object):

    def __init__(self):
        self.app = Flask(__name__)
        self.app.name = "backend"

        # Swagger UI
        self.app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'

        # Exceptions are re-raised rather than being handled by the app’s error handlers.
        self.app.config['PROPAGATE_EXCEPTIONS'] = True

        # flask_jwt_extended
        self.app.config['JWT_SECRET_KEY'] = jwt_config["secret"]
        self.app.config['JWT_ALGORITHM'] = jwt_config["algorithm"]
        ## How long (in seconds) an access token should live before it expires
        self.app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=jwt_config["token_expires"])
        # The key of the error message in a JSON error response
        self.app.config['JWT_ERROR_MESSAGE_KEY'] = "message"

        # flask_basicauth
        self.app.config['BASIC_AUTH_USERNAME'] = os.environ.get("API_USERNAME", "admin")
        self.app.config['BASIC_AUTH_PASSWORD'] = os.environ.get("API_PASSWORD", "admin")

        # prefix
        self.app.config['API_PREFIX'] = os.environ.get("API_PREFIX", "/")

        authorizations = {
            'Bearer': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': "Type in the *'Value'* input box below: **'Bearer XXX'**, where XXX is the token"
            },
            'Basic': {
                'type': 'basic',
                'in': 'header',
                'name': 'Authorization'
            }
        }

        #with mock.patch('flask_restx.Api._register_apidoc', _register_apidoc):
        self.api = MyApi(self.app,
                         version='1.0.9',
                         title='SMS Gateway',
                         description='This REST API allow you to send and receive SMS',
                         doc=os.environ.get("API_PREFIX", "/"),
                         authorizations=authorizations,
                         security=environment_config["security"],
                         prefix=self.app.config['API_PREFIX']
                         )

        self.jwt = JWTManager(self.app)

    def run(self):
        init_db()

        logger = logging.getLogger('waitress')
        logger.setLevel(logging.INFO)
        logger = logging.getLogger('backend')
        logger.setLevel(logging.INFO)

        serve(
            self.app,
            host=environment_config["ip"],
            port=environment_config["port"]
        )


server = Server()
