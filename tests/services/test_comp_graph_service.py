# TODO: Write test cases just for service,
#  test should cover each possible case
import asyncio
import pytest
from app.entities.graph_entities import Graph
from unittest.mock import patch, MagicMock


@pytest.mark.asyncio
async def test_get_surrounding_by_node_success(mock_comp_graph_service):
    surrounding: Graph = await mock_comp_graph_service.get_surrounding_by_node("test_node_id_success",
                                                                               "test_expand_number_of_layers")
    assert surrounding.nodes[0].id is "test_node_id_success"


@pytest.mark.asyncio
async def test_get_surrounding_by_node_none(mock_comp_graph_service):
    surrounding: Graph = await mock_comp_graph_service.get_surrounding_by_node("test_node_id_fail",
                                                                               "test_expand_number_of_layers")
    assert surrounding is None


@pytest.mark.asyncio
async def test_bfs_success(mock_comp_graph_service):
    with patch('neo4j.GraphDatabase.driver') as mock_driver:
        mock_session = MagicMock()
        mock_driver.return_value.session.return_value.__enter__.return_value = mock_session
        mock_session.run.return_value.data.return_value = [{
            'nodes': [{"id": "175", "name": "NKE"}],  # Your mocked nodes data
            'links': [{"category": "competition", "source": "175", "target": "178"}]  # Your mocked relationships data
        }]

        result = await mock_comp_graph_service.bfs("test_node_id_success", "test_expand_number_of_layers",
                                                   [True, False, True, False])

        assert result is not None
        assert result['nodes'] is not None
        assert result['links'] is not None

