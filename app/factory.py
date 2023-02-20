from quart import Quart
from app.blueprints.comp_graph_bp import comp_graph_controller
from app.container import ApplicationContainer


def create_app() -> Quart:
    app_container = ApplicationContainer()
    app = Quart(__name__)
    app.container = app_container
    # Wire all related packages here, set parameter to "packages" because '__name__' is not main
    app.container.wire(packages=[
        "app",
        "app.repository",
        "app.services",
        "app.blueprints",
    ])
    app.register_blueprint(comp_graph_controller)
    return app
