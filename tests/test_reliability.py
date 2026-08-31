from app.config import Settings
from app.models import ServiceSignal, Severity
from app.reliability import ReliabilityEngine


def test_healthy_signal() -> None:
    engine = ReliabilityEngine(Settings(api_key="test"))
    result = engine.evaluate(
        ServiceSignal(service="llm-gateway", availability=99.99, p95_latency_ms=900, error_rate=0.001)
    )
    assert result.severity is Severity.healthy
    assert result.violations == []


def test_critical_signal_triggers_remediation() -> None:
    engine = ReliabilityEngine(Settings(api_key="test"))
    result = engine.evaluate(
        ServiceSignal(service="rag-api", availability=98.0, p95_latency_ms=4000, error_rate=0.08)
    )
    assert result.severity is Severity.critical
    assert result.remediation_action == "rollback_or_shift_traffic"
