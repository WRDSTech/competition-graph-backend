import collections
from operator import truediv

from app.entities.graph_entities import Entity, EntityRelation, Graph
from app.repository.comp_graph_repository import CompanyGraphDao


class CompanyGraphDaoImpl(CompanyGraphDao):
    def __init__(self, entity_map, relationship_map, complete_graph):
        self.entity_map = entity_map
        self.relationship_map = relationship_map
        self.complete_graph = complete_graph

    def get_surrounding_node_by_center(self, center_node, dist_to_center) -> Graph:
        if dist_to_center < 0 or center_node not in self.entity_map:
            return Graph(nodes=[], links=[])
        entity_queue = collections.deque([center_node])
        g = Graph(nodes=[Entity(id=center_node, name=self.entity_map[center_node])], links=[])
        visited_entities = {center_node}
        curr_layer = 0

        while len(entity_queue) > 0:
            if curr_layer >= dist_to_center:
                break
            self._process_current_layer(entity_queue, g, visited_entities)
            curr_layer += 1

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
