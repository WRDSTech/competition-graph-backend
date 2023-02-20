# TODO: Write test cases just for service,
#  test should cover each possible case
import asyncio
import pytest
from app.entities.graph_entities import Graph


@pytest.mark.asyncio
async def test_get_surrouding_by_node_success(mock_comp_graph_service):
    surrouding: Graph = await mock_comp_graph_service.get_surrouding_by_node("test_node_id_success", "test_expand_number_of_layers")
    assert surrouding.nodes[0].id is "test_node_id_success"


@pytest.mark.asyncio
async def test_get_surrouding_by_node_none(mock_comp_graph_service):
    surrouding: Graph = await mock_comp_graph_service.get_surrouding_by_node("test_node_id_fail", "test_expand_number_of_layers")
    assert surrouding is None
