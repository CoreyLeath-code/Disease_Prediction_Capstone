"""Tests for the hardened supervisor compatibility workflow."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from agents.supervisor import DiagnosticSupervisorEngine


def test_low_indicator_profile_returns_transparent_state() -> None:
    engine = DiagnosticSupervisorEngine(use_llm_analyst=True)

    state = engine.process_patient_record(
        patient_id="SYNTHETIC-LOW",
        biomarkers={
            "cholesterol": 178.0,
            "fasting_blood_glucose": 88.0,
            "hba1c": 5.2,
        },
        s_bp=118.0,
        d_bp=74.0,
    )

    assert state.diagnostic_classification == "LOW_EDUCATIONAL_RISK_INDICATOR"
    assert state.compliance_risk_score == 0.0
    assert state.override_active is False
    assert state.execution_trace


def test_elevated_profile_receives_deterministic_safety_review() -> None:
    engine = DiagnosticSupervisorEngine(use_llm_analyst=True)

    state = engine.process_patient_record(
        patient_id="SYNTHETIC-ELEVATED",
        biomarkers={
            "cholesterol": 270.0,
            "fasting_blood_glucose": 170.0,
            "hba1c": 7.5,
        },
        s_bp=160.0,
        d_bp=98.0,
    )

    assert state.diagnostic_classification == "ELEVATED_EDUCATIONAL_RISK_INDICATOR"
    assert state.compliance_risk_score >= 6.0
    assert state.llm_compliance_analysis == "EDUCATIONAL_REVIEW_REQUIRED"
    assert "not a diagnosis" in state.llm_clinical_suggestions.lower()


def test_latency_guard_returns_explicit_fallback() -> None:
    engine = DiagnosticSupervisorEngine(
        use_llm_analyst=False,
        hard_deadline_ms=0.000001,
    )

    state = engine.process_patient_record(
        patient_id="SYNTHETIC-LATENCY",
        biomarkers={"cholesterol": 180.0},
        s_bp=120.0,
        d_bp=75.0,
    )

    assert state.override_active is True
    assert state.diagnostic_classification == "LATENCY_GUARD_FALLBACK"
    assert any("Latency guard opened" in entry for entry in state.execution_trace)


def test_unknown_biomarker_is_rejected() -> None:
    engine = DiagnosticSupervisorEngine()

    with pytest.raises(ValidationError, match="Unsupported biomarker"):
        engine.process_patient_record(
            patient_id="SYNTHETIC-INVALID",
            biomarkers={"full_name": 1.0},
            s_bp=120.0,
            d_bp=75.0,
        )


def test_reversed_blood_pressure_is_rejected() -> None:
    engine = DiagnosticSupervisorEngine()

    with pytest.raises(ValidationError, match="diastolic_bp"):
        engine.process_patient_record(
            patient_id="SYNTHETIC-INVALID",
            biomarkers={"cholesterol": 180.0},
            s_bp=80.0,
            d_bp=90.0,
        )
