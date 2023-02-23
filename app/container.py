"""Application Level Container"""

from dependency_injector import containers, providers

from app.blueprints.container import CompGraphBpContainer
from app.services.container import ServiceContainer
from app.repository.container import RepositoryContainer


class ApplicationContainer(containers.DeclarativeContainer):
    comp_graph_repo = providers.Container(
        RepositoryContainer,
    )
    comp_graph_svc = providers.Container(
        ServiceContainer,
        repo=comp_graph_repo.comp_graph_repo
    )
    comp_graph_bp = providers.Container(
        CompGraphBpContainer,
        comp_graph_svc=comp_graph_svc.comp_graph_service
    )
