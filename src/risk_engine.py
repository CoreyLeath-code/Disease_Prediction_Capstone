"""Transparent, deterministic risk-screening utilities for the portfolio demo.

This module intentionally avoids diagnosing disease. It converts bounded, synthetic or
user-entered biomarker values into an explainable educational risk-indicator score.
The output is suitable for demonstrations, tests, and deployment smoke checks; it is
not validated for clinical use.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Final, Literal

DISCLAIMER: Final[str] = (
    "Educational portfolio demonstration only. This output is not a diagnosis, "
    "medical advice, or a substitute for evaluation by a licensed clinician."
)

RiskCategory = Literal["low", "moderate", "elevated"]


@dataclass(frozen=True, slots=True)
class PatientProfile:
    """Validated input contract for the educational screening engine."""

    age: int
    bmi: float
    systolic_bp: float
    diastolic_bp: float
    glucose: float
    insulin: float
    skin_thickness: float
    cholesterol: float
    hba1c: float

    def __post_init__(self) -> None:
        ranges: dict[str, tuple[float, float]] = {
            "age": (18.0, 120.0),
            "bmi": (10.0, 80.0),
            "systolic_bp": (70.0, 260.0),
            "diastolic_bp": (40.0, 160.0),
            "glucose": (40.0, 600.0),
            "insulin": (0.0, 1_000.0),
            "skin_thickness": (0.0, 100.0),
            "cholesterol": (80.0, 500.0),
            "hba1c": (3.0, 20.0),
        }

        for field_name, (minimum, maximum) in ranges.items():
            value = float(getattr(self, field_name))
            if not math.isfinite(value):
                raise ValueError(f"{field_name} must be finite.")
            if not minimum <= value <= maximum:
                raise ValueError(
                    f"{field_name} must be between {minimum:g} and {maximum:g}; "
                    f"received {value:g}."
                )

        if self.diastolic_bp >= self.systolic_bp:
            raise ValueError("diastolic_bp must be lower than systolic_bp.")


@dataclass(frozen=True, slots=True)
class RiskAssessment:
    """Serializable, explainable output from the deterministic screening baseline."""

    score: float
    category: RiskCategory
    contributors: tuple[str, ...]
    educational_notes: tuple[str, ...]
    backend: str = "deterministic-educational-screening-baseline"
    disclaimer: str = DISCLAIMER

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable representation."""

        payload = asdict(self)
        payload["contributors"] = list(self.contributors)
        payload["educational_notes"] = list(self.educational_notes)
        return payload


def _category_for(score: float) -> RiskCategory:
    if score >= 55.0:
        return "elevated"
    if score >= 25.0:
        return "moderate"
    return "low"


def assess_profile(profile: PatientProfile) -> RiskAssessment:
    """Calculate an explainable educational score from common risk indicators.

    The weights are intentionally simple and transparent. They are not a trained
    clinical model and must not be interpreted as disease probabilities.
    """

    score = 0.0
    contributors: list[str] = []
    notes: list[str] = []

    if profile.glucose >= 126.0:
        score += 25.0
        contributors.append("glucose is in the highest demo threshold band")
    elif profile.glucose >= 100.0:
        score += 12.0
        contributors.append("glucose is above the demo reference band")

    if profile.hba1c >= 6.5:
        score += 25.0
        contributors.append("HbA1c is in the highest demo threshold band")
    elif profile.hba1c >= 5.7:
        score += 12.0
        contributors.append("HbA1c is above the demo reference band")

    if profile.systolic_bp >= 140.0 or profile.diastolic_bp >= 90.0:
        score += 18.0
        contributors.append("blood pressure is in the highest demo threshold band")
    elif profile.systolic_bp >= 130.0 or profile.diastolic_bp >= 80.0:
        score += 9.0
        contributors.append("blood pressure is above the demo reference band")

    if profile.bmi >= 30.0:
        score += 12.0
        contributors.append("BMI is in the highest demo threshold band")
    elif profile.bmi >= 25.0:
        score += 6.0
        contributors.append("BMI is above the demo reference band")

    if profile.cholesterol >= 240.0:
        score += 10.0
        contributors.append("cholesterol is in the highest demo threshold band")
    elif profile.cholesterol >= 200.0:
        score += 5.0
        contributors.append("cholesterol is above the demo reference band")

    if profile.age >= 65:
        score += 5.0
        contributors.append("age contributes to the educational screening score")
    elif profile.age >= 45:
        score += 3.0
        contributors.append("age modestly contributes to the educational screening score")

    # Insulin and skin-thickness values remain part of the validated feature contract
    # but are not assigned standalone heuristic weights without a trained/calibrated model.
    if profile.insulin == 0.0 or profile.skin_thickness == 0.0:
        notes.append(
            "A zero insulin or skin-thickness value may represent missing data in some datasets."
        )

    score = min(round(score, 1), 100.0)
    category = _category_for(score)

    if not contributors:
        contributors.append("no configured demo threshold was exceeded")

    notes.extend(
        [
            "The score is a transparent rule-based demonstration, not a calibrated probability.",
            "Only synthetic or non-identifiable data should be entered into this public demo.",
        ]
    )

    return RiskAssessment(
        score=score,
        category=category,
        contributors=tuple(contributors),
        educational_notes=tuple(notes),
    )


def example_profiles() -> dict[str, PatientProfile]:
    """Return reproducible, fictional profiles for the UI and documentation."""

    return {
        "Lower indicator example": PatientProfile(
            age=34,
            bmi=23.5,
            systolic_bp=118.0,
            diastolic_bp=74.0,
            glucose=88.0,
            insulin=72.0,
            skin_thickness=22.0,
            cholesterol=178.0,
            hba1c=5.2,
        ),
        "Moderate indicator example": PatientProfile(
            age=52,
            bmi=28.4,
            systolic_bp=134.0,
            diastolic_bp=84.0,
            glucose=112.0,
            insulin=118.0,
            skin_thickness=30.0,
            cholesterol=216.0,
            hba1c=5.9,
        ),
        "Elevated indicator example": PatientProfile(
            age=67,
            bmi=34.2,
            systolic_bp=154.0,
            diastolic_bp=96.0,
            glucose=162.0,
            insulin=185.0,
            skin_thickness=38.0,
            cholesterol=266.0,
            hba1c=7.4,
        ),
    }
