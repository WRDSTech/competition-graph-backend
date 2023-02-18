import collections
from app.repository.comp_graph_repository_impl import CompanyGraphDaoImpl
from dependency_injector import containers, providers
from settings import ENTITY_FILE_LOCATION, RELATION_FILE_LOCATION, TRAIN_FILE_LOCATION

def read_entityfile(self) -> dict[int, str]:        
    entity_map = {}                     
    with open(ENTITY_FILE_LOCATION,"r") as f:
        num_of_items = f.readline()
                           
        for line in f:                     
            entity = line.replace(' \n', '').split('     ')[0]
            entity_id = int(line.replace(' \n', '').split('     ')[1])
            entity_map[entity_id] = entity

    return entity_map

def read_relationfile(self) -> dict[int, str]:
    relationship_map = {}
    with open(RELATION_FILE_LOCATION,"r") as f:
        num_of_items = f.readline()  
          
        for line in f:      
            relation = line.replace(' \n', '').split('     ')[0]
            relation_id = int(line.replace(' \n', '').split('     ')[1])
            relationship_map[relation_id] = relation
            
    return relationship_map

def read_trainfile(self, entity_map):
    complete_graph = {}
    HalfEdge = collections.namedtuple("HalfEdge", "dest_id relation_id")
    
    for eid in entity_map.keys():
        complete_graph[eid] = []
        
    with open(TRAIN_FILE_LOCATION,"r") as f:
        num_of_items = f.readline()    
        for line in f:      
            entity1_id, entity2_id, relation_id =  list(map(int, line.replace(' \n', '').split('     ')))
            complete_graph[entity1_id].append(HalfEdge(entity2_id, relation_id))
            complete_graph[entity2_id].append(HalfEdge(entity1_id, relation_id))
            
    return complete_graph
    
class RepositoryContainer(containers.DeclarativeContainer):
    entity_map = providers.Resource(read_entityfile)
    relationship_map = providers.Resource(read_relationfile)
    complete_graph = providers.Resource(read_trainfile)

    comp_graph_repo = providers.Singleton(
        CompanyGraphDaoImpl,
        entity_map = entity_map, 
        relationship_map = relationship_map, 
        complete_graph = complete_graph
    )
