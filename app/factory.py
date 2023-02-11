from quart import Quart

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
    # TODO: Register blueprint here

    return app
