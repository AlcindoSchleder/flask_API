# -*- coding: utf-8 -*-
import json
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database
from common.base.interfaceDB import IDatabases
from common.db.configureConnection import ConfigureConnection

"""
    Class that implements a Basic DataBase Connection
    * class      Connection
    * requires   python 3.+
    * version    1.0.0
    * package    icity-BlockChain
    * author     Alcindo Schleder <alcindoschleder@gmail.com>
    * copyright  Vocatio Telecom <https://www.vocatiotelecom.com.br>
"""
class Connection(IDatabases):

    def __init__(self, app):
        super(Connection, self).__init__()
        self._app = app
        self._appConfig = None
        self._engine  = None
        self._session = None
        self._dbTable = None
        self._filter = None
        self._DATABASE_URI = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if (not self._engine.closed):
            self._engine.dispose()

    def setDriver(self, driver):
        self._appConfig = ConfigureConnection()
        self._app.config['ICITY_SECURITY_DATA'] = self._appConfig.globalConfig['ICITY_SECURITY_DATA']
        try:
            if (self._appConfig.result['code']['sttCode'] == 200):
                self._appConfig.dbDriver = driver
                self._DATABASE_URI = self._appConfig.connectionUri()
                self._config_db()
        except Exception as e:
            self.resultStatusCode = 500
            self.resultStatusMessage = 'A internal unexpected error occurred: %s' %(e)            
        finally:
            return self.result

    def _config_db(self):
        self.resultStatusCode = 200
        try:
            if not database_exists(self._DATABASE_URI):
                self.resultStatusCode = 404
                self.resultStatusMessage = 'Database %s on %s not found. Plase verify with your sysdba!' %(self._appConfig.databaseName, self._appConfig.databaseDriver)
        finally:
            return self.result
        
    def _createSession(self):
        if ((not self._engine) and (self._engine.closed)):
            self.resultStatusCode = 301
            self.resultStatusMessage = 'Database not connected!'
            return False
        try:
            Session = sessionmaker(bind=self._engine)
            Session.configure(bind=self._engine)
            self._session = Session(autocommit=True)
            return True
        except Exception as e:
            if (self._session.is_active):
                self._session.close()
            self.resultStatusCode = 500
            self.resultStatusMessage = "Can't create a session into Database %s (%s)" %(self._dbTable.name, e.args)
            return False

    def connect(self):
        self.resultStatusCode = 200
        self._app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self._app.config['SQLALCHEMY_DATABASE_URI'] = self._DATABASE_URI
        try:
            self._engine = create_engine(self._DATABASE_URI, echo=False)
            self._createSession()
        except:
            if (self._engine):
                self._engine.dispose()
            self.resultStatusCode = 500
            self.resultStatusMessage = 'A Unexpected error occurred on connect database, please contact network admin!'
        finally:
            return self.result

    def disconnect(self):
        if ((self._session) and (self._session.is_active)):
            self._session.close()
        return True

    def isConnected(self):
        return ((self._session) and (self._session.is_active))

    @property
    def engine(self):
        return self._engine
    
    @property
    def session(self):
        return self._session

    @property
    def dbTable(self):
        return self._dbTable

    @dbTable.setter
    def dbTable(self, table):
        if ((table) & (table.tableName)):
            if (table.tableName != self._dbTable.tableName):
                self.disconnect()
            self._dbTable = table

    @property
    def dbTableName(self):
        return self._dbTable.tableName

    def setFilter(self, *filter):
        self._filter = filter
        
    def execCommand(self, aQuery: str, aParams: dict = None):
        if (not self._session.is_active):
            self._session.begin()
        if (self.resultStatusCode != 200):
            return False
        try:
            dbObj = self._session.query(self.dbTable).from_statement(text(aQuery)).params(aParams).all()
            self._session.commit()
            self.resultData = dbObj
        except Exception as e:
            self._session.rollback()
            self.resultStatusCode = 500
            self.resultStatusMessage = 'Erro on execute sql command!' + str(e.args)
        finally:
            self._session.close()
        return (self.resultStatusCode == 200)

    def browse(self):
        self.resultStatusCode = 200
        try:
            if (not self._session.is_active):
                self._session.begin()

            data = []
            if (self._dbTable.filters is None):
                dbData = self._session.query(self._dbTable).all()
            else:
                dbData = self._session.query(self._dbTable).filter(self._dbTable.filter).all()
            
            idx = 0
            for regData in dbData:
                data[idx] = regData
                idx += 1 

            self.resultData = data
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            self.resultStatusCode = 500
            self.resultStatusMessage = 'Erro ao pesquisar registros na tabela %s! : %s' %(self.dbTableName, str(e.args))
        finally:
            self._filter = None
            self._session.close()
        return (self.resultStatusCode == 200)

    def insert(self):
        self.resultStatusCode = 200
        try:
            if (not self._session.is_active):
                self._session.begin()
            data = self._session.add(self._dbTable)
            self.resultData = data
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            self.resultStatusCode = 500
            self.resultStatusMessage = 'Erro ao inserir um registro na tabela %s! : %s' %(self.dbTableName, str(e.args))
        finally:
            self._session.close()
        return (self.resultStatusCode == 200)

    def update(self):
        self.resultStatusCode = 200
        try:
            if (not self._session.is_active):
                self._session.begin()
            data = self._session.update(self._dbTable)
            self.resultData = data
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            self.resultStatusCode = 500
            self.resultStatusMessage = 'Erro ao editar um registro na tabela %s! : %s' %(self.dbTableName, str(e.args))
        finally:
            self._session.close()
        return (self.resultStatusCode == 200)

    def delete(self):
        self.resultStatusCode = 200
        try:
            if (not self._session.is_active):
                self._session.begin()
            self._session.delete(self._dbTable)
            self.resultData = {}
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            self.resultStatusCode = 500
            self.resultStatusMessage = 'Erro ao deletar um registro na tabela %s!: %s' %(self.dbTableName, str(e.args))
        finally:
            self._session.close()
        return (self.resultStatusCode == 200)
