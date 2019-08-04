# -*- coding: utf-8 -*-
from common.helpers.operationResults import OperationResults
from common.base.connection import Connection
from workspaces.admin.categories.schema import Categories, TTypeRoles

"""
    Class that manage categories table by restfull api
    * class      RouteCategories
    * requires   python 3.+
    * version    1.0.0
    * package    iCity
    * subpackage iCity
    * author     Alcindo Schleder <alcindoschleder@gmail.com>
    * copyright  Vocatio Telecom <https://www.vocatiotelecom.com.br>
""" 
class HandleCategories(Connection):

    def __init__(self, app):
        super(HandleCategories, self).__init__(app)
 
    def browse(self, id: int = 0, page: int = 0):
        self.resultStatusCode = 200

        print('------> Verificando PK se deve inserir um filtro!')
        if (id > 0): # if is valid id param
            # read a registry from categories table with pkCategories = id value
            Categories.filters = (Categories.pk_categories == id)
        print('------> Verificando PAGE se deve inserir um filtro!')
        if (page > 0):
            # set limit to page of generate pagination if page > 0 and all to all recores
            # Categories.limit = 10
            pass
        print(f'------> Criando o esquema de Categorias atribuindo o ID ({id}) à Categories()!')
        self.dbTable = Categories(pkCategories = id)
        print('------> Executando o Browser do DB!')
        self.browseRecord()

        print('------> Retornando o result!', self.result)
        return self.result
 
    def insert(self, data: dict):
        self.resultStatusCode = 200

        self.db.dbTable = Categories(
            dscTCat = data.dscTCat, 
            flagTCat = data.flagTCat, 
            flagDefault = data.flagDefault
        )
        self.insertRecord()

        return self.result
 
    def update(self, data: dict):
        self.resultStatusCode = 200

        Categories.filters = (Categories.filters == data.pkCategories)
        self.dbTable = Categories(
            pkCategories = data.pkCategories, 
            dscTCat = data.dscTCat, 
            flagTCat = data.flagTCat, 
            flagDefault = data.flagDefault
        )
        self.updateRecord()

        return self.result
 
    def delete(self, pk: int):
        self.resultStatusCode = 200

        Categories.filters = (Categories.filters == pk)
        self.dbTable = Categories(pkCategories = pk)
        self.deleteRecord()

        return self.result
