from abc import abstractmethod

from app.entities.graph_entities import Graph


class CompanyGraphDao():
    @abstractmethod
    def get_surrounding_node_by_center(self, center_node, dist_to_center) -> Graph:
        pass
