# Streamlit Community Cloud Deployment

Disease Prediction Capstone includes a lightweight, artifact-independent public dashboard designed for Streamlit Community Cloud.

## Deployment settings

After this pull request is merged, create the app with:

```text
Repository:
CoreyLeath-code/Disease_Prediction_Capstone

Branch:
main

Main file path:
streamlit_demo/app.py
```

The public demo does not require API keys, model files, private datasets, GPUs, or external services.

## Runtime design

Streamlit Community Cloud installs the dependency manifest nearest to the selected entry point. The dedicated `streamlit_demo/` directory keeps the deployment small and avoids installing training, model-serving, testing, or security tooling.

Deployment files:

- `streamlit_demo/app.py` — Community Cloud entry point.
- `streamlit_demo/requirements.txt` — lightweight pinned dependencies.
- `.python-version` — Python 3.11 runtime pin.
- `.streamlit/config.toml` — headless server, XSRF protection, and theme configuration.
- `streamlit_app.py` — dashboard implementation.
- `src/risk_engine.py` — shared deterministic domain engine.

## Local validation

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

The Streamlit health endpoint is:

```text
http://localhost:8501/_stcore/health
```

## Public-demo behavior

The dashboard provides:

- bounded biomarker and vital-sign inputs;
- three fictional example profiles;
- a deterministic educational indicator score;
- explicit low, moderate, and elevated demonstration bands;
- explainability evidence for each configured threshold;
- responsible-use notes and non-clinical disclaimers;
- a downloadable JSON result;
- architecture, nine-tier hygiene, and extended Q&A panels.

The output is not a diagnosis, a calibrated disease probability, medical advice, or a substitute for evaluation by a licensed clinician.

## Data safety

Do not enter:

- names;
- dates of birth;
- medical-record numbers;
- addresses;
- phone numbers;
- email addresses;
- real laboratory records;
- any protected or identifiable health information.

Use only fictional, synthetic, or fully non-identifiable values.

## Secrets

No secrets are required for the built-in demo. If optional integrations are added later, configure them through Streamlit Community Cloud's encrypted secrets interface. Never commit `.streamlit/secrets.toml`, `.env` files, tokens, or credentials.

## CI evidence

The Enterprise CI workflow:

1. installs the Streamlit-specific manifest;
2. imports the dashboard implementation;
3. verifies the shared domain contract;
4. starts Streamlit in headless mode;
5. checks `/_stcore/health`;
6. requires the Streamlit job to pass before release readiness can pass.

## Troubleshooting

### Dependency installation is slow

Confirm that the selected main file is exactly:

```text
streamlit_demo/app.py
```

Selecting the repository-root implementation may cause Streamlit Cloud to use the broader root dependency manifest.

### Import error

Reboot the app after merging changes and confirm the branch is `main`. The wrapper adds the repository root to `sys.path` before importing `streamlit_app.py`.

### App starts but no result appears

Select a fictional preset or enter bounded values, then choose **Run educational screening**.

### Health check fails in CI

Review the Streamlit job log. The workflow prints `streamlit.log` on exit so import, configuration, and startup failures remain visible.
