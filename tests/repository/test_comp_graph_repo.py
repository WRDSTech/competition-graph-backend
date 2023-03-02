from app.entities.graph_entities import Entity, EntityRelation


def test_get_surrounding_node_by_center(comp_graph_repo):
    assert len(comp_graph_repo.get_surrounding_node_by_center(2, -1).nodes) == 0
    assert len(comp_graph_repo.get_surrounding_node_by_center(2, 0).nodes) == 1
    assert len(comp_graph_repo.get_surrounding_node_by_center(2, 1).nodes) == 2
    assert len(comp_graph_repo.get_surrounding_node_by_center(2, 2).nodes) == 3
    assert len(comp_graph_repo.get_surrounding_node_by_center(2, 3).nodes) == 3
    assert len(comp_graph_repo.get_surrounding_node_by_center(6, 3).nodes) == 4
    assert len(comp_graph_repo.get_surrounding_node_by_center(9, 5).nodes) == 2
    assert len(comp_graph_repo.get_surrounding_node_by_center(10, 1).nodes) == 2
    assert len(comp_graph_repo.get_surrounding_node_by_center(11, 1).nodes) == 0

    partial_graph = comp_graph_repo.get_surrounding_node_by_center(6, 3)
    assert len(partial_graph.links) == 3
    assert len(partial_graph.nodes) == 4
    assert Entity(id=8, name="Disney") in partial_graph.nodes
    assert Entity(id=9, name="Standard Chartered Bank") not in partial_graph.nodes
    assert EntityRelation(id=3, category="product", source=6, target=5) in partial_graph.links
    assert EntityRelation(id=3, category="product", source=5, target=6) not in partial_graph.links
    assert EntityRelation(id=5, category="competition", source=5, target=7) in partial_graph.links
    assert EntityRelation(id=5, category="competition", source=7, target=5) not in partial_graph.links
