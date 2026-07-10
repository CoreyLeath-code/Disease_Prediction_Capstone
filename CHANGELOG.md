# Changelog

All notable changes to Disease Prediction Capstone are documented here.

The project follows Semantic Versioning and the Keep a Changelog structure.

## [Unreleased]

### Added

- Artifact-independent Streamlit Community Cloud dashboard.
- Lightweight Streamlit deployment entry point and pinned dependency manifest.
- Python 3.11 deployment pin and hardened Streamlit configuration.
- Transparent deterministic educational risk-screening engine.
- Fictional preset profiles, explainability evidence, responsible-use notes, and JSON export.
- Validated FastAPI root, health, metrics, examples, and prediction contracts.
- Prometheus request, error, and latency metrics.
- Python 3.10 and 3.11 CI matrix.
- Domain and API tests with coverage XML and JUnit evidence.
- Streamlit health smoke testing.
- Container build and live health smoke testing.
- CodeQL, Gitleaks, Bandit, Trivy, pip-audit, Dependabot, and CycloneDX SBOM automation.
- Semantic GitHub Releases and GHCR container publishing with provenance and SBOM generation.
- L6 nine-tier deployment-hygiene documentation.
- Streamlit deployment runbook.
- CODEOWNERS and deployment-aware pull-request template.

### Changed

- Replaced import-time serialized-model loading with a shared artifact-independent domain engine.
- Reworked legacy API and Streamlit entry points as compatibility wrappers.
- Hardened the supervisor workflow with immutable state, bounded inputs, monotonic timing, and transparent deterministic safety review.
- Replaced unsupported clinical and external-LLM claims with explicit educational-use language.
- Reworked the API image into a multi-stage, non-root, minimal runtime.
- Separated API, Streamlit, and development dependency manifests.
- Updated security and contribution policies for data minimization and non-clinical use.

### Security

- Added unknown-field rejection at the API boundary.
- Added explicit prohibition on real patient data and protected health information in the public demo.
- Added secret, source, dependency, filesystem, and container scanning evidence.
- Excluded datasets, model artifacts, credentials, notebooks, and development output from the container context.

## [1.0.0] - 2025-06-01

### Added

- Initial disease-prediction capstone structure.
- Early FastAPI, model-loading, agent, testing, and documentation experiments.

[Unreleased]: https://github.com/CoreyLeath-code/Disease_Prediction_Capstone/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/CoreyLeath-code/Disease_Prediction_Capstone/releases/tag/v1.0.0
