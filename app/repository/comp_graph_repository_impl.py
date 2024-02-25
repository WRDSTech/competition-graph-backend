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
                          graphName AS graph, nodeProjection, nodeCount AS nodes, relationshipProjection, relationshipCount AS rels'''
        with self.driver.session(database="neo4j") as session:
            session.read_transaction(
                lambda tx, cypher_query=import_query: tx.run(cypher_query).data())
            self.driver.close()

    def get_dow30(self) -> Graph:
        cypher_query = '''MATCH (a)-[b]->(c)
                          WHERE a.graph="dow30"
                          RETURN a, b.id AS id, b.category AS category, startNode(b).id AS source, endNode(b).id AS target'''
        print(cypher_query)

        g = Graph(nodes=[], links=[])

        with self.driver.session(database="neo4j") as session:
            results = session.read_transaction(
                lambda tx, cypher_query=cypher_query: tx.run(cypher_query).data())
            for record in results:
                print(record)
                # Append nodes
                node = record['a']
                g.nodes.append(Entity(id=node['id'], name=node['name']))
                # Append links
                # print(record['r'])
                
                g.links.append(EntityRelation(id=record["id"], category=record["category"], 
                                                source=record["source"], target=record["target"]))

            self.driver.close()
        print(g)
        return g
    
    def get_sp500(self) -> Graph:
        cypher_query = '''MATCH (a)-[b]->(c)
                          WHERE a.graph="sp500"
                          RETURN a, b.id AS id, b.category AS category, startNode(b).id AS source, endNode(b).id AS target'''
        print(cypher_query)

        g = Graph(nodes=[], links=[])

        with self.driver.session(database="neo4j") as session:
            results = session.read_transaction(
                lambda tx, cypher_query=cypher_query: tx.run(cypher_query).data())
            for record in results:
                print(record)
                # Append nodes
                node = record['a']
                g.nodes.append(Entity(id=node['id'], name=node['name']))
                # Append links
                # print(record['r'])
                
                g.links.append(EntityRelation(id=record["id"], category=record["category"], 
                                                source=record["source"], target=record["target"]))

            self.driver.close()
        print(g)
        return g

    def get_surrounding_node_by_center(self, center_node, dist_to_center) -> Graph:
        if dist_to_center < 0 or center_node not in self.entity_map:
            return Graph(nodes=[], links=[])

        cypher_query = '''MATCH p=(a:Node {{id:\"{}\"}})-[*..{}]->(b:Node)
                          WITH [r IN relationships(p) | [startNode(r), properties(r), endNode(r)]] AS p, b
                          RETURN p, b'''.format(center_node, dist_to_center)
        print(cypher_query)

        g = Graph(nodes=[Entity(id=center_node, name=self.entity_map[center_node])], links=[])

        with self.driver.session(database="neo4j") as session:
            results = session.read_transaction(
                lambda tx, cypher_query=cypher_query: tx.run(cypher_query).data())
            for record in results:
                print(record)
                # Append nodes
                neighbor = record['b']
                g.nodes.append(Entity(id=neighbor['id'], name=neighbor['name']))
                
                # Append links
                properties = record['p']
                for property in properties:
                    g.links.append(EntityRelation(id=property[1]["id"], category=property[1]["category"], 
                                                   source=property[0]["id"], target=property[2]["id"]))

            self.driver.close()
        print(g)
        return g
    
    def get_sample_graph(self) -> Graph:
        
        
        cypher_query = '''CALL {
                              MATCH (a)-[r]-(b)
                              WITH a, COUNT(r) AS degree
                              ORDER BY degree DESC
                              LIMIT 5
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
        
        print(cypher_query)
        g = Graph(nodes=[], links=[])

        with self.driver.session(database="neo4j") as session:
            results = session.read_transaction(
                lambda tx, cypher_query=cypher_query: tx.run(cypher_query).data())
            for record in results:
                print(record)
                # Append nodes
                for node in record['nodesInPath']:
                    g.nodes.append(Entity(id=node['id'], name=node['name']))
                
                # Append links
                for link in record['relationshipsInPath']:
                    print(link)
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
