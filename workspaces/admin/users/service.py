# -*- coding: utf-8 -*-
from datetime import datetime

from common.base.db.connection import Connection
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
        filters = None
        if (id > 0):
            filters = (Categories.pk_categories == id)
        
        #   ////////// PAGINATION ////////
        # if (page > 0): order_by()[limit integer:offset integer]
        #     # set limit to page of generate pagination if page > 0 and all to all recores
        #     # Categories.limit = 10
        #     pass
        # order_by = Categories.dsc_tcat
        
        self.dbTable = Categories
        self.browseRecord(filters)

        return self.result
 
    def insert(self, data):
        self.resultStatusCode = 200
        data['update_date'] = None
        data['insert_date'] = datetime.now()
        self.dbTable = Categories(
            dscTCat = data['dsc_tcat'], 
            flagTCat = data['flag_tcat'], 
            flagDefault = data['flag_default'],
            dateUpdate = data['update_date'],
            dateInsert = data['insert_date']
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
