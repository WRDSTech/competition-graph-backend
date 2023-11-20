from neo4j import GraphDatabase

from app.services.comp_graph_service import CompGraphService
from app.repository.comp_graph_repository import CompanyGraphDao
from app.entities.graph_entities import Graph
from settings import NEO4J_GRAPH_DB_URI, NEO4J_GRAPH_DB_USER, NEO4J_GRAPH_DB_PASSWORD


class CompGraphServiceImpl(CompGraphService):
    def __init__(self, repo: CompanyGraphDao) -> None:
        self.repo = repo

    async def get_surrounding_by_node(self, node_id, expand_number_of_layers) -> Graph:
        surrounding = self.repo.get_surrounding_node_by_center(
            node_id, expand_number_of_layers
        )
        return surrounding

    async def bfs(self, node_id, expand_number_of_layers, flags):
        uri = NEO4J_GRAPH_DB_URI
        user = NEO4J_GRAPH_DB_USER
        password = NEO4J_GRAPH_DB_PASSWORD
        driver = GraphDatabase.driver(uri, auth=(user, password))

        types = ['competition', 'product', 'other', 'unknown']

        types_str = ''
        for i in range(len(flags)):
            if flags[i]:
                types_str += types[i] + '|'
        types_str = types_str[:-1]

        query = '''
        MATCH (source:Node{id: '$node_id'})
        CALL apoc.path.subgraphAll(source, {
            relationshipFilter: '$types',
            minLevel: 0,
            maxLevel: $depth
        })
        YIELD nodes, relationships
        RETURN nodes, relationships; 
        '''

        query = query.replace('$node_id', str(node_id))
        query = query.replace('$depth', str(expand_number_of_layers))
        query = query.replace('$types', types_str)

        with driver.session() as session:
            results = session.read_transaction(
                lambda tx: tx.run(query).data())[0]

        driver.close()

        # format data to same structure as the original implementation
        results['links'] = results.pop('relationships')
        for i in range(len(results['links'])):
            lis = results['links'][i]
            results['links'][i] = {'category': lis[1], "source": lis[0]["id"], "target": lis[2]["id"]}

        return results
