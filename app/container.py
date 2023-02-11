"""Application Level Container"""

from dependency_injector import containers, providers

from app.blueprints.containers import CompGraphBpContainer
from app.services.containers import ServiceContainer
from app.repository.containers import RepositoryContainer


class ApplicationContainer(containers.DeclarativeContainer):
    # TODO: Add dependencies for service and blueprint here
    comp_graph_repo = providers.Container(
        RepositoryContainer,
    )
    comp_graph_svc = providers.Container(
        ServiceContainer,
    )
    comp_graph_bp = providers.Container(
        CompGraphBpContainer,
    )
