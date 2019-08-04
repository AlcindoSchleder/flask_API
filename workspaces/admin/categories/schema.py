# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, MetaData, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import validates

Base = declarative_base()

class TTypeRoles():
    trUsers      = 0
    trAdmin      = 1
    trCustomers  = 2
    trSuppliers  = 3
    trEmployes   = 4
    trOthers     = 5
 
"""
    Class that define the category table
    * class      User
    * requires   python 3.5+
    * version    1.0.0
    * package    icity-BlockChain
    * author     Alcindo Schleder <alcindoschleder@gmail.com>
    * copyright  Vocatio Telecom <https://www.vocatiotelecom.com.br>
"""
class Categories(Base):
    __tablename__ = 'categories'
    __filters__   = None
    
    pk_categories = Column(Integer, primary_key=True)
    dsc_tcat = Column(String(100), nullable=False)
    flag_tcat = Column(Integer, nullable=False, default=TTypeRoles.trUsers)
    flag_default = Column(Integer, nullable=False, default=0)
    date_update = Column(DateTime, nullable=True)
    date_insert = Column(DateTime, nullable=False)

    def __init__(self, pkCategories = None, dscTCat = None, flagTCat = None, flagDefault = None, updateDate = None, insertDate = None):
        self.pk_categories = pkCategories if (pkCategories) else 0
        self.dsc_tcat = dscTCat if (dscTCat) else ' '
        self.flag_tcat = flagTCat if (flagTCat) else 0
        self.flag_default = flagDefault if (flagDefault) else 0
        self.update_date = updateDate
        self.insert_date = insertDate if (insertDate) else datetime.now

    @validates('flag_tcat', include_backrefs=False)
    def validate_flag_tcat(self, key, address):
        assert ((address > -1) and (address < 6)), "Field 'flag_tcat' only supports value between 0 and 5!"
        return address

    @validates('flag_default', include_backrefs=False)
    def validate_flag_default(self, key, address):
        assert (address in (0, 1)), "Field 'flag_default' only accept false(0) or true(1)!"
        return address

    @property
    def tableName(self):
        return self.__tablename__

    @property
    def filters(self):
        return self.__filters__

    @filters.setter
    def filters(self, *filters):
        self.__filters__ = filters
    
    def __repr__(self):
        return "<Categories(pk_categories='%s', dsc_cat='%s', flag_tcat='%s', flag_default='%s', date_insert='%s', date_update='%s')>" % (
            self.pk_categories, self.dsc_tcat, self.flag_tcat, self.flag_default, self.date_insert, self.date_update)

