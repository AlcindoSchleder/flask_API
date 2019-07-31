# -*- coding: utf-8 -*-
from server import icityServer

# Need to import all resources
from workspaces.home.controller import HomeRoutes

# Register all Blueprint
icityServer.icity_app.register_blueprint(icityServer.icity_bp)

# run dev, prod or test
if __name__ == '__main__':
    icityServer.run()
