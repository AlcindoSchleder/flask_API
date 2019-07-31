# -*- coding: utf-8 -*-
from flask_restplus import Namespace
from server import icityServer
from workspaces.home import BaseRoutes

ns = Namespace(BaseRoutes.API_BASE_NAME, description='Print Hello Word')

@ns.route('/')
@ns.doc('Imprime o HelloWord na tela')
class HomeRoutes(BaseRoutes):

    def __init__(self):
        super(HomeRoutes, self).__init__()

    @ns.doc('envia mensagem hello word')
    def get(self):
        return "<h1>Home page with Blueprint!</h1>"

icityServer.icity_api.add_namespace(ns, path=BaseRoutes.PATH_API)

api_functions = HomeRoutes.as_view(BaseRoutes.API_BASE_NAME)
icityServer.icity_app.add_url_rule('/', view_func=api_functions, methods=['GET'])
