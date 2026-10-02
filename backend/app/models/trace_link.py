from enum import Enum

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class TraceRelationship(str, Enum):
    IMPLEMENTED_BY = "IMPLEMENTED_BY"
    READS = "READS"
    WRITES = "WRITES"
    VALIDATED_BY = "VALIDATED_BY"
    REPORTED_BY = "REPORTED_BY"
    TESTED_BY = "TESTED_BY"


class TraceLink(Base):
    __tablename__ = "trace_links"

    __table_args__ = (
        UniqueConstraint(
            "business_rule_id",
            "component_id",
            name="uq_business_rule_component"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    business_rule_id: Mapped[int] = mapped_column(
        ForeignKey(
            "business_rules.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    component_id: Mapped[int] = mapped_column(
        ForeignKey(
            "system_components.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    relationship_type: Mapped[TraceRelationship] = mapped_column(
        SQLEnum(TraceRelationship),
        default=TraceRelationship.IMPLEMENTED_BY,
        nullable=False
    )