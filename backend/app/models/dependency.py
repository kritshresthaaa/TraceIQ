from enum import Enum

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class DependencyType(str, Enum):
    DEPENDS_ON = "DEPENDS_ON"
    FEEDS = "FEEDS"
    USED_BY = "USED_BY"
    CALLS = "CALLS"
    TRIGGERS = "TRIGGERS"
    VALIDATED_BY = "VALIDATED_BY"
    REPORTED_IN = "REPORTED_IN"
    TESTED_BY = "TESTED_BY"


class Dependency(Base):
    __tablename__ = "dependencies"

    __table_args__ = (
        UniqueConstraint(
            "source_component_id",
            "target_component_id",
            name="uq_dependency_source_target"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    source_component_id: Mapped[int] = mapped_column(
        ForeignKey(
            "system_components.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    target_component_id: Mapped[int] = mapped_column(
        ForeignKey(
            "system_components.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    dependency_type: Mapped[DependencyType] = mapped_column(
        SQLEnum(DependencyType),
        nullable=False
    )