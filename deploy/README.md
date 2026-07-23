# Production Compose Profile

This profile is a hardened single-service reference for a private API host. It is not a complete internet-facing deployment: place a TLS gateway, authentication, authorization, rate limiting, and network policy in front of it.

## Use an immutable image

Set the image to a release digest or reviewed version before deployment:

```powershell
$env:DISEASE_CAPSTONE_IMAGE = "ghcr.io/coreyleath-code/disease-prediction-capstone:2.0.0"
docker compose -f deploy/docker-compose.production.yml pull
docker compose -f deploy/docker-compose.production.yml up -d
```

For the strongest rollback guarantee, use an image digest:

```text
ghcr.io/coreyleath-code/disease-prediction-capstone@sha256:<reviewed-digest>
```

## Verify and roll back

```powershell
docker compose -f deploy/docker-compose.production.yml ps
Invoke-WebRequest http://127.0.0.1:8000/health
docker compose -f deploy/docker-compose.production.yml logs --tail 100 api
```

Roll back by setting `DISEASE_CAPSTONE_IMAGE` to the previous reviewed digest, then run `pull` and `up -d` again.

Do not expose port 8000 directly to the internet. Follow `docs/PRODUCTION_DEPLOYMENT.md` for the required gateway, privacy, observability, and incident controls.
