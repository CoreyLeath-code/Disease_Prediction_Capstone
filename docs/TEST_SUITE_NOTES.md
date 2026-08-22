# Test Suite Repair Notes

The repository's supported public runtime is the deterministic educational screening baseline in `src/risk_engine.py`, not a trained clinical classifier.

The previous `tests/test_model.py` created an unrelated scikit-learn `RandomForestClassifier` at collection time. A full `pytest tests` run could therefore fail in a clean supported development environment because NumPy/scikit-learn are not part of `requirements-dev.txt`, even though the normal CI command silently skipped that test file.

This repair aligns the test suite with the actual public runtime and closes the CI blind spot:

- `tests/test_model.py` now validates the real deterministic screening baseline, backend provenance, disclaimer, ordering of fictional examples, bounded scores, and explainability evidence.
- CI now lints `tests/test_model.py` and runs `pytest tests -v` rather than an allow-list of only three test modules.
- No clinical-model accuracy or disease-prediction quality claim is introduced.

A future trained model should receive its own isolated dependency set, immutable dataset/model manifests, leakage-safe evaluation protocol, and model-quality test/evaluation suite rather than reusing these baseline contract tests.
