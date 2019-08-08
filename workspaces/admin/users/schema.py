# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Table, MetaData, Column, Integer, String, DateTime, ForeignKey, inspect
from sqlalchemy.orm import validates
from common.base.schema.schemabase import SchemaBase

'''
	pk_registers integer NOT NULL DEFAULT nextval('public.sq_registers'::regclass),
	type_owner public.type_owner NOT NULL DEFAULT 0,
	user_name varchar(50) NOT NULL,
	first_name varchar(50),
	last_name varchar(50),
	alias_reg varchar(50),
	user_login varchar(50) NOT NULL,
	user_pwd varchar(255),
	reg_score smallint NOT NULL DEFAULT 0,
	flag_confirmed public.flag_true_false NOT NULL DEFAULT 0,
	flag_mailer public.flag_true_false NOT NULL DEFAULT 1,
	expire_date timestamp,
	hash_data varchar(64) NOT NULL,
	update_date timestamp,
	insert_date public.timestamp_default NOT NULL DEFAULT now(),

'''
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
class Categories(SchemaBase):
    __tablename__ = 'categories'
    
    pk_categories = Column(Integer, primary_key=True)
    dsc_tcat = Column(String(100), nullable=False)
    flag_tcat = Column(Integer, nullable=False, default=TTypeRoles.trUsers)
    flag_default = Column(Integer, nullable=False, default=0)
    date_update = Column(DateTime, nullable=True)
    date_insert = Column(DateTime, nullable=False)

    def __init__(self, pkCategories = None, dscTCat = None, flagTCat = None, flagDefault = None, dateUpdate = None, dateInsert = None):
        self.pk_categories = pkCategories if (pkCategories) else 0
        self.dsc_tcat = dscTCat if (dscTCat) else ' '
        self.flag_tcat = flagTCat if (flagTCat) else 0
        self.flag_default = flagDefault if (flagDefault) else 0
        self.date_update = dateUpdate
        self.date_insert = dateInsert if (dateInsert) else datetime.now()

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
