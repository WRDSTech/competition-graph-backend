import abc
from app.entities.graph_entities import Graph


class CompGraphService(abc.ABC):
    @abc.abstractclassmethod
    async def get_surrouding_by_node(self, node_id, expand_number_of_layers) -> Graph:
        raise NotImplementedError
