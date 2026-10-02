from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.business_rule import BusinessRule
from app.models.dependency import Dependency
from app.models.requirement import Requirement
from app.models.system_component import SystemComponent
from app.models.trace_link import TraceLink


def get_requirement_impact(
    requirement_code: str,
    db: Session
):
    requirement = db.scalar(
        select(Requirement).where(
            Requirement.requirement_code == requirement_code
        )
    )

    if requirement is None:
        return None

    business_rules = db.scalars(
        select(BusinessRule).where(
            BusinessRule.requirement_id == requirement.id
        )
    ).all()

    starting_components = []

    for rule in business_rules:
        trace_links = db.scalars(
            select(TraceLink).where(
                TraceLink.business_rule_id == rule.id
            )
        ).all()

        for link in trace_links:
            component = db.get(
                SystemComponent,
                link.component_id
            )

            if component:
                starting_components.append(component)

    visited = set()
    impacted_components = []

    for component in starting_components:
        traverse_dependencies(
            component.id,
            db,
            visited,
            impacted_components
        )

    return {
        "requirement": requirement,
        "business_rules": business_rules,
        "starting_components": starting_components,
        "impacted_components": impacted_components
    }


def traverse_dependencies(
    component_id: int,
    db: Session,
    visited: set,
    impacted_components: list
):
    if component_id in visited:
        return

    visited.add(component_id)

    component = db.get(
        SystemComponent,
        component_id
    )

    if component:
        impacted_components.append(component)

    dependencies = db.scalars(
        select(Dependency).where(
            Dependency.source_component_id
            == component_id
        )
    ).all()

    for dependency in dependencies:
        traverse_dependencies(
            dependency.target_component_id,
            db,
            visited,
            impacted_components
        )