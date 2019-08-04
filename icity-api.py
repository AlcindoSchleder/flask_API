# -*- coding: utf-8 -*-
import os
from server import icityServer

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

# Need to import all resources
from workspaces.home.controller import HomeRoutes
from workspaces.admin.categories.controller import CategoriesRoutes

# Register all Blueprint
icityServer.icity_app.register_blueprint(icityServer.icity_bp)
icityServer.icity_app.register_blueprint(icityServer.icity_admin_bp)

# run dev, prod or test
if __name__ == '__main__':
    icityServer.run()
