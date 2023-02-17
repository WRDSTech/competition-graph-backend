# TODO: Write test cases just for repository,
#  test should cover each possible case
import pytest

def test_read_entityfile(entity_map):
    assert len(entity_map) == 9
    assert entity_map[1] == '340B'
    assert entity_map[9] == 'AGN.2'

def test_read_relationfile(relationship_map):
    assert len(relationship_map) == 2
    assert relationship_map[0] == 'unknown'
    assert relationship_map[1] == 'product'

def test_read_trainfile(comp_graph_repo):  
    assert len(comp_graph_repo.get_surrounding_node_by_center(2, -1).nodes)== 0
    assert len(comp_graph_repo.get_surrounding_node_by_center(2, 0).nodes)== 1
    assert len(comp_graph_repo.get_surrounding_node_by_center(2, 1).nodes)== 4
    assert len(comp_graph_repo.get_surrounding_node_by_center(2, 2).nodes)== 8
    assert len(comp_graph_repo.get_surrounding_node_by_center(2, 3).nodes)== 9