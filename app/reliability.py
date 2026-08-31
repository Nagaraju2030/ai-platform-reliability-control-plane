from app.config import Settings
from app.models import Evaluation, ServiceSignal, Severity


class ReliabilityEngine:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def evaluate(self, signal: ServiceSignal) -> Evaluation:
        violations: list[str] = []
        if signal.availability < self.settings.target_availability:
            violations.append("availability_slo_breach")
        if signal.p95_latency_ms > self.settings.target_p95_latency_ms:
            violations.append("latency_slo_breach")
        if signal.error_rate > self.settings.max_error_rate:
            violations.append("error_budget_breach")

        if len(violations) >= 2:
            severity = Severity.critical
        elif violations:
            severity = Severity.warning
        else:
            severity = Severity.healthy

        action = None
        if severity is Severity.critical and self.settings.remediation_enabled:
            action = self._select_remediation(violations)

        return Evaluation(
            service=signal.service,
            severity=severity,
            violations=violations,
            remediation_action=action,
        )

    @staticmethod
    def _select_remediation(violations: list[str]) -> str:
        if "error_budget_breach" in violations:
            return "rollback_or_shift_traffic"
        return "scale_and_run_health_checks"
