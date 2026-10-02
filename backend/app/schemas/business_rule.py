from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class BusinessRuleCreate(BaseModel):
    rule_code: str = Field(
        min_length=3,
        max_length=50
    )

    requirement_code: str

    name: str = Field(
        min_length=3,
        max_length=200
    )

    description: str = Field(
        min_length=5
    )

    rule_expression: str | None = None


class BusinessRuleResponse(BaseModel):
    id: int
    rule_code: str
    requirement_id: int
    name: str
    description: str
    rule_expression: str | None

    model_config = ConfigDict(
        from_attributes=True
    )