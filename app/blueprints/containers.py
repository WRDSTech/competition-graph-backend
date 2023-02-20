from dependency_injector import containers, providers
from app.services.comp_graph_service import CompGraphService


class CompGraphBpContainer(containers.DeclarativeContainer):
    comp_graph_svc = providers.Dependency(instance_of=CompGraphService)
