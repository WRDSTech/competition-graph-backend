import pytest
from app.repository.comp_graph_repository_impl import CompanyGraphDaoImpl
from app.repository.container import load_json_files


@pytest.fixture
def map_bundle():
    bundle = load_json_files("tests/data/test_relation1.json", "tests/data/test_relation2.json")
    return bundle


@pytest.fixture
def comp_graph_repo(map_bundle):
    yield CompanyGraphDaoImpl(
        map_bundle.entity_map,
        map_bundle.relationship_map,
        map_bundle.complete_graph,
    )
