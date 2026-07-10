# Contributing to Disease Prediction Capstone

Thank you for contributing. This repository is an educational engineering portfolio project focused on transparent risk-screening logic, FastAPI, Streamlit, testing, security, and deployment automation.

It is **not a medical device** and must not be used for diagnosis, treatment, triage, or patient-care decisions.

## Development setup

```bash
git clone https://github.com/CoreyLeath-code/Disease_Prediction_Capstone.git
cd Disease_Prediction_Capstone
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

## Required local validation

Run the same critical checks enforced by CI:

```bash
python -m compileall -q api agents src tests streamlit_app.py streamlit_demo/app.py
ruff check api agents src tests/test_api.py tests/test_risk_engine.py streamlit_app.py streamlit_demo/app.py \
  --select E9,F63,F7,F82
pytest tests/test_api.py tests/test_risk_engine.py -v \
  --cov=api --cov=src --cov-report=term-missing
docker build -t disease-capstone:local .
```

Validate the public dashboard locally:

```bash
streamlit run streamlit_demo/app.py
```

## Data-safety requirements

Do not commit, upload, log, or use in screenshots:

- real patient records;
- names, dates of birth, addresses, phone numbers, or email addresses;
- medical-record, insurance, or government identifiers;
- protected health information (PHI);
- restricted clinical documents;
- model artifacts trained on sensitive or unlicensed datasets.

Use synthetic, fictional, or fully non-identifiable data only.

## Code standards

### Python

- Use type annotations in public and critical paths.
- Keep functions focused and deterministic when practical.
- Add docstrings that explain purpose and safety boundaries.
- Prefer explicit validation over implicit assumptions.
- Avoid hidden global state and import-time model loading.
- Use `time.perf_counter()` for elapsed-time measurement.

### Domain logic

- Do not describe a heuristic score as a diagnosis or calibrated probability.
- Keep thresholds and weights transparent and test-covered.
- Preserve the educational-use disclaimer.
- Document the source and validation status of any future model.
- Add tests for boundary values, invalid inputs, deterministic behavior, and output provenance.

### FastAPI

- Use bounded Pydantic request and response models.
- Reject unknown fields unless a documented use case requires them.
- Avoid returning stack traces, local paths, or raw exception details.
- Keep `/health` lightweight and dependency-free.
- Update OpenAPI examples when contracts change.

### Streamlit

- Keep the public deployment artifact-independent.
- Use the lightweight manifest in `streamlit_demo/requirements.txt`.
- Do not add secrets to source control.
- Preserve clear non-clinical labels and responsible-use guidance.
- Test the `/_stcore/health` endpoint in CI after meaningful UI changes.

### Containers and release engineering

- Keep the runtime non-root.
- Do not bake datasets, credentials, or private model artifacts into images.
- Preserve health checks and minimal runtime dependencies.
- Document operational and rollback impact for deployment changes.

## Branch and commit conventions

Use focused branches, for example:

```text
feat/add-calibration-evidence
fix/api-range-validation
test/add-boundary-cases
docs/update-streamlit-runbook
```

Conventional Commit prefixes are recommended:

```text
feat:
fix:
refactor:
test:
docs:
security:
ci:
build:
deploy:
release:
chore:
```

## Pull-request standard

Every pull request should explain:

1. the problem or risk being addressed;
2. the design and alternatives considered;
3. user-facing and API behavior changes;
4. validation evidence;
5. security, privacy, and data-handling impact;
6. deployment and rollback impact;
7. documentation updates.

Before requesting review, confirm:

- [ ] New behavior is tested.
- [ ] Python 3.10 and 3.11 checks pass.
- [ ] Streamlit deployment smoke testing passes when applicable.
- [ ] The API container builds and becomes healthy.
- [ ] No secrets or identifiable health data are included.
- [ ] Disclaimers and backend provenance remain accurate.
- [ ] Documentation and changelog entries are updated.

## Review criteria

Reviewers should evaluate:

- correctness and deterministic behavior;
- input boundaries and failure modes;
- medical-claim and responsible-use language;
- privacy and data-minimization impact;
- security and dependency impact;
- maintainability and testability;
- observability and operational behavior;
- deployment compatibility and rollback safety.

## Release process

Releases use tags in the form:

```text
vMAJOR.MINOR.PATCH
```

A release tag triggers GitHub Release artifact generation and GHCR image publishing. Release notes should distinguish application features, safety changes, dependency changes, and operational changes.
