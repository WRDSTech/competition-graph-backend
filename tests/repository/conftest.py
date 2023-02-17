# TODO: Use pytest.fixtures to declare resources for testing, actual db/data should be mocked,
#  alone with other resources needed to construct a repository object.
import collections
import pytest
from app.repository.comp_graph_repository_impl import CompanyGraphDaoImpl
from settings import TEST_ENTITY_FILE_LOCATION, TEST_RELATION_FILE_LOCATION, TEST_TRAIN_FILE_LOCATION

@pytest.fixture
def entity_map():
    entity_map = {}                     
    
    with open(TEST_ENTITY_FILE_LOCATION,"r") as f:
        num_of_items = f.readline()                   
        for line in f:                     
            entity = line.replace(' \n', '').split('     ')[0]
            entity_id = int(line.replace(' \n', '').split('     ')[1])
            entity_map[entity_id] = entity
            
    return entity_map

@pytest.fixture
def relationship_map():
    relationship_map = {}
    
    with open(TEST_RELATION_FILE_LOCATION,"r") as f:
        num_of_items = f.readline()    
        for line in f:      
            relation = line.replace(' \n', '').split('     ')[0]
            relation_id = int(line.replace(' \n', '').split('     ')[1])
            relationship_map[relation_id] = relation
            
    return relationship_map

@pytest.fixture
def complete_graph(entity_map):
    complete_graph = {}
    HalfEdge = collections.namedtuple("HalfEdge", "dest_id relation_id")
    
    for eid in entity_map.keys():
        complete_graph[eid] = []
        
    with open(TEST_TRAIN_FILE_LOCATION,"r") as f:
        num_of_items = f.readline()    
        for line in f:      
            print(line)
            entity1_id, entity2_id, relation_id =  list(map(int, line.replace(' \n', '').split('     ')))
            complete_graph[entity1_id].append(HalfEdge(entity2_id, relation_id))
            complete_graph[entity2_id].append(HalfEdge(entity1_id, relation_id))

    return complete_graph


@pytest.fixture
def comp_graph_repo(entity_map, relationship_map, complete_graph):
    yield CompanyGraphDaoImpl(entity_map, relationship_map, complete_graph)
