# AI Platform Reliability Control Plane

A production-oriented **AI/SRE reliability control plane** for evaluating AI APIs against service-level objectives, detecting reliability degradation, exposing operational telemetry, and recommending policy-driven remediation.

This project demonstrates the engineering layer required around production LLM, RAG, agentic, and ML services—not another model demo.

## Why this project

AI workloads introduce reliability challenges beyond ordinary REST services: expensive inference, variable latency, upstream model/provider failures, retrieval dependencies, and cascading agent/tool errors. This control plane provides a small but extensible reliability boundary where teams can centralize SLO decisions before integrating automated operational actions.

## Architecture

```text
AI/ML APIs -> Reliability Signal -> FastAPI Control Plane
                                      |
                                      v
                              SLO Policy Engine
                         availability / p95 / errors
                               |              |
                               v              v
                         Prometheus      Remediation
                          + JSON logs       decision
```

See [`docs/architecture.md`](docs/architecture.md) for the full flow and production extension points.

## Production features

- FastAPI API with typed Pydantic contracts and automatic OpenAPI documentation
- Configurable availability, p95 latency, and error-rate SLO policies
- Deterministic healthy/warning/critical classification
- Policy-driven remediation recommendations for critical incidents
- API-key authentication on control operations
- Structured JSON logging
- Prometheus metrics
- Kubernetes liveness/readiness probes and resource limits
- Non-root Docker runtime
- Docker Compose stack with Prometheus
- Unit and API tests
- Ruff lint/format, strict mypy, pytest coverage
- GitHub Actions quality gate and container build validation
- Explicit security hardening guidance and sample operational data

## Tech stack

Python 3.11+, FastAPI, Pydantic Settings, Prometheus Client, Structlog, Pytest, Ruff, mypy, Docker, Docker Compose, Kubernetes, GitHub Actions.

## Repository structure

```text
.
├── app/
│   ├── config.py
│   ├── logging.py
│   ├── main.py
│   ├── models.py
│   ├── observability.py
│   └── reliability.py
├── deploy/
│   ├── kubernetes.yaml
│   └── prometheus.yml
├── docs/
│   ├── api-contract.md
│   └── architecture.md
├── sample-data/signals.json
├── tests/
│   ├── test_api.py
│   └── test_reliability.py
├── .github/workflows/ci.yml
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── SECURITY.md
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e '.[dev]'
cp .env.example .env       # Windows: copy .env.example .env
uvicorn app.main:app --reload
```

Open API docs at `http://localhost:8000/docs`, health at `http://localhost:8000/healthz`, and metrics at `http://localhost:8000/metrics`.

## Example evaluation

```bash
curl -X POST http://localhost:8000/v1/evaluations \
  -H "Content-Type: application/json" \
  -H "X-API-Key: replace-with-a-long-random-secret" \
  -d '{"service":"enterprise-rag-api","availability":98.8,"p95_latency_ms":4200,"error_rate":0.06}'
```

A multi-SLO breach is classified as `critical` and can return `rollback_or_shift_traffic` as the remediation recommendation. See [`docs/api-contract.md`](docs/api-contract.md).

## Docker Compose

```bash
cp .env.example .env
# Replace CONTROL_PLANE_API_KEY before running.
docker compose up --build
```

The API is available on port `8000`; Prometheus is available on port `9090`.

## Quality checks

```bash
ruff check .
ruff format --check .
mypy app
pytest
```

CI performs all four checks and then validates that the Docker image builds.

## Kubernetes deployment

Build and publish the container image referenced by `deploy/kubernetes.yaml`, then create the runtime secret and deploy:

```bash
kubectl create secret generic control-plane-secrets \
  --from-literal=CONTROL_PLANE_API_KEY='<strong-secret>' \
  --from-literal=CONTROL_PLANE_ENVIRONMENT='production'
kubectl apply -f deploy/kubernetes.yaml
```

For production, pin the deployment to an immutable image digest instead of `latest` and place the service behind authenticated TLS ingress.

## Security

See [`SECURITY.md`](SECURITY.md). Automated remediation in this portfolio implementation produces a **recommendation** rather than directly mutating infrastructure. Production integrations should add RBAC, approval gates, audit trails, idempotency, rollback safety, and cloud-native secret management before enabling write actions.

## Roadmap

Natural enterprise extensions include OpenTelemetry traces, burn-rate alerting, persistent incident history, LangGraph human-approval remediation, Kubernetes/Argo Rollouts adapters, provider failover, anomaly models, PagerDuty/Slack integrations, and Grafana dashboards.

## License

Use this project as a portfolio/reference implementation. Add your organization's preferred license before commercial reuse.
