from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class ComponentType(str, Enum):
    DATABASE_TABLE = "DATABASE_TABLE"
    DATABASE_FIELD = "DATABASE_FIELD"
    SQL_QUERY = "SQL_QUERY"
    SERVICE = "SERVICE"
    API = "API"
    INTEGRATION = "INTEGRATION"
    REPORT = "REPORT"
    KPI = "KPI"
    TEST_CASE = "TEST_CASE"


class SystemComponent(Base):
    __tablename__ = "system_components"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    component_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    component_type: Mapped[ComponentType] = mapped_column(
        SQLEnum(ComponentType),
        nullable=False,
        index=True
    )

    technical_name: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    owner: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )