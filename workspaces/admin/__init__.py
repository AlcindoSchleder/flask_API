# -*- coding: utf-8 -*-
from flask.views import MethodView
from common.helpers.operationResults import OperationResults
from server import icityServer

"""
    Class to Base all Routes for Admin Workspace
    * class      BaseRoutes
    * requires   python 3.+, PyQt5
    * version    1.0.0
    * package    pyCommom
    * subpackage pyCommom
    * author     Alcindo Schleder <alcindoschleder@gmail.com>
    * copyright  Vocatio Telecom <https://www.vocatiotelecom.com.br>
"""
class BaseRoutes(MethodView, OperationResults):

    API_ROOT = icityServer.icity_prefix
    API_BASE_NAME = 'admin'
    VERSION = '1.0'
    PREFIX_ROUTE = f'{API_ROOT}/{API_BASE_NAME}'
    PATH_API = f'{API_ROOT}/{API_BASE_NAME}/{VERSION}'

    # def __init__(self):
    #     super(BaseRoutes, self).__init__()
        
    def get(self):
        raise NotImplementedError()
