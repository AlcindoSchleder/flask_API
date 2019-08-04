# -*- coding: utf-8 -*-
from flask.views import MethodView

from server import icityServer
from workspaces.interface import InterfaceRoute
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
class BaseRoutes(InterfaceRoute):

    API_ROOT = icityServer.icity_prefix
    API_BASE_NAME = 'admin'
    VERSION = '1.0'
    PREFIX_ROUTE = f'{API_ROOT}/{API_BASE_NAME}'
    PATH_API = f'{API_ROOT}/{API_BASE_NAME}/{VERSION}'
