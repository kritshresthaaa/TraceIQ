from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from app.models.change_request import ChangeRequestStatus
from app.schemas.business_rule import BusinessRuleResponse
from app.schemas.system_component import SystemComponentResponse


class ChangeRequestCreate(BaseModel):
    change_code: str = Field(
        min_length=3,
        max_length=50
    )

    requirement_code: str

    title: str = Field(
        min_length=3,
        max_length=200
    )

    current_state: str = Field(
        min_length=3
    )

    proposed_state: str = Field(
        min_length=3
    )

    reason: str | None = None

    status: ChangeRequestStatus = (
        ChangeRequestStatus.DRAFT
    )

    requested_by: str | None = None


class ChangeRequestResponse(BaseModel):
    id: int

    change_code: str
    requirement_id: int

    title: str

    current_state: str
    proposed_state: str
    reason: str | None

    status: ChangeRequestStatus
    requested_by: str | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class ChangeImpactResponse(BaseModel):
    change_code: str
    change_title: str

    requirement_code: str
    requirement_title: str

    current_state: str
    proposed_state: str

    business_rules: list[BusinessRuleResponse]

    direct_impact: list[SystemComponentResponse]

    downstream_impact: list[SystemComponentResponse]

    total_impacted_components: int

    impacted_by_type: dict[str, int]

    affected_owners: list[str]