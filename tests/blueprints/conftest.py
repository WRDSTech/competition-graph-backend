# TODO: Use pytest.fixtures to declare resources for testing, services should be mocked
#  for blueprint, you may want to init a mock client to test the response for each case
import pytest
from app.entities.graph_entities import Graph, Entity
from app.factory import create_app
from app.repository.comp_graph_repository import CompanyGraphDao
from app.services.comp_graph_service import CompGraphService


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture
def comp_graph_mock_svc():
    yield MockCompGraphSvc()


class MockCompGraphSvc(CompGraphService):
    def __init__(self) -> None:
        ...

    async def get_surrounding_by_node(self, node_id, expand_number_of_layers) -> Graph:
        test_surrounding = Graph(
            nodes=[Entity(id="!!!!!====!!!!", name="!!!!!====")], links=[])

        return test_surrounding
