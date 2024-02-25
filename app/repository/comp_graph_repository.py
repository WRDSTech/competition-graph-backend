import abc
from abc import abstractmethod

from app.entities.graph_entities import Graph


class CompanyGraphDao(abc.ABC):
    @abstractmethod
    def get_dow30(self) -> Graph:
        raise NotImplementedError
    
    @abstractmethod
    def get_sp500(self) -> Graph:
        raise NotImplementedError
    
    @abstractmethod
    def get_sample_graph(self) -> Graph:
        raise NotImplementedError
    
    @abstractmethod
    def get_surrounding_node_by_center(self, center_node, dist_to_center) -> Graph:
        raise NotImplementedError