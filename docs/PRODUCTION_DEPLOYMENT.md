# Production Deployment Runbook

This runbook describes the minimum controls required before exposing the educational screening API to real users. The repository is a portfolio demonstration, not a clinically validated medical device.

## Scope and non-negotiable boundaries

- Use only synthetic or fully non-identifiable values.
- Do not send protected health information (PHI), names, identifiers, or clinical records.
- Do not describe the output as a diagnosis, treatment recommendation, or calibrated probability.
- Keep the public Streamlit demo separate from any private API deployment.

## Reference topology

Place the API behind a managed TLS-terminating reverse proxy or API gateway:

```text
Internet -> TLS gateway/WAF -> authenticated private network -> API container
                                      |
                                      +-> metrics collector (restricted network)
```

The API container should not be directly exposed to the public internet. Bind the container to a private interface, restrict ingress to the gateway, and expose `/metrics` only to the monitoring network.

## Required controls before go-live

### Identity and network

- Enforce HTTPS with an automatically renewed certificate.
- Require authentication and authorization at the gateway; the application intentionally does not implement user identity.
- Apply rate limits, request-size limits, idle timeouts, and connection limits.
- Restrict outbound egress to only required destinations. The current API should need none.
- Place the service in a private subnet or equivalent network boundary.
- Define an administrative break-glass procedure and test it.

### Secrets and data handling

- Store secrets in a managed secret store; never use Docker build arguments or committed files.
- Disable request-body logging at the gateway and application layers.
- Define retention, deletion, and access-review policies before accepting any sensitive input.
- Verify that traces, metrics, crash reports, and backups cannot contain request payloads.
- Document the data owner, processor, purpose, and approved regions.

### Observability and operations

- Monitor liveness, latency, error rate, saturation, and restart count.
- Alert on repeated 5xx responses, health-check failures, abnormal latency, and resource exhaustion.
- Scrape Prometheus metrics from a restricted network only.
- Centralize logs with access controls and a documented retention period.
- Record deployment version, image digest, configuration revision, and rollback target.
- Run a restore drill for configuration and operational data if any are introduced.

### Release and rollback

- Deploy an immutable image digest, not a floating `latest` tag.
- Require CI, security, and dependency checks before release.
- Generate and retain the release SBOM and provenance evidence.
- Roll out to a staging environment with synthetic smoke traffic first.
- Use a canary or blue/green strategy where practical.
- Keep the previous known-good image digest available for rollback.
- Roll back automatically on failed health checks or error-budget regression.

## Go-live checklist

- [ ] Threat model reviewed and accepted.
- [ ] Privacy and responsible-use review completed.
- [ ] TLS, gateway authentication, rate limiting, and network policy tested.
- [ ] Payload and secret redaction verified in logs, traces, and metrics.
- [ ] Synthetic end-to-end smoke test passed.
- [ ] Image digest, SBOM, and provenance recorded.
- [ ] Alerts tested with a controlled failure.
- [ ] Rollback completed successfully in staging.
- [ ] On-call owner and incident procedure documented.
- [ ] Clinical/regulatory review completed if the intended use changes.

## Incident response

1. Restrict or disable ingress if unauthorized data may have been submitted.
2. Preserve access-controlled logs and deployment metadata without copying request payloads.
3. Rotate potentially exposed credentials and revoke affected sessions.
4. Identify the image digest, configuration revision, and time window.
5. Notify the designated security/privacy owner according to the applicable policy.
6. Restore service only after the boundary, data handling, and rollback checks are re-validated.

A passing GitHub Actions workflow is necessary evidence for this project, but it is not a production authorization, privacy certification, clinical validation, or regulatory approval.
