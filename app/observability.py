from prometheus_client import Counter, Histogram

REQUESTS = Counter(
    "control_plane_evaluations_total",
    "Total reliability evaluations",
    ["service", "severity"],
)
LATENCY = Histogram(
    "control_plane_observed_p95_latency_ms",
    "Observed downstream p95 latency in milliseconds",
    ["service"],
)


def record_evaluation(service: str, severity: str, latency_ms: float) -> None:
    REQUESTS.labels(service=service, severity=severity).inc()
    LATENCY.labels(service=service).observe(latency_ms)
