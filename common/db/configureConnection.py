# -*- coding: utf-8 -*-
from common.helpers.loadConfig import LoadJsonFiles
from common.helpers.operationResults import OperationResults
from server.icity_server import CONFIGURE_FILE, CONFIGURE_HASH

SUPPORTED_DRIVERS = ['mysql', 'mongodb', 'sqlite', 'postgresql']
DRIVER_MAP = {
    "mysql"     : "MYSQL_DATABASE_CONNECTION",
    "postgresql": "PGSQL_DATABASE_CONNECTION",
    "sqlite"    : "SQLITE_DATABASE_CONNECTION",
    "infuxdb"   : "INFLUX_DATABASE_CONNECTION",
    "mongodb"   : "MONGO_DATABASE_CONNECTION"
}
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
class ConfigureConnection(OperationResults):

    def __init__(self):
        super(ConfigureConnection, self).__init__()
        self.resultStatusCode = 200
        self._globalConfig = None
        self._dbDriver = 'sqlite'
        self._configDriver = DRIVER_MAP[self._dbDriver]
        try:
            ljf = LoadJsonFiles(CONFIGURE_FILE)
            self.result = ljf.checkFileHash(CONFIGURE_HASH)
            if (self.resultStatusCode != 200):
                raise Exception(self.resultStatusMessage)
            self._globalConfig = ljf.dictData
        except Exception as e:
            msg = f'Can not load config file {CONFIGURE_FILE}!!\nRazon: {e.args}'
            self.resultStatusCode = 500
            self.resultStatusMessage = msg
            raise Exception(msg)

    def connectionUri(self):
        if (self.resultStatusCode != 200):
            return False

        driver = self._globalConfig[self._configDriver]["database"]["driver"]
        host   = self._globalConfig[self._configDriver]["database"]["host"]
        user   = self._globalConfig[self._configDriver]["database"]["user"]
        pwd    = self._globalConfig[self._configDriver]["database"]["password"]
        dbName = self._globalConfig[self._configDriver]["database"]["db_name"]
        if (driver == 'sqlite'):
            from data import DATABASE_PATH
            return f'{driver}:///{DATABASE_PATH}/{dbName}'
        else:
            return f'{driver}://{user}:{pwd}@{host}/{dbName}'

    @property
    def globalConfig(self):
        return self._globalConfig

    @property
    def databaseDriver(self):
        return self._globalConfig[self._configDriver]["database"]["driver"]

    @property
    def databaseName(self):
        return self._globalConfig[self._configDriver]["database"]["db_name"]

    @property
    def databaseUser(self):
        return self._globalConfig[self._configDriver]["database"]["user"]

    @property
    def databasePassword(self):
        return self._globalConfig[self._configDriver]["database"]["password"]

    @property
    def dbDriver(self):
        return self._dbDriver

    @dbDriver.setter
    def dbDriver(self, driver: str):
        if (driver in SUPPORTED_DRIVERS):
            self._dbDriver = driver
            self._configDriver = DRIVER_MAP[self._dbDriver]
        else:
            self.resultStatusMessage = "Driver '%s' not implemented yet!" %(self._dbDriver)
