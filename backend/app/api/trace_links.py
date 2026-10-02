from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.business_rule import BusinessRule
from app.models.system_component import SystemComponent
from app.models.trace_link import TraceLink
from app.schemas.trace_link import TraceLinkCreate
from app.schemas.trace_link import TraceLinkResponse


router = APIRouter(
    prefix="/trace-links",
    tags=["Traceability"]
)


@router.post(
    "",
    response_model=TraceLinkResponse,
    status_code=201
)
def create_trace_link(
    request: TraceLinkCreate,
    db: Session = Depends(get_db)
):

    rule = db.scalar(
        select(BusinessRule).where(
            BusinessRule.rule_code
            == request.business_rule_code
        )
    )

    if rule is None:
        raise HTTPException(
            status_code=404,
            detail="Business rule not found."
        )

    component = db.scalar(
        select(SystemComponent).where(
            SystemComponent.component_code
            == request.component_code
        )
    )

    if component is None:
        raise HTTPException(
            status_code=404,
            detail="System component not found."
        )

    trace_link = TraceLink(
        business_rule_id=rule.id,
        component_id=component.id,
        relationship_type=request.relationship_type
    )

    db.add(trace_link)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Trace link already exists."
        )

    db.refresh(trace_link)

    return trace_link