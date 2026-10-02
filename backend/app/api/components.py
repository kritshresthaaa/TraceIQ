from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.system_component import SystemComponent
from app.schemas.system_component import SystemComponentCreate
from app.schemas.system_component import SystemComponentResponse


router = APIRouter(
    prefix="/components",
    tags=["System Components"]
)


@router.post(
    "",
    response_model=SystemComponentResponse,
    status_code=201
)
def create_component(
    request: SystemComponentCreate,
    db: Session = Depends(get_db)
):

    component = SystemComponent(
        component_code=request.component_code,
        name=request.name,
        component_type=request.component_type,
        technical_name=request.technical_name,
        description=request.description,
        owner=request.owner
    )

    db.add(component)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Component code already exists."
        )

    db.refresh(component)

    return component


@router.get(
    "",
    response_model=list[SystemComponentResponse]
)
def get_components(
    db: Session = Depends(get_db)
):

    statement = select(SystemComponent)

    return db.scalars(statement).all()