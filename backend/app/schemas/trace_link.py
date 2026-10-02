from pydantic import BaseModel

from app.models.trace_link import TraceRelationship


class TraceLinkCreate(BaseModel):
    business_rule_code: str
    component_code: str

    relationship_type: TraceRelationship = (
        TraceRelationship.IMPLEMENTED_BY
    )


class TraceLinkResponse(BaseModel):
    id: int
    business_rule_id: int
    component_id: int
    relationship_type: TraceRelationship

    model_config = {
        "from_attributes": True
    }