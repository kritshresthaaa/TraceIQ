from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.impact import ImpactAnalysisResponse
from app.services.impact_analysis import get_requirement_impact


router = APIRouter(
    prefix="/impact",
    tags=["Impact Analysis"]
)


@router.get(
    "/{requirement_code}",
    response_model=ImpactAnalysisResponse
)
def analyze_requirement_impact(
    requirement_code: str,
    db: Session = Depends(get_db)
):

    result = get_requirement_impact(
        requirement_code,
        db
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Requirement not found."
        )

    return {
        "requirement_code": (
            result["requirement"].requirement_code
        ),

        "requirement_title": (
            result["requirement"].title
        ),

        "business_rules": result["business_rules"],

        "starting_components": (
            result["starting_components"]
        ),

        "impacted_components": (
            result["impacted_components"]
        ),

        "total_impacted_components": len(
            result["impacted_components"]
        )
    }