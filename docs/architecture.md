# Architecture

```text
AI/ML Services
     |
     | reliability signals
     v
+---------------------------+
| FastAPI Control Plane     |
| auth + validation         |
+-------------+-------------+
              |
              v
+---------------------------+
| SLO / Error Budget Engine |
| availability              |
| p95 latency               |
| error rate                |
+-------------+-------------+
              |
       +------+------+
       |             |
       v             v
 Prometheus     Policy Decision
 / Metrics           |
                     v
             Remediation Action
          rollback / traffic shift
          scale / health checks
```

## Reliability flow

1. A monitored AI service or telemetry adapter posts an aggregated reliability signal.
2. API-key authentication and Pydantic validation reject malformed or unauthorized input.
3. The policy engine compares the signal with configurable SLO thresholds.
4. Healthy, warning, or critical severity is calculated deterministically.
5. Critical multi-SLO breaches produce a remediation recommendation when remediation is enabled.
6. Prometheus metrics and structured logs provide operational evidence for dashboards and alerts.

## Production extension points

The policy engine is intentionally separated from transport. Enterprise implementations can replace the deterministic remediation recommendation with LangGraph approval workflows, Kubernetes operators, Argo Rollouts, PagerDuty/Slack notification adapters, or cloud-native autoscaling APIs without changing the public API contract.
