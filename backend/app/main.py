from fastapi import FastAPI

from app.api.business_rules import router as business_rules_router
from app.api.components import router as components_router
from app.api.dependencies import router as dependencies_router
from app.api.requirements import router as requirements_router
from app.api.trace_links import router as trace_links_router
from app.core.config import settings
from app.api.impact import router as impact_router
from app.api.change_requests import (
    router as change_requests_router
)
app = FastAPI(
    title=settings.app_name,
    description=(
        "Requirements traceability and "
        "change-impact analysis platform."
    ),
    version="0.3.0"
)


app.include_router(requirements_router)
app.include_router(business_rules_router)
app.include_router(components_router)
app.include_router(trace_links_router)
app.include_router(dependencies_router)
app.include_router(impact_router)
app.include_router(
    change_requests_router
)
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": settings.app_name,
        "environment": settings.app_env
    }