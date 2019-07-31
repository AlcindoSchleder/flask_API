# -*- coding: utf-8 -*-
from common.base.connection import Connection
from sqlalchemy import text

"""
    Class that implements a Connection To PostgreSQL Database
    * class      pgConnection
    * requires   python 3.+
    * version    1.0.0
    * package    icity-BlockChain
    * author     Alcindo Schleder <alcindoschleder@gmail.com>
    * copyright  Vocatio Telecom <https://www.vocatiotelecom.com.br>
"""
class pgConnection(Connection):

    def __init__(self, app):
        super(pgConnection, self).__init__(app)
        self.result = self.setDriver('postgresql')
        if (self.resultStatusCode == 200):
            self.connect()

    @property
    def db(self):
        return self.session


