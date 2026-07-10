"""Immutable orchestration state for the educational clinical-risk demo."""

from __future__ import annotations

import math
from typing import Final

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

_ALLOWED_BIOMARKERS: Final[set[str]] = {
    "cholesterol",
    "fasting_blood_glucose",
    "hba1c",
    "bmi",
    "insulin",
    "skin_thickness",
}


class DiagnosticState(BaseModel):
    """Validated, immutable snapshot passed through the supervisor workflow.

    The name is retained for backwards compatibility with the original capstone,
    but the state represents an educational risk-screening workflow—not a medical
    diagnosis or a clinically validated decision-support system.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    patient_id: str = Field(min_length=1, max_length=64)
    biomarker_features: dict[str, float] = Field(default_factory=dict)
    systolic_bp: float = Field(ge=70.0, le=260.0)
    diastolic_bp: float = Field(ge=40.0, le=160.0)

    risk_probability: float = Field(default=0.0, ge=0.0, le=1.0)
    diagnostic_classification: str | None = None
    compliance_risk_score: float = Field(default=0.0, ge=0.0, le=10.0)

    llm_compliance_analysis: str | None = None
    llm_clinical_suggestions: str | None = None
    override_active: bool = False

    processing_latency_ms: float = Field(default=0.0, ge=0.0)
    execution_trace: tuple[str, ...] = Field(default_factory=tuple)

    @field_validator("patient_id")
    @classmethod
    def normalize_patient_id(cls, value: str) -> str:
        """Strip display identifiers and reject empty values."""

        normalized = value.strip()
        if not normalized:
            raise ValueError("patient_id must not be blank.")
        return normalized

    @field_validator("biomarker_features")
    @classmethod
    def validate_biomarkers(cls, values: dict[str, float]) -> dict[str, float]:
        """Reject unknown, non-finite, and implausible demonstration values."""

        normalized: dict[str, float] = {}
        for key, raw_value in values.items():
            if key not in _ALLOWED_BIOMARKERS:
                raise ValueError(f"Unsupported biomarker field: {key}")
            value = float(raw_value)
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{key} must be a finite, non-negative number.")
            normalized[key] = value
        return normalized

    @model_validator(mode="after")
    def validate_blood_pressure_order(self) -> "DiagnosticState":
        """Require physiologically ordered blood-pressure values."""

        if self.diastolic_bp >= self.systolic_bp:
            raise ValueError("diastolic_bp must be lower than systolic_bp.")
        return self

    def append_trace(self, message: str) -> "DiagnosticState":
        """Return a new immutable snapshot with one sanitized trace message."""

        clean_message = " ".join(message.strip().split())
        if not clean_message:
            return self
        return self.model_copy(
            update={"execution_trace": (*self.execution_trace, clean_message)}
        )
