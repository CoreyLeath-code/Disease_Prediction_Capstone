# Security Policy

## Responsible-use boundary

Disease Prediction Capstone is an educational software-engineering and machine-learning portfolio project. It is **not a medical device**, has not been clinically validated, and must not be used to diagnose, treat, triage, or make patient-care decisions.

The public Streamlit application and API accept synthetic or non-identifiable demonstration values only.

## Supported versions

Security fixes are applied to the latest release and the `main` branch.

## Reporting a vulnerability

Do not disclose suspected vulnerabilities in a public issue or pull request.

Use GitHub private vulnerability reporting when available. Include:

- affected component and version;
- reproduction steps or proof of concept;
- expected and observed behavior;
- impact and severity assessment;
- suggested mitigation, when known.

Confirmed findings are prioritized by severity and documented after a remediation is available.

## Health-data and privacy rules

Never commit, upload, or enter into the public demo:

- names or contact information;
- dates of birth;
- medical-record or insurance identifiers;
- real laboratory, diagnosis, medication, or encounter records;
- protected health information (PHI);
- model artifacts trained on restricted or sensitive datasets;
- private vector indexes or clinical documents.

Use fictional, synthetic, or fully non-identifiable values only.

The application intentionally rejects unknown API fields to reduce accidental collection of unrelated personal information. This is a defense-in-depth control, not a complete privacy program.

## Application security controls

The repository implements:

- bounded Pydantic request validation;
- domain-level finite-value and range validation;
- explicit non-clinical disclaimers;
- transparent deterministic-backend provenance;
- controlled API response contracts;
- Prometheus request and latency metrics;
- non-root container execution;
- minimal API and Streamlit dependency manifests;
- container health checks;
- secret and vulnerability scanning;
- dependency auditing and SBOM generation.

Production deployments would still require HTTPS, authentication and authorization where appropriate, rate limiting, network controls, logging policy, retention policy, privacy review, and threat modeling.

## Secret management

Never commit:

- `.env` files;
- `.streamlit/secrets.toml`;
- API keys or access tokens;
- cloud credentials;
- private certificates;
- database connection strings;
- signing keys.

Use GitHub Actions secrets, Streamlit Community Cloud encrypted secrets, or a managed secret store. Do not pass long-lived secrets through Docker build arguments because build metadata and layers may expose them.

## Software supply chain

Automated controls include:

- CodeQL source analysis;
- Gitleaks current-tree secret scanning;
- Bandit report generation;
- Trivy filesystem and container reports;
- `pip-audit` reports for API and Streamlit manifests;
- Dependabot updates;
- CycloneDX SBOM generation;
- release-container provenance and SBOM generation.

Security reports are evidence for review and triage. A green workflow is not proof that the application is vulnerability-free or compliant with a healthcare regulation.

## Dependency policy

- Pin deployment dependencies.
- Review dependency updates before merge.
- Prefer maintained packages from established publishers.
- Remove unused dependencies.
- Keep the public Streamlit runtime separate from training and security tooling.
- Open focused remediation issues for actionable findings.

## Container security

The production API image:

- uses a multi-stage build;
- installs only API runtime dependencies;
- runs as a non-root user;
- exposes only the API port;
- includes a health check;
- excludes local datasets, model artifacts, secrets, notebooks, and development tooling from the build context.

## Clinical and model-safety requirements

Contributions must not:

- present heuristic output as a diagnosis or calibrated disease probability;
- claim regulatory approval or clinical validation without documented evidence;
- provide personalized treatment or medication instructions;
- silently change thresholds or scoring behavior;
- remove responsible-use disclaimers;
- introduce real patient data.

Any future trained model must document dataset provenance, intended use, excluded use, validation design, subgroup performance, calibration, limitations, and model versioning before its output is exposed publicly.
