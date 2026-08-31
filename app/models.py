from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class Severity(StrEnum):
    healthy = "healthy"
    warning = "warning"
    critical = "critical"


class ServiceSignal(BaseModel):
    service: str = Field(min_length=2, max_length=100)
    availability: float = Field(ge=0, le=100)
    p95_latency_ms: float = Field(ge=0)
    error_rate: float = Field(ge=0, le=1)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Evaluation(BaseModel):
    service: str
    severity: Severity
    violations: list[str]
    remediation_action: str | None = None


class ServiceStatus(BaseModel):
    status: str
    service: str
