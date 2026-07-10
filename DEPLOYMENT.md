# Deployment Guide — Disease Prediction Capstone

This guide covers the two supported deployment paths:

1. **Streamlit Community Cloud** for the public educational dashboard.
2. **Docker / GHCR** for the FastAPI service.

The project is an educational portfolio demonstration. It is not a medical device and must not be used for patient-care decisions.

## 1. Streamlit Community Cloud

Use these settings:

```text
Repository:
CoreyLeath-code/Disease_Prediction_Capstone

Branch:
main

Main file path:
streamlit_demo/app.py
```

No secrets, model artifacts, private datasets, GPUs, or external APIs are required.

The deployment uses:

- `.python-version` for Python 3.11;
- `streamlit_demo/requirements.txt` for lightweight dependencies;
- `.streamlit/config.toml` for theme and server settings;
- `streamlit_demo/app.py` as the cloud entry point;
- `streamlit_app.py` as the shared dashboard implementation.

See `docs/STREAMLIT_DEPLOYMENT.md` for troubleshooting and responsible-use requirements.

## 2. Local Streamlit Deployment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r streamlit_demo/requirements.txt
streamlit run streamlit_demo/app.py
```

Open:

```text
http://localhost:8501
```

Health endpoint:

```text
http://localhost:8501/_stcore/health
```

## 3. Local FastAPI Deployment

Install only API dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements-api.txt
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Open:

```text
API:     http://localhost:8000
Swagger: http://localhost:8000/docs
ReDoc:   http://localhost:8000/redoc
Health:  http://localhost:8000/health
Metrics: http://localhost:8000/metrics
```

## 4. Docker Deployment

Build:

```bash
docker build --pull -t disease-prediction-capstone .
```

Run:

```bash
docker run --rm \
  --name disease-prediction-capstone \
  -p 8000:8000 \
  disease-prediction-capstone
```

Verify:

```bash
curl --fail http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy",
  "service": "disease-prediction-capstone-api",
  "version": "2.0.0",
  "clinical_use": false
}
```

## 5. Container Security Properties

The Dockerfile uses:

- a separate dependency-builder stage;
- a minimal Python 3.11 slim runtime;
- a non-root user with UID `10001`;
- an explicit Uvicorn entry point;
- an HTTP health check;
- an API-only dependency manifest;
- a reduced build context that excludes datasets, model artifacts, notebooks, credentials, and development output.

## 6. GHCR Release Image

Semantic tags trigger the release workflow.

Example:

```bash
git tag v2.0.0
git push origin v2.0.0
```

Published image:

```text
ghcr.io/coreyleath-code/disease-prediction-capstone
```

Pull and run:

```bash
docker pull ghcr.io/coreyleath-code/disease-prediction-capstone:2.0.0

docker run --rm \
  -p 8000:8000 \
  ghcr.io/coreyleath-code/disease-prediction-capstone:2.0.0
```

The release workflow also creates GitHub Release notes, a source archive, OCI labels, provenance, and a container SBOM.

## 7. Generic Container Platform Guidance

The API image can run on services that support OCI containers, including managed container platforms and Kubernetes. Configure:

```text
Container port: 8000
Health path: /health
Protocol: HTTP
```

Recommended baseline controls:

- HTTPS at the ingress or load balancer;
- a non-root runtime;
- read-only root filesystem when supported;
- dropped Linux capabilities;
- CPU and memory limits;
- request-rate controls;
- network restrictions;
- centralized logs with a privacy-reviewed retention policy;
- no real patient data;
- no credentials baked into the image.

## 8. API Smoke Test

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 52,
    "bmi": 28.4,
    "systolic_bp": 134,
    "diastolic_bp": 84,
    "glucose": 112,
    "insulin": 118,
    "skin_thickness": 30,
    "cholesterol": 216,
    "hba1c": 5.9
  }'
```

The response includes:

- an educational indicator score;
- a low, moderate, or elevated demonstration band;
- transparent contributors;
- responsible-use notes;
- deterministic-backend provenance;
- a non-clinical disclaimer.

## 9. Secrets

The built-in Streamlit and API deployments require no secrets.

If optional integrations are added later:

- use Streamlit Community Cloud encrypted secrets for the dashboard;
- use GitHub Actions secrets for workflows;
- use a managed secret store for production workloads;
- never commit `.env`, `.streamlit/secrets.toml`, tokens, or credentials;
- do not pass long-lived secrets through Docker build arguments.

## 10. Rollback

For a container release:

1. identify the previously healthy semantic image tag;
2. redeploy that immutable tag;
3. verify `/health`;
4. run the `/predict` smoke contract with fictional input;
5. preserve logs and security evidence for incident review.

For Streamlit Community Cloud:

1. select the last known-good commit or branch;
2. reboot the application;
3. verify `/_stcore/health`;
4. run a fictional preset through the dashboard.

## 11. Deployment Boundary

A successful deployment proves that the software starts and its automated contracts pass. It does **not** establish clinical validity, regulatory approval, healthcare compliance, fairness, calibration, or fitness for patient care.
