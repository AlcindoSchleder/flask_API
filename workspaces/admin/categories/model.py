# -*- coding: utf-8 -*-
from flask_restplus import fields

"""
    Classes that Define a serializer model
    * requires   python 3.+, PyQt5
    * version    1.0.0
    * package    icity_api
    * subpackage icity_api
    * author     Alcindo Schleder <alcindoschleder@gmail.com>
    * copyright  Vocatio Telecom <https://www.vocatiotelecom.com.br>
"""

class CategoriesModel:
    def __call__(self, api):
        return api.model('Categories', {
            'pk_categories': fields.Integer(required=False, description='Código da categoria'),
            'dsc_tcat': fields.String(required=True, description='Descrição da categoria'),
            'flag_tcat': fields.Integer(required=True, description='Tipo da categoria'),
            'flag_default': fields.Integer(required=True, description='Marca categoria como default'),
            'date_update': fields.DateTime(description='Data da última atualização do registro'),
            'date_insert': fields.DateTime(description='Data da inserção do registro')
        })
