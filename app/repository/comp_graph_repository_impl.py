import collections
from operator import truediv

from app.entities.graph_entities import Entity, EntityRelation, Graph
from app.repository.comp_graph_repository import CompanyGraphDao

from neo4j import GraphDatabase


class CompanyGraphDaoImpl(CompanyGraphDao):
    def __init__(self, entity_map, relationship_map, complete_graph):
        self.entity_map = entity_map
        self.relationship_map = relationship_map
        self.complete_graph = complete_graph

        self.driver = GraphDatabase.driver(
            # "bolt://host.docker.internal:7687",
            "bolt://localhost:7687",
            auth=("neo4j", "wrdsdbms")
        )

        import_query = '''CALL gds.graph.exists('graph') YIELD exists AS graphExists
                          WITH graphExists
                          WHERE NOT graphExists
                          CALL gds.graph.project(
                            'graph',
                            "*",
                            "*"
                          )
                          YIELD
                          graphName AS graph, nodeProjection, nodeCount AS nodes, relationshipProjection, relationshipCount AS rels
                          RETURN graph, nodeProjection, nodes, relationshipProjection, rels'''
        with self.driver.session(database="neo4j") as session:
            session.read_transaction(
                lambda tx: tx.run(import_query).data())
            self.driver.close()
    
    def get_subgraph(self, graph) -> Graph:
        g = Graph(nodes=[], links=[])

        node_query = '''MATCH (a)
                        WHERE a.graph="{}"
                        RETURN DISTINCT a;'''.format(graph)
        
        with self.driver.session(database="neo4j") as session:
            results = session.read_transaction(
                lambda tx: tx.run(node_query).data())
            
            self.driver.close()
        
        for record in results:
            # Append nodes
            node = record['a']
            g.nodes.append(Entity(id=node['id'], name=node['name']))
        
        edge_query = '''MATCH (a)-[b]->(c)
                        WHERE a.graph="{}"
                        RETURN DISTINCT b.id AS id, b.category AS category,
                        startNode(b).id AS source, endNode(b).id AS target;'''.format(graph)
        
        with self.driver.session(database="neo4j") as session:
            results = session.read_transaction(
                lambda tx: tx.run(edge_query).data())
            
            self.driver.close()
        
        for record in results:
            # Append links
            g.links.append(EntityRelation(id=record["id"], category=record["category"], source=record["source"], target=record["target"]))
        
        return g

    def get_dow30(self) -> Graph:
        return self.get_subgraph("dow30");
    
    def get_sp500(self) -> Graph:
        return self.get_subgraph("sp500");

    def get_surrounding_node_by_center(self, center_node, dist_to_center, flags) -> Graph:
        if dist_to_center < 0 or center_node not in self.entity_map:
            return Graph(nodes=[], links=[])
        
        types = ['competition', 'product', 'other', 'unknown']
        types_list = [types[i] for i, flag in enumerate(flags) if flag]

        cypher_query = '''MATCH p=(a:Node {{id:\"{}\"}})-[*..{}]->(b:Node)
                          WHERE all(rel in relationships(p) WHERE rel.category IN {})
                          WITH [r IN relationships(p) | [startNode(r), properties(r), endNode(r)]] AS p, b
                          RETURN p, b;'''.format(center_node, dist_to_center, str(types_list))

        g = Graph(nodes=[Entity(id=center_node, name=self.entity_map[center_node])], links=[])

        with self.driver.session(database="neo4j") as session:
            results = session.read_transaction(
                lambda tx, cypher_query=cypher_query: tx.run(cypher_query).data())
            for record in results:
                # Append nodes
                neighbor = record['b']
                g.nodes.append(Entity(id=neighbor['id'], name=neighbor['name']))
                
                # Append links
                properties = record['p']
                for property in properties:
                    g.links.append(EntityRelation(id=property[1]["id"], category=property[1]["category"], 
                                                   source=property[0]["id"], target=property[2]["id"]))

            self.driver.close()
        return g
    
    def get_sample_graph(self) -> Graph:
        cypher_query = '''CALL {
                              MATCH (a)-[r]-(b)
                              WHERE a.graph="sp500"
                              WITH a, COUNT(r) AS degree
                              ORDER BY degree DESC
                              LIMIT 5
                              WITH a, degree
                              ORDER BY rand()
                              LIMIT 1
                              RETURN collect(id(a)) AS sourceIds
                          }
                          UNWIND sourceIds AS sourceId
                          MATCH (source)
                          WHERE id(source) = sourceId
                          CALL gds.bfs.stream('graph', {
                              sourceNode: source,
                              maxDepth: 5
                          })
                          YIELD path
                          RETURN nodes(path) AS nodesInPath, relationships(path) AS relationshipsInPath'''
        
        g = Graph(nodes=[], links=[])

        with self.driver.session(database="neo4j") as session:
            results = session.read_transaction(
                lambda tx: tx.run(cypher_query).data())
            for record in results:
                # Append nodes
                for node in record['nodesInPath']:
                    g.nodes.append(Entity(id=node['id'], name=node['name']))
                
                # Append links
                for link in record['relationshipsInPath']:
                    g.links.append(EntityRelation(id=0, category="null", source=link[0]["id"], target=link[2]["id"]))

            self.driver.close()
        
        return g

    def _process_current_layer(self, entity_queue, g, visited_entities):
        num_of_items_curr_layer = len(entity_queue)
        for _ in range(num_of_items_curr_layer):
            curr_node = entity_queue.popleft()
            self._process_neighbor(entity_queue, g, visited_entities, curr_node)

    def _process_neighbor(self, entity_queue, g, visited_entities, curr_node):
        for adjacent_node, relation_type in self.complete_graph[curr_node]:

            if adjacent_node not in visited_entities:
                visited_entities.add(adjacent_node)
                g.nodes.append(Entity(id=adjacent_node, name=self.entity_map[adjacent_node]))
                g.links.append(
                    EntityRelation(id=relation_type, category=self.relationship_map[relation_type], source=curr_node,
                                   target=adjacent_node))
                entity_queue.append(adjacent_node)
