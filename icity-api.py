# -*- coding: utf-8 -*-
from server import icityServer

# Need to import all resources
from workspaces.home.controller import HomeRoutes

# so that they will be registered into the server 
icityServer.icity_app.register_blueprint(icityServer.icity_bp)
# print("------> EndPoints: ", *icityServer.icity_app.url_map._rules, sep='\n')

# run dev, prod or test
if __name__ == '__main__':
    icityServer.run()
