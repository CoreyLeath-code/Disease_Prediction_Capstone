"""Unit and failure-mode tests for the transparent screening baseline."""

from __future__ import annotations

import pytest

from src.risk_engine import PatientProfile, assess_profile, example_profiles


def test_example_profiles_cover_all_indicator_bands() -> None:
    assessments = {
        name: assess_profile(profile) for name, profile in example_profiles().items()
    }

    assert assessments["Lower indicator example"].category == "low"
    assert assessments["Moderate indicator example"].category == "moderate"
    assert assessments["Elevated indicator example"].category == "elevated"


def test_assessment_is_deterministic_and_serializable() -> None:
    profile = example_profiles()["Moderate indicator example"]

    first = assess_profile(profile)
    second = assess_profile(profile)

    assert first == second
    payload = first.to_dict()
    assert payload["score"] == first.score
    assert isinstance(payload["contributors"], list)
    assert "not a diagnosis" in str(payload["disclaimer"]).lower()


def test_no_thresholds_produces_explainable_low_result() -> None:
    profile = PatientProfile(
        age=30,
        bmi=22.0,
        systolic_bp=112.0,
        diastolic_bp=70.0,
        glucose=85.0,
        insulin=70.0,
        skin_thickness=20.0,
        cholesterol=170.0,
        hba1c=5.1,
    )

    assessment = assess_profile(profile)

    assert assessment.category == "low"
    assert assessment.score == 0.0
    assert assessment.contributors == (
        "no configured demo threshold was exceeded",
    )


def test_zero_optional_measurements_add_data_quality_note() -> None:
    profile = PatientProfile(
        age=30,
        bmi=22.0,
        systolic_bp=112.0,
        diastolic_bp=70.0,
        glucose=85.0,
        insulin=0.0,
        skin_thickness=0.0,
        cholesterol=170.0,
        hba1c=5.1,
    )

    assessment = assess_profile(profile)

    assert any("missing data" in note for note in assessment.educational_notes)


@pytest.mark.parametrize(
    "field,value",
    [
        ("age", 17),
        ("bmi", 81.0),
        ("glucose", float("nan")),
        ("cholesterol", 501.0),
        ("hba1c", 2.9),
    ],
)
def test_profile_rejects_invalid_values(field: str, value: float) -> None:
    values = {
        "age": 45,
        "bmi": 26.0,
        "systolic_bp": 122.0,
        "diastolic_bp": 78.0,
        "glucose": 95.0,
        "insulin": 80.0,
        "skin_thickness": 24.0,
        "cholesterol": 190.0,
        "hba1c": 5.4,
    }
    values[field] = value

    with pytest.raises(ValueError, match=field):
        PatientProfile(**values)


def test_profile_rejects_reversed_blood_pressure() -> None:
    with pytest.raises(ValueError, match="diastolic_bp"):
        PatientProfile(
            age=45,
            bmi=26.0,
            systolic_bp=80.0,
            diastolic_bp=90.0,
            glucose=95.0,
            insulin=80.0,
            skin_thickness=24.0,
            cholesterol=190.0,
            hba1c=5.4,
        )
