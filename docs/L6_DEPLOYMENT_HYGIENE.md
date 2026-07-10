# Disease Prediction Capstone — L6 Nine-Tier Deployment Hygiene

This document defines the repository's portfolio engineering baseline and the automated evidence associated with each tier. **L6** is used here as an engineering-maturity target for the portfolio; it is not an employment-level certification, a regulatory designation, or a claim that this software is clinically approved.

The application is an educational risk-screening demonstration. It is not a medical device, does not diagnose disease, and must not be used for patient-care decisions.

## Tier 1 — Source Hygiene

**Objective:** keep the source tree deterministic, reviewable, typed, and resistant to configuration drift.

Controls:

- Bounded domain inputs in `src/risk_engine.py`.
- Bounded Pydantic API schemas with unknown-field rejection.
- Immutable orchestration state snapshots.
- Explicit educational-use disclaimers and backend provenance.
- Python syntax compilation in CI.
- High-confidence Ruff correctness gates.
- Separate pinned manifests for API, Streamlit, and development environments.
- Python 3.11 deployment pin.

Evidence:

- `src/risk_engine.py`
- `api/main.py`
- `agents/state.py`
- `requirements-api.txt`
- `requirements-dev.txt`
- `streamlit_demo/requirements.txt`
- `.python-version`

## Tier 2 — Test Engineering

**Objective:** validate public contracts, deterministic behavior, edge cases, and failure modes.

Controls:

- Python 3.10 and 3.11 compatibility matrix.
- API root, health, metrics, examples, validation, and prediction tests.
- Domain tests for low, moderate, and elevated demonstration bands.
- Determinism checks.
- Invalid range and blood-pressure ordering tests.
- Coverage XML and JUnit evidence artifacts.
- Streamlit import and domain-contract validation.

Evidence:

- `tests/test_api.py`
- `tests/test_risk_engine.py`
- `.github/workflows/ci.yml`

## Tier 3 — Static Quality

**Objective:** identify correctness and security defects before runtime.

Controls:

- Python compile validation.
- Ruff undefined-name and syntax-related checks.
- CodeQL analysis.
- Pydantic request and response contracts.
- Frozen domain and orchestration data structures.
- Explicit type annotations in critical paths.

Evidence:

- `.github/workflows/ci.yml`
- `.github/workflows/security.yml`
- `api/main.py`
- `src/risk_engine.py`
- `agents/state.py`

## Tier 4 — Security Engineering

**Objective:** reduce source, secret, input, dependency, container, and data-handling risk.

Controls:

- Gitleaks current-tree secret scanning.
- Bandit report generation.
- Trivy filesystem and container reports.
- Non-root container execution.
- Minimal container contents.
- Bounded API and domain inputs.
- Unknown-field rejection to discourage accidental personal-data collection.
- Responsible vulnerability-disclosure policy.
- Explicit prohibition on real patient data in the public demo.

Evidence:

- `.github/workflows/security.yml`
- `SECURITY.md`
- `Dockerfile`
- `.gitignore`
- `.dockerignore`

## Tier 5 — Supply-Chain Hygiene

**Objective:** make dependencies visible, reviewable, maintainable, and auditable.

Controls:

- Version-pinned API, Streamlit, and development manifests.
- Dependabot for Python, Streamlit, GitHub Actions, and Docker.
- `pip-audit` reports for both deployment manifests.
- CycloneDX repository SBOM generation.
- Container SBOM and provenance on release builds.

Evidence:

- `requirements-api.txt`
- `streamlit_demo/requirements.txt`
- `requirements-dev.txt`
- `.github/dependabot.yml`
- `.github/workflows/security.yml`
- `.github/workflows/release.yml`

## Tier 6 — Reproducible Runtime

**Objective:** make local, CI, container, and Streamlit execution predictable.

Controls:

- Multi-stage API image.
- Minimal API-only dependency set.
- Non-root runtime identity.
- Explicit Uvicorn entry point.
- Container health check.
- Python 3.11 deployment pin.
- Lightweight Streamlit-specific dependency set.
- Artifact-independent public demonstration.
- Deterministic, transparent risk-screening baseline.

Evidence:

- `Dockerfile`
- `.python-version`
- `.streamlit/config.toml`
- `streamlit_demo/app.py`
- `streamlit_demo/requirements.txt`
- `src/risk_engine.py`

## Tier 7 — Continuous Delivery

**Objective:** validate every integration path consistently before merge.

Controls:

- Pull-request and main-branch validation.
- Superseded-run cancellation.
- Multi-version quality and test matrix.
- Streamlit server health smoke test.
- Container build and live API health smoke test.
- Release-readiness contract that always executes and reports prerequisite states.
- Test, coverage, and deployment evidence artifacts.

Evidence:

- `.github/workflows/ci.yml`

## Tier 8 — Release Engineering

**Objective:** create traceable, repeatable, and distributable release artifacts.

Controls:

- Semantic version tag trigger using `vMAJOR.MINOR.PATCH`.
- Generated GitHub Release notes.
- Source archives excluding local data, model artifacts, and secrets.
- GHCR container publishing.
- OCI metadata labels.
- Container provenance and SBOM generation.

Evidence:

- `.github/workflows/release.yml`
- `CHANGELOG.md`

## Tier 9 — Operational Governance

**Objective:** make ownership, responsible-use assumptions, promotion criteria, and recovery expectations explicit.

Controls:

- Security and vulnerability-disclosure process.
- Contribution, validation, and data-safety standards.
- Semantic changelog.
- CODEOWNERS.
- Deployment-aware pull-request template.
- API liveness and Prometheus metrics endpoints.
- Streamlit deployment runbook.
- Explicit non-clinical-use disclaimer.
- Auditable CI, security, dependency, coverage, test, and SBOM artifacts.

Evidence:

- `SECURITY.md`
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `.github/CODEOWNERS`
- `.github/pull_request_template.md`
- `docs/STREAMLIT_DEPLOYMENT.md`
- `README.md`

## Promotion Standard

A change is eligible for merge when:

1. Python 3.10 and 3.11 quality-and-test jobs pass.
2. The Streamlit deployment smoke test passes.
3. The API container builds and its live health endpoint passes.
4. The release-readiness contract passes.
5. Security and supply-chain workflows produce their expected evidence.
6. New behavior is tested and documented.
7. No secrets, real patient data, or identifiable health information are introduced.

Advisory scan findings should become focused remediation issues. They should not be hidden, silently discarded, or misrepresented as proof of regulatory compliance.
