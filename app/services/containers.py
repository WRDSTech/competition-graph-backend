from dependency_injector import containers, providers
from app.services.comp_graph_service_impl import CompGraphServiceImpl
from app.repository.comp_graph_repository import CompanyGraphDao
from app.entities.graph_entities import Graph


# def get_mock_repo_object():
#     class MockRepo(CompanyGraphDao):
#         def __init__(self):
#             ...

#         def get_surrouding_by_node(
#             self, node_id, expand_number_of_layers
#         ) -> Graph:
#             # return Graph()
#             return Graph(nodes=[], links=[])

#     return MockRepo()


class ServiceContainer(containers.DeclarativeContainer):
    repo = providers.Resource(CompanyGraphDao)
    comp_graph_service = providers.Singleton(CompGraphServiceImpl, repo=repo)
