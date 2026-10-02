from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from app.models.system_component import ComponentType


class SystemComponentCreate(BaseModel):
    component_code: str = Field(
        min_length=3,
        max_length=50
    )

    name: str = Field(
        min_length=2,
        max_length=200
    )

    component_type: ComponentType

    technical_name: str | None = None
    description: str | None = None
    owner: str | None = None


class SystemComponentResponse(BaseModel):
    id: int
    component_code: str
    name: str
    component_type: ComponentType
    technical_name: str | None
    description: str | None
    owner: str | None

    model_config = ConfigDict(
        from_attributes=True
    )