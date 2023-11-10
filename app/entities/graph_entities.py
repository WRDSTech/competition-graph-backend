from typing import List
from pydantic import BaseModel, Field


class Entity(BaseModel):
    id: str = Field(..., description="Entity ID")
    name: str = Field(..., description="Name of Entity")


class EntityRelation(BaseModel):
    id: str = Field(..., description="Relation ID")
    category: str = Field(..., description="Category of Relation")
    source: str = Field(..., description="The source of link")
    target: str = Field(..., description="The target of link")


class Graph(BaseModel):
    nodes: List[Entity] = Field(..., description="Collection of Entities")
    links: List[EntityRelation] = Field(..., description="Relations of Entities")
