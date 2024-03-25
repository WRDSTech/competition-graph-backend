import abc
from app.entities.graph_entities import Graph


class CompGraphService(abc.ABC):    
    @abc.abstractmethod
    async def get_dow30(self) -> Graph:
        raise NotImplementedError
    
    @abc.abstractmethod
    async def get_sp500(self) -> Graph:
        raise NotImplementedError
    
    @abc.abstractmethod
    async def get_sample(self) -> Graph:
        raise NotImplementedError
    
    @abc.abstractmethod
    async def get_surrounding_by_node(self, node_id: int, expand_number_of_layers: int, flags: list) -> Graph:
        raise NotImplementedError