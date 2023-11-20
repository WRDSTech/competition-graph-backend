import abc

from app.entities.graph_entities import Graph


class CompGraphService(abc.ABC):
    @abc.abstractmethod
    async def get_surrounding_by_node(self, node_id: int, expand_number_of_layers: int) -> Graph:
        raise NotImplementedError

    @abc.abstractmethod
    async def bfs(self, node_id: int, expand_number_of_layers: int, flags: list):
        raise NotImplementedError
