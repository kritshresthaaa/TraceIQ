from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.change_request import ChangeRequest
from app.models.requirement import Requirement

from app.schemas.change_request import ChangeRequestCreate
from app.schemas.change_request import ChangeRequestResponse
from app.schemas.change_request import ChangeImpactResponse

from app.services.impact_analysis import get_requirement_impact


router = APIRouter(
    prefix="/change-requests",
    tags=["Change Requests"]
)
@router.post(
    "",
    response_model=ChangeRequestResponse,
    status_code=201
)
def create_change_request(
    request: ChangeRequestCreate,
    db: Session = Depends(get_db)
):

    requirement = db.scalar(
        select(Requirement).where(
            Requirement.requirement_code
            == request.requirement_code
        )
    )

    if requirement is None:
        raise HTTPException(
            status_code=404,
            detail="Requirement not found."
        )

    change_request = ChangeRequest(
        change_code=request.change_code,
        requirement_id=requirement.id,
        title=request.title,
        current_state=request.current_state,
        proposed_state=request.proposed_state,
        reason=request.reason,
        status=request.status,
        requested_by=request.requested_by
    )

    db.add(change_request)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Change request code already exists."
        )

    db.refresh(change_request)

    return change_request
@router.get(
    "",
    response_model=list[ChangeRequestResponse]
)
def get_change_requests(
    db: Session = Depends(get_db)
):

    statement = select(ChangeRequest)

    return db.scalars(statement).all()

@router.get(
    "/{change_code}",
    response_model=ChangeRequestResponse
)
def get_change_request(
    change_code: str,
    db: Session = Depends(get_db)
):

    change_request = db.scalar(
        select(ChangeRequest).where(
            ChangeRequest.change_code == change_code
        )
    )

    if change_request is None:
        raise HTTPException(
            status_code=404,
            detail="Change request not found."
        )

    return change_request

@router.get(
    "/{change_code}/impact",
    response_model=ChangeImpactResponse
)
def analyze_change_impact(
    change_code: str,
    db: Session = Depends(get_db)
):

    change_request = db.scalar(
        select(ChangeRequest).where(
            ChangeRequest.change_code == change_code
        )
    )

    if change_request is None:
        raise HTTPException(
            status_code=404,
            detail="Change request not found."
        )

    requirement = db.get(
        Requirement,
        change_request.requirement_id
    )

    if requirement is None:
        raise HTTPException(
            status_code=404,
            detail="Requirement not found."
        )

    impact = get_requirement_impact(
        requirement.requirement_code,
        db
    )

    direct_impact = impact[
        "starting_components"
    ]

    all_impacted = impact[
        "impacted_components"
    ]

    direct_ids = {
        component.id
        for component in direct_impact
    }

    downstream_impact = [
        component
        for component in all_impacted
        if component.id not in direct_ids
    ]

    impacted_by_type = {}

    for component in all_impacted:

        type_name = component.component_type.value

        impacted_by_type[type_name] = (
            impacted_by_type.get(type_name, 0)
            + 1
        )

    owners = sorted({
        component.owner
        for component in all_impacted
        if component.owner
    })

    return {
        "change_code": change_request.change_code,

        "change_title": change_request.title,

        "requirement_code": (
            requirement.requirement_code
        ),

        "requirement_title": (
            requirement.title
        ),

        "current_state": (
            change_request.current_state
        ),

        "proposed_state": (
            change_request.proposed_state
        ),

        "business_rules": impact[
            "business_rules"
        ],

        "direct_impact": direct_impact,

        "downstream_impact": downstream_impact,

        "total_impacted_components": len(
            all_impacted
        ),

        "impacted_by_type": impacted_by_type,

        "affected_owners": owners
    }