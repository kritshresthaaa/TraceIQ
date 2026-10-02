from pydantic import BaseModel

from app.models.dependency import DependencyType


class DependencyCreate(BaseModel):
    source_component_code: str
    target_component_code: str
    dependency_type: DependencyType


class DependencyResponse(BaseModel):
    id: int
    source_component_id: int
    target_component_id: int
    dependency_type: DependencyType

    model_config = {
        "from_attributes": True
    }