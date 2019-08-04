# -*- coding: utf-8 -*-
from flask import Flask
from flask_restplus import Namespace, reqparse

from server import icityServer
from workspaces.admin import BaseRoutes
from workspaces.admin.categories.service import HandleCategories
from workspaces.admin.categories.model import CategoriesModel


ns = Namespace(BaseRoutes.API_BASE_NAME, description='Cadastro de Categorias')

CategoryModel = CategoriesModel()(ns) 

page_parser = reqparse.RequestParser()
page_parser.add_argument('page', type=int, default=1, help='Página da lista')

db = HandleCategories(icityServer.icity_app)
db.connect()


"""
    Class that manage categories table by restfull api
    * class      RouteCategories
    * requires   python 3.+
    * version    1.0.0
    * package    iCity
    * subpackage iCity/Admin
    * author     Alcindo Schleder <alcindoschleder@gmail.com>
    * copyright  Vocatio Telecom <https://www.vocatiotelecom.com.br>
""" 
@ns.route('/')
class CategoriesListRoutes(BaseRoutes):

    def __init__(self, *args, **kwargs):
        super(CategoriesListRoutes, self).__init__(args, kwargs)
        self.db = db

    @ns.doc('Lista as categorias de usuários')
    @ns.expect(page_parser)
    @ns.doc(responses={500: 'Internal Error:'})
    @ns.marshal_list_with(CategoryModel)
    def get(self, page: int = 0):
        self.resultStatusCode = 200
        print('------> Chamando o método Browser')
        self.result = self.db.browse(page=page)
        if (self.resultStatusCode != 200):
            ns.abort(code=self.resultStatusCode, message=self.resultStatusMessage)
        return self.result, self.resultStatusCode
 
    @ns.doc('Insere novas categorias de usuários')
    @ns.doc(responses={500: 'Internal Error:'})
    @ns.expect(CategoryModel)
    @ns.marshal_with(CategoryModel)
    def post(self):
        self.resultStatusCode = 200

        data = {
            "dscTCat": CategoryModel.get('dsc_tcat'),
            "flagTCat": CategoryModel.get('flag_tcat'),
            "flagDefault": CategoryModel.get('flag_default')
        }
        self.result = self.db.insert(data)
        if (self.resultStatusCode != 200):
            ns.abort(code=self.resultStatusCode, message=self.resultStatusMessage)
        return self.result, self.resultStatusCode

@ns.route('/<int:id>')
class CategoriesRoutes(BaseRoutes):

    def __init__(self, *args, **kwargs):
        super(CategoriesRoutes, self).__init__(args, kwargs)
        self.db = db

    @ns.doc('Busca uma categoria de usuários')
    @ns.doc(responses={500: 'Internal Error:'})
    @ns.marshal_list_with(CategoryModel)
    def get(self, id: int = 0, page: int = 0):
        self.resultStatusCode = 200
        self.result = self.db.browse(id)
        if (self.resultStatusCode != 200):
            ns.abort(code=self.resultStatusCode, message=self.resultStatusMessage)
        return self.result, self.resultStatusCode
 
    @ns.doc('Altera uma categoria de usuários')
    @ns.doc(responses={500: 'Internal Error:'})
    @ns.expect(CategoryModel)
    @ns.marshal_with(CategoryModel)
    def put(self, id):
        self.resultStatusCode = 200

        data = {
            "pkCategories": id,
            "dscTCat": CategoryModel.get('dsc_tcat'),
            "flagTCat": CategoryModel.get('flag_tcat'),
            "flagDefault": CategoryModel.get('flag_default')
        }
        self.result = self.db.update(data)
        if (self.resultStatusCode != 200):
            ns.abort(code=self.resultStatusCode, message=self.resultStatusMessage)
        return self.result, self.resultStatusCode
 
    @ns.doc('Exclui uma categorias de usuários')
    @ns.doc(responses={500: 'Internal Error:'})
    def delete(self, id):
        self.resultStatusCode = 200
        self.result = self.db.delete(id)
        if (self.resultStatusCode != 200):
            ns.abort(code=self.resultStatusCode, message=self.resultStatusMessage)
        return self.result, self.resultStatusCode

icityServer.icity_api.add_namespace(ns, path=f'{BaseRoutes.PATH_API}/categories')

# Routes to List Rules
icityServer.icity_app.add_url_rule('/', view_func=CategoriesListRoutes.get, methods=['GET', 'POST'])

api_route = CategoriesRoutes.as_view(f'{BaseRoutes.API_BASE_NAME}_categories')

icityServer.icity_app.add_url_rule('/<int:id>', view_func=api_route, methods=['GET'])
icityServer.icity_app.add_url_rule('/<int:id>', view_func=api_route, methods=['PUT'])
icityServer.icity_app.add_url_rule('/<int:id>', view_func=api_route, methods=['DELETE'])
