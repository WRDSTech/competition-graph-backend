from neo4j import GraphDatabase

from app.services.comp_graph_service import CompGraphService
from app.repository.comp_graph_repository import CompanyGraphDao
from app.entities.graph_entities import Graph


class CompGraphServiceImpl(CompGraphService):
    def __init__(self, repo: CompanyGraphDao) -> None:
        self.repo = repo

    async def get_surrounding_by_node(self, node_id, expand_number_of_layers) -> Graph:
        surrounding = self.repo.get_surrounding_node_by_center(
            node_id, expand_number_of_layers
        )
        return surrounding

    async def bfs(self, node_id, expand_number_of_layers, flags):
        uri = 'bolt://172.17.0.2:7687'
        user = 'neo4j'
        password = 'graph2023'
        driver = GraphDatabase.driver(uri, auth=(user, password))

        # [abandoned] bfs get nodes then query edges? if so, get nodeIds instead of path
        # [abandoned] problem: no 'unknown' relationType exists in dow30 graph, including it in types will cause error
        # bfs_query = """
        #             MATCH (source:Node{id:'$node_id'})
        #             CALL gds.bfs.stream('dow30', {
        #               sourceNode: source,
        #               maxDepth: $depth,
        #               relationshipTypes: $types
        #             })
        #             YIELD path
        #             CALL apoc.graph.fromPaths([path],'test', {})
        #             YIELD graph AS g
        #             RETURN g.nodes
        #             """

        # bfs_query = bfs_query.replace('$node_id', str(node_id))
        # bfs_query = bfs_query.replace('$depth', str(expand_number_of_layers))
        # bfs_query = bfs_query.replace('$types', str(types))

        # with driver.session() as session:
        #     results = session.read_transaction(
        #         lambda tx: tx.run(bfs_query).data())

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
                lambda tx: tx.run(query).data())

        driver.close()
        return results
