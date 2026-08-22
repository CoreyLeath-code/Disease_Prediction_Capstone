# L6 Engineering Audit — Disease Prediction Capstone

## Executive assessment

This repository is strongest when presented as an evidence-bounded educational health-risk screening system rather than a clinically validated disease predictor. The current public path is deterministic and explainable, has bounded input contracts, API/UI delivery surfaces, tests, security automation, and a non-root container. Those are meaningful software-engineering strengths.

The main L6 risk is narrative mismatch: the repository name and some legacy surfaces suggest disease prediction and retraining, while the verified public implementation is a transparent rule-based educational baseline. The project should keep those stories explicitly separated until a learned model is evaluated under a versioned, leakage-safe research protocol.

## Verified strengths

- deterministic, inspectable risk engine with explicit disclaimer
- finite/range validation for all public input fields
- tests for indicator bands, determinism, serialization, invalid inputs, and blood-pressure consistency
- FastAPI and Streamlit delivery boundaries
- non-root Python 3.11 container with health check
- CI/security/dependency/release automation
- semantic release and GHCR publication workflow already present

## Critical gaps

### 1. No clinical-model evaluation contract

The current public baseline is not trained on outcome labels and therefore cannot support accuracy, AUROC, sensitivity/specificity, calibration, or clinical-effectiveness claims.

### 2. No machine-readable runtime benchmark artifact

The repository documents what should be measured but does not yet check in a repeatable benchmark result containing commit SHA, hardware/runtime provenance, warm-up, sample count, concurrency, percentiles, throughput, error rate, and memory.

### 3. Repository identity versus verified capability

The name `Disease_Prediction_Capstone` is broader than the current verified implementation. Documentation should continue to say "educational risk-screening baseline" unless a trained model and evaluation artifact are explicitly selected.

### 4. Retraining path requires stronger promotion controls

A retraining workflow should not silently alter the public inference contract. A learned model requires immutable data/model manifests, evaluation gates, model-card updates, artifact hashes, and explicit promotion approval.

### 5. Release evidence can be stronger

Current semantic-tag release automation publishes a source archive and GHCR image. Future hardening should add source checksums, image digest evidence, signed attestations, final-image scanning, and immutable action pinning where practical.

## Promotion criteria — research model

Before adding predictive-quality claims, require:

- versioned dataset or manifest with provenance and license/use constraints
- patient-level leakage controls
- frozen train/validation/test protocol
- preprocessing fitted only on training data
- declared seed set or cross-validation design
- AUROC and AUPRC with confidence intervals
- sensitivity/specificity at pre-declared thresholds
- Brier score, calibration curve, and ECE
- subgroup performance with uncertainty
- baseline comparison
- model artifact hash and model card
- documented missing-data/OOD failure modes

## Promotion criteria — production-shaped service

Before adding stronger reliability claims, require:

- repeatable load harness with machine-readable output
- p50/p95/p99 latency, throughput, error rate, memory, CPU and concurrency
- readiness and graceful-shutdown behavior
- rollback evidence
- structured logging without sensitive payload capture
- dependency/container scan evidence tied to release
- immutable release digest and provenance

## Evidence rule

A passing CI badge proves automation completed for a commit. It does not prove clinical validity, fairness, calibration, patient safety, absence of security defects, or production-scale capacity.
