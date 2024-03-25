from pydantic import BaseModel, Field
from pydantic.class_validators import Optional


class GetSurroundingByNodeRequest(BaseModel):
    node_id: Optional[int] = Field(None, description="The center of the displayed graph")
    expand_number_of_layers: Optional[int] = Field(None, description="Number of neighboring layers to include in the graph")
    competition: Optional[bool] = Field(True, description="If to include competition relationships in the graph")
    product: Optional[bool] = Field(True, description="If to include product relationships in the graph")
    other: Optional[bool] = Field(True, description="If to include other relationships in the graph")
    unknown: Optional[bool] = Field(True, description="If to include unknown relationships in the graph")
