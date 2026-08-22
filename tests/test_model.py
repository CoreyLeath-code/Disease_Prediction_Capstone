"""Regression tests for the verified public screening baseline.

This repository does not currently ship a trained disease-prediction model. The legacy
version of this file created an unrelated scikit-learn RandomForest during test collection,
which made a full `pytest` run depend on packages that are not part of the supported runtime
and implied model-quality evidence that the public application does not provide.

These tests instead exercise the actual deterministic, explainable baseline used by the
public API and Streamlit surfaces.
"""

from __future__ import annotations

from src.risk_engine import DISCLAIMER, assess_profile, example_profiles


def test_public_baseline_is_deterministic() -> None:
    profile = example_profiles()["Moderate indicator example"]

    first = assess_profile(profile)
    second = assess_profile(profile)

    assert first == second


def test_public_baseline_exposes_nonclinical_provenance() -> None:
    assessment = assess_profile(example_profiles()["Elevated indicator example"])

    assert assessment.backend == "deterministic-educational-screening-baseline"
    assert assessment.disclaimer == DISCLAIMER
    assert "not a diagnosis" in assessment.disclaimer.lower()


def test_example_profiles_cover_expected_indicator_ordering() -> None:
    examples = example_profiles()

    low = assess_profile(examples["Lower indicator example"])
    moderate = assess_profile(examples["Moderate indicator example"])
    elevated = assess_profile(examples["Elevated indicator example"])

    assert low.category == "low"
    assert moderate.category == "moderate"
    assert elevated.category == "elevated"
    assert low.score < moderate.score < elevated.score


def test_public_score_is_bounded_and_explainable() -> None:
    for profile in example_profiles().values():
        assessment = assess_profile(profile)

        assert 0.0 <= assessment.score <= 100.0
        assert assessment.contributors
        assert assessment.educational_notes
