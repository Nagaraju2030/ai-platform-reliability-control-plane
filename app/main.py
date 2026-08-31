from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
import structlog

from app.config import Settings, get_settings
from app.logging import configure_logging
from app.models import Evaluation, ServiceSignal, ServiceStatus
from app.observability import record_evaluation
from app.reliability import ReliabilityEngine

settings = get_settings()
configure_logging(settings.log_level)
logger = structlog.get_logger()
app = FastAPI(title=settings.app_name, version="1.0.0")


def require_api_key(
    x_api_key: str | None = Header(default=None),
    config: Settings = Depends(get_settings),
) -> None:
    if not x_api_key or x_api_key != config.api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")


@app.get("/healthz", response_model=ServiceStatus, tags=["platform"])
def health() -> ServiceStatus:
    return ServiceStatus(status="ok", service="control-plane")


@app.get("/readyz", response_model=ServiceStatus, tags=["platform"])
def readiness() -> ServiceStatus:
    return ServiceStatus(status="ready", service="control-plane")


@app.get("/metrics", include_in_schema=False)
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post(
    "/v1/evaluations",
    response_model=Evaluation,
    dependencies=[Depends(require_api_key)],
    tags=["reliability"],
)
def evaluate(signal: ServiceSignal, config: Settings = Depends(get_settings)) -> Evaluation:
    result = ReliabilityEngine(config).evaluate(signal)
    record_evaluation(signal.service, result.severity.value, signal.p95_latency_ms)
    logger.info(
        "reliability_evaluation",
        service=signal.service,
        severity=result.severity.value,
        violations=result.violations,
    )
    return result
