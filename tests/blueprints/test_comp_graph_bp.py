# TODO: Write test cases just for blueprint,
#  test should cover each possible case
import asyncio
import pytest


@pytest.mark.asyncio
async def test_get_surrouding_by_node_success(comp_graph_mock_svc, client):

    surrounding = await client.get(
        "/api/comp/surrouding?node_id=1&expand_number_of_layers=2"
    )

    result = await surrounding.data
    result = result.decode("utf-8")

    assert result is not None


@pytest.mark.asyncio
async def test_get_surrouding_by_node_miss_nodeid(comp_graph_mock_svc, client):

    surrounding = await client.get(
        "/api/comp/surrouding?expand_number_of_layers=2"
    )
    assert surrounding.status_code == 400


@pytest.mark.asyncio
async def test_get_surrouding_by_node_miss_layers(comp_graph_mock_svc, client):

    surrounding = await client.get(
        "/api/comp/surrouding?node_id=1"
    )
    assert surrounding.status_code == 400
