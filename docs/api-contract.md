# API Contract

## `GET /healthz`
Liveness endpoint. No authentication required.

## `GET /readyz`
Readiness endpoint. No authentication required.

## `GET /metrics`
Prometheus exposition endpoint.

## `POST /v1/evaluations`
Evaluate an AI service against configured reliability objectives.

Header: `X-API-Key: <CONTROL_PLANE_API_KEY>`

Request:
```json
{
  "service": "enterprise-rag-api",
  "availability": 99.7,
  "p95_latency_ms": 3100,
  "error_rate": 0.025
}
```

Response:
```json
{
  "service": "enterprise-rag-api",
  "severity": "critical",
  "violations": [
    "availability_slo_breach",
    "latency_slo_breach",
    "error_budget_breach"
  ],
  "remediation_action": "rollback_or_shift_traffic"
}
```

HTTP errors: `401` invalid/missing API key; `422` request validation failure.
