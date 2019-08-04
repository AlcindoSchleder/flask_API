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
        self._setDriver(self._app.config['DATABASE_DRIVER'])

    def __exit__(self, exc_type, exc_val, exc_tb):
        if (not self._engine.closed):
            self._engine.dispose()

    def _setDriver(self, driver) -> dict:
        self._appConfig = ConfigureConnection()
        self._app.config['ICITY_SECURITY_DATA'] = self._appConfig.globalConfig['ICITY_SECURITY_DATA']
        try:
            if (self._appConfig.result['state']['sttCode'] == 200):
                self._appConfig.dbDriver = driver
                self._DATABASE_URI = self._appConfig.connectionUri()
                self._config_db()
        except Exception as e:
            msg = f'A internal unexpected error occurred: ({e.args})'
            self.resultStatusCode = 500
            self.resultStatusMessage = msg
            raise Exception(msg)

    def _config_db(self):
        self.resultStatusCode = 200
        msg = f'Database {self._appConfig.databaseName} on {self._appConfig.databaseDriver} not found. Plase verify with your sysdba!'
        try:
            if not database_exists(self._DATABASE_URI):
                self.resultStatusCode = 404
                self.resultStatusMessage = msg
        except Exception as e:
            self.resultStatusCode = 500
            self.resultStatusMessage = f'{msg}: ({e.args})'
            raise Exception(f'{msg}: ({e.args})')
        
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
            if (self._session) and (self._session.is_active):
                self._session.close()
            msg = f"Can't create a session into Database {self._dbTable.name}: ({e.args})"
            self.resultStatusCode = 500
            self.resultStatusMessage = msg
            raise Exception(msg)

    def connect(self):
        self.resultStatusCode = 200
        if (not self.isConnected):
            self._app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            self._app.config['SQLALCHEMY_DATABASE_URI'] = self._DATABASE_URI
            try:
                self._engine = create_engine(self._DATABASE_URI, echo=False)
                self._createSession()
            except Exception as e:
                if (self._engine):
                    self._engine.dispose()
                msg = f'A Unexpected error occurred on connect database, please contact network admin! ({e.args})'
                self.resultStatusCode = 500
                self.resultStatusMessage = msg
                raise Exception(msg)

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
    def db(self):
        return self.session

    @property
    def dbTable(self):
        return self._dbTable

    @dbTable.setter
    def dbTable(self, table):
        if ((table) and (table.tableName)):
            if ((self._dbTable) and (table.tableName != self._dbTable.tableName)):
                self.disconnect()
            self._dbTable = table

    @property
    def dbTableName(self) -> str:
        return self._dbTable.tableName

    def setFilter(self, *filter):
        self._filter = filter
        
    def execCommand(self, aQuery: str, aParams: dict = None) -> dict:
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
        return self.result

    def browseRecord(self):
        self.resultStatusCode = 200
        try:
            print('-------> Iniciando a sessão!')
            if (not self._session.is_active):
                self._session.begin()

            print(f'-------> Iniciando a Busca na tabela {self.dbTableName}!')
            if (self._dbTable.filters is None):
                print(f'-------> Buscando todos os registros!')
                dbRecords = self._session.query(self._dbTable).all()
            else:
                print(f'-------> Buscando registros filtrados!')
                dbRecords = self._session.query(self._dbTable).filter(self._dbTable.filter).all()
            
            print('-------> Conteudor de dbRecords: ', dir(dbRecords))
            self.resultData = {dbRecords}
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            self.resultStatusCode = 500
            self.resultStatusMessage = f'Erro ao pesquisar registros na tabela {self.dbTableName}! : {e.args}'
            print(f'------>', self.resultStatusMessage)
        finally:
            self._filter = None
            self._session.close()

    def insertRecord(self):
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

    def updateRecord(self):
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

    def deleteRecord(self):
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
