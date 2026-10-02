from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from app.models.requirement import RequirementPriority
from app.models.requirement import RequirementStatus


class RequirementCreate(BaseModel):
    requirement_code: str = Field(
        min_length=3,
        max_length=50
    )

    title: str = Field(
        min_length=3,
        max_length=200
    )

    description: str = Field(
        min_length=5
    )

    status: RequirementStatus = RequirementStatus.DRAFT

    priority: RequirementPriority = RequirementPriority.MEDIUM

    owner: str | None = None


class RequirementResponse(BaseModel):
    id: int

    requirement_code: str
    title: str
    description: str

    status: RequirementStatus
    priority: RequirementPriority

    owner: str | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )