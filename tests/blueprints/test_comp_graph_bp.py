# TODO: Write test cases just for blueprint,
#  test should cover each possible case
import asyncio
import http

import pytest


@pytest.mark.asyncio
async def test_get_surrounding_by_node_success(client):

    surrounding = await client.get(
        "/api/comp/surrounding?node_id=1&expand_number_of_layers=2"
    )
    assert surrounding.status_code == http.HTTPStatus.OK
    result = await surrounding.get_json()
    assert result is not None


@pytest.mark.asyncio
async def test_get_surrounding_by_node_miss_nodeid(client):

    surrounding = await client.get(
        "/api/comp/surrounding?&expand_number_of_layers=2"
    )
    assert surrounding.status_code == http.HTTPStatus.BAD_REQUEST
    result = await surrounding.get_json()
    assert "node_id can not be empty" == result["message"]


@pytest.mark.asyncio
async def test_get_surrounding_by_node_miss_layers(client):

    surrounding = await client.get(
        "/api/comp/surrounding?node_id=1"
    )
    assert surrounding.status_code == http.HTTPStatus.BAD_REQUEST
    result = await surrounding.get_json()
    assert "expand_number_of_layers can not be empty" == result["message"]


@pytest.mark.asyncio
async def test_get_surrounding_by_node_wrong_type(client):

    surrounding = await client.get(
        "/api/comp/surrounding?node_id=a&expand_number_of_layers=b"
    )
    assert surrounding.status_code == http.HTTPStatus.BAD_REQUEST
    result = await surrounding.get_json()
    print(result)
    assert "Request parameter should be an integer" == result["message"]
