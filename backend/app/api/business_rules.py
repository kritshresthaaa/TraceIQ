from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.business_rule import BusinessRule
from app.models.requirement import Requirement
from app.schemas.business_rule import BusinessRuleCreate
from app.schemas.business_rule import BusinessRuleResponse


router = APIRouter(
    prefix="/business-rules",
    tags=["Business Rules"]
)


@router.post(
    "",
    response_model=BusinessRuleResponse,
    status_code=201
)
def create_business_rule(
    request: BusinessRuleCreate,
    db: Session = Depends(get_db)
):

    requirement_statement = select(
        Requirement
    ).where(
        Requirement.requirement_code
        == request.requirement_code
    )

    requirement = db.scalar(
        requirement_statement
    )

    if requirement is None:
        raise HTTPException(
            status_code=404,
            detail="Requirement not found."
        )

    business_rule = BusinessRule(
        rule_code=request.rule_code,
        requirement_id=requirement.id,
        name=request.name,
        description=request.description,
        rule_expression=request.rule_expression
    )

    db.add(business_rule)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Business rule code already exists."
        )

    db.refresh(business_rule)

    return business_rule