from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.requirement import Requirement
from app.schemas.requirement import RequirementCreate
from app.schemas.requirement import RequirementResponse


router = APIRouter(
    prefix="/requirements",
    tags=["Requirements"]
)


@router.post(
    "",
    response_model=RequirementResponse,
    status_code=201
)
def create_requirement(
    request: RequirementCreate,
    db: Session = Depends(get_db)
):

    requirement = Requirement(
        requirement_code=request.requirement_code,
        title=request.title,
        description=request.description,
        status=request.status,
        priority=request.priority,
        owner=request.owner
    )

    db.add(requirement)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Requirement code already exists."
        )

    db.refresh(requirement)

    return requirement


@router.get(
    "",
    response_model=list[RequirementResponse]
)
def get_requirements(
    db: Session = Depends(get_db)
):

    statement = select(Requirement)

    requirements = db.scalars(statement).all()

    return requirements


@router.get(
    "/{requirement_code}",
    response_model=RequirementResponse
)
def get_requirement(
    requirement_code: str,
    db: Session = Depends(get_db)
):

    statement = select(Requirement).where(
        Requirement.requirement_code == requirement_code
    )

    requirement = db.scalar(statement)

    if requirement is None:
        raise HTTPException(
            status_code=404,
            detail="Requirement not found."
        )

    return requirement