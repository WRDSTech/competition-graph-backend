import collections
import json
from typing import Dict, Tuple, List

from app.repository.comp_graph_repository_impl import CompanyGraphDaoImpl
from dependency_injector import containers, providers


class InvalidFileTypeException(Exception):
    pass


class InvalidCSVRowException(Exception):
    pass


class MapBundle:
    def __init__(self, entity_map, relationship_map, complete_graph):
        self.entity_map = entity_map
        self.relationship_map = relationship_map
        self.complete_graph = complete_graph


class EmptyJsonFileException(Exception):
    pass


def _read_graph_from_json_file(path: str,
                               start_eid: int,
                               entity2id: Dict[str, int],
                               entity_map: Dict[int, str],
                               relation2id: Dict[str, int],
                               graph: collections.defaultdict[int, List[Tuple[int, int]]]) -> int:
    if not path.endswith(".json"):
        raise InvalidFileTypeException("Filetype must be json.")

    with open(path, encoding="utf8") as f:
        partial_graph: Dict[str, dict] = json.load(f)
        if not partial_graph:
            raise EmptyJsonFileException("the file is empty!")
        eid = start_eid

        for _, edge in partial_graph.items():
            source_e = edge["entity_1"]
            target_e = edge["entity_2"]
            relation = edge["relation"]

            # source/target entity is empty
            if not source_e or not target_e:
                continue

            if source_e not in entity2id:
                entity2id[source_e] = eid
                entity_map[eid] = source_e
                eid += 1
            if target_e not in entity2id:
                entity2id[target_e] = eid
                entity_map[eid] = target_e
                eid += 1

            graph[entity2id[source_e]].append((entity2id[target_e], relation2id[relation]))
            graph[entity2id[target_e]].append((entity2id[source_e], relation2id[relation]))
    return eid


def load_json_files(*files: str) -> MapBundle:
    relation2id = {
        "unknown": 0,
        "product": 1,
        "competition": 2,
    }
    relationship_map = {
        0: "unknown",
        1: "product",
        2: "competition",
    }
    complete_graph = collections.defaultdict(list)
    entity2id = collections.defaultdict(int)
    entity_map = collections.defaultdict(str)
    eid = 0
    for path in files:
        eid = _read_graph_from_json_file(
            path,
            eid,
            entity2id,
            entity_map,
            relation2id,
            complete_graph,
        )
    return MapBundle(entity_map, relationship_map, complete_graph)


class RepositoryContainer(containers.DeclarativeContainer):
    map_bundle = load_json_files("app/data/dow30_relation.json", "app/data/sp500_relation.json")

    comp_graph_repo = providers.Singleton(
        CompanyGraphDaoImpl,
        entity_map=map_bundle.entity_map,
        relationship_map=map_bundle.relationship_map,
        complete_graph=map_bundle.complete_graph,
    )
