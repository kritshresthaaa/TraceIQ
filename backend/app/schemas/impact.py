from pydantic import BaseModel

from app.schemas.business_rule import BusinessRuleResponse
from app.schemas.system_component import SystemComponentResponse


class ImpactAnalysisResponse(BaseModel):
    requirement_code: str
    requirement_title: str

    business_rules: list[BusinessRuleResponse]

    starting_components: list[SystemComponentResponse]

    impacted_components: list[SystemComponentResponse]

    total_impacted_components: int