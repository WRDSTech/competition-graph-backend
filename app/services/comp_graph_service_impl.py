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
    
    async def get_sample(self) -> Graph:
        return self.repo.get_sample_graph()
