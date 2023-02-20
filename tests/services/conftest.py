# TODO: Use pytest.fixtures to declare resources for testing, repository layer should be mocked,
#  alone with other resources needed to construct a service object.
import pytest
from app.services.comp_graph_service_impl import CompGraphServiceImpl
from app.repository.comp_graph_repository import CompanyGraphDao
from app.entities.graph_entities import Graph
from app.entities.graph_entities import Entity


@pytest.fixture
def get_mock_repo_object():
    class MockRepo(CompanyGraphDao):
        def __init__(self):
            ...

        def get_surrounding_node_by_center(self, node_id, expand_number_of_layers) -> Graph:
            if node_id == "test_node_id_success" and expand_number_of_layers == "test_expand_number_of_layers":
                test_get_surrouding_by_node_sucess = Graph(
                    nodes=[Entity(id=node_id, name="test_node_id")], links=[])
            else:
                return None

            return test_get_surrouding_by_node_sucess

    return MockRepo()


@pytest.fixture
def mock_comp_graph_service(
        get_mock_repo_object):
    yield CompGraphServiceImpl(get_mock_repo_object)
