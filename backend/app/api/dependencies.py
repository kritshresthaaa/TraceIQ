from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.dependency import Dependency
from app.models.system_component import SystemComponent
from app.schemas.dependency import DependencyCreate
from app.schemas.dependency import DependencyResponse


router = APIRouter(
    prefix="/dependencies",
    tags=["Dependencies"]
)


@router.post(
    "",
    response_model=DependencyResponse,
    status_code=201
)
def create_dependency(
    request: DependencyCreate,
    db: Session = Depends(get_db)
):

    source = db.scalar(
        select(SystemComponent).where(
            SystemComponent.component_code
            == request.source_component_code
        )
    )

    if source is None:
        raise HTTPException(
            status_code=404,
            detail="Source component not found."
        )

    target = db.scalar(
        select(SystemComponent).where(
            SystemComponent.component_code
            == request.target_component_code
        )
    )

    if target is None:
        raise HTTPException(
            status_code=404,
            detail="Target component not found."
        )

    if source.id == target.id:
        raise HTTPException(
            status_code=400,
            detail="A component cannot depend on itself."
        )

    dependency = Dependency(
        source_component_id=source.id,
        target_component_id=target.id,
        dependency_type=request.dependency_type
    )

    db.add(dependency)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Dependency already exists."
        )

    db.refresh(dependency)

    return dependency