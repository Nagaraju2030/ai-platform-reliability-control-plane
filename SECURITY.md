# Security

## Controls

- Evaluation APIs require an API key supplied through environment/secret management.
- Secrets are never committed; `.env` is ignored and `.env.example` contains placeholders only.
- Request payloads are constrained with Pydantic validation.
- The container runs as a non-root user.
- Kubernetes manifests define resource limits and health probes.
- CI uses read-only repository permissions.

## Production recommendations

Use a managed secret store (AWS Secrets Manager, Azure Key Vault, or Kubernetes External Secrets), terminate TLS at an ingress/API gateway, rotate credentials, restrict `/metrics` to the observability network, add rate limiting/WAF controls, sign container images, scan dependencies/images, and require human approval before destructive remediation actions.

Do not expose the example API key in production.
