from pydantic import BaseModel, Field
from pydantic.class_validators import Optional


class GetSurroundingByNodeRequest(BaseModel):
    node_id: Optional[int] = Field(None, description="The center of the displayed graph")
    expand_number_of_layers: Optional[int] = Field(None, description="Number of neighboring layers to include in the graph")
