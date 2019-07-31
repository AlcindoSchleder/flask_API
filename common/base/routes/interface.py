# -*- coding: utf-8 -*-
from flask.views import MethodView

from common.helpers.operationResults import OperationResults

"""
    Class that inform a error code of http list
    * class      httpErrorCodes
    * requires   python 3.+, PyQt5
    * version    1.0.0
    * package    pyCommom
    * subpackage pyCommom
    * author     Alcindo Schleder <alcindoschleder@gmail.com>
    * copyright  Vocatio Telecom <https://www.vocatiotelecom.com.br>
"""

class InterfaceRoute(MethodView, OperationResults):

    def __init__(self):
        super(InterfaceRoute, self).__init__()

    def get(self):
        raise NotImplementedError()
