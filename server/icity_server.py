# -*- coding: utf-8 -*-
import os
from flask import Flask, Blueprint
from flask_restplus import Api
from common import COMMON_DIRECTORY
from common.helpers.operationResults import OperationResults

CONFIGURE_FILE = f'{COMMON_DIRECTORY}/config.json'
CONFIGURE_HASH = os.environ.get("CONFIG_HASH", default="b17913cc95df7a21eb8faa3fb55571e70f963f26a613bc72677842033506f32c")
CONFIGURE_DATA = "ICITY_SECURITY_DATA"

"""
    Class that initialize API Server
    * class      ICityServer
    * requires   python 3.+, PyQt5
    * version    1.0.0
    * package    icity_api
    * subpackage icity_api
    * author     Alcindo Schleder <alcindoschleder@gmail.com>
    * copyright  Vocatio Telecom <https://icity.vocatio.com.br>
"""
class ICityServer(OperationResults):
    def __init__(self):
        super(ICityServer, self).__init__()

        # Create a instance of Flask and get api configuration
        self.icity_app = Flask(__name__)

        self.icity_prefix = '/icity-api'
        self.icity_app.config['FLASK_ENV'] = os.environ.get("FLASK_ENV", default="development")
        self.setEnvironmentConfig()

        # Create all blueprint apps 
        self.icity_bp = Blueprint('home', __name__)
        self.icity_admin_bp = Blueprint('admin', __name__)

        # Create a swagger api from home app
        self.icity_api = Api(
            app = self.icity_bp,
            version = "1.0",
            title = "Vocatio Telecom API",
            description = "Api para uso como Fonte de Estudos",
            doc=self.icity_prefix + '/docs'
        )

    def setEnvironmentConfig(self):
        from server.config import config_by_name

        mode = config_by_name[self.icity_app.config['FLASK_ENV']]

        # self.icity_app.config['SECRET_KEY'] = self.apikey
        self.icity_app.config['DEBUG'] = mode.DEBUG
        self.icity_app.config['TESTING'] = mode.TESTING
        self.icity_app.config['DB_SERVER'] = mode.DB_SERVER
        self.icity_app.config['DATABASE_DRIVER'] = mode.DATABASE_DRIVER
        self.icity_app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = mode.PRESERVE_CONTEXT_ON_EXCEPTION
        self.icity_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = mode.SQLALCHEMY_TRACK_MODIFICATIONS
    
    def run(self):
        self.icity_app.run(
            debug = self.icity_app.config['DEBUG'] 
        )
