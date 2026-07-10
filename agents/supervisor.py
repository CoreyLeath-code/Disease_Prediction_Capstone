"""Supervisor orchestration for the educational clinical-risk portfolio demo."""

from __future__ import annotations

import time
from typing import Final

from .guards import DiagnosticCircuitBreaker, DiagnosticDeadlineException
from .state import DiagnosticState

_EDUCATIONAL_DISCLAIMER: Final[str] = (
    "Educational demonstration only; this output is not a diagnosis or medical advice."
)


class DiagnosticSupervisorEngine:
    """Coordinate validation, transparent scoring, review, and latency telemetry.

    The original capstone used diagnostic terminology. This hardened implementation
    preserves the public class interface while clearly operating as a deterministic,
    non-clinical educational screening workflow.
    """

    def __init__(
        self,
        use_llm_analyst: bool = True,
        hard_deadline_ms: float = 50.0,
    ) -> None:
        self.breaker = DiagnosticCircuitBreaker(hard_deadline_ms=hard_deadline_ms)
        # Retained as a compatibility flag. No external LLM call is made.
        self.use_llm_analyst = bool(use_llm_analyst)

    def process_patient_record(
        self,
        patient_id: str,
        biomarkers: dict[str, float],
        s_bp: float,
        d_bp: float,
    ) -> DiagnosticState:
        """Process one synthetic/non-identifiable profile into an explainable state."""

        self.breaker.reset()
        state = DiagnosticState(
            patient_id=patient_id,
            biomarker_features=biomarkers,
            systolic_bp=s_bp,
            diastolic_bp=d_bp,
        ).append_trace("Validated non-identifiable screening inputs.")

        started = time.perf_counter()
        try:
            score, reasons = self._calculate_indicator_score(state)
            category = self._classification_for(score)
            state = state.model_copy(
                update={
                    "compliance_risk_score": score,
                    "risk_probability": round(score / 10.0, 3),
                    "diagnostic_classification": category,
                }
            )
            for reason in reasons:
                state = state.append_trace(reason)

            if self.use_llm_analyst and score >= 6.0:
                state = self._run_educational_safety_review(state)

            elapsed_ms = (time.perf_counter() - started) * 1_000.0
            self.breaker.evaluate_execution_timing(elapsed_ms)
            return state.model_copy(update={"processing_latency_ms": elapsed_ms})

        except DiagnosticDeadlineException as exc:
            elapsed_ms = (time.perf_counter() - started) * 1_000.0
            return state.model_copy(
                update={
                    "override_active": True,
                    "diagnostic_classification": "LATENCY_GUARD_FALLBACK",
                    "llm_clinical_suggestions": (
                        "The demonstration latency budget was exceeded. "
                        "No screening interpretation should be relied upon."
                    ),
                    "processing_latency_ms": elapsed_ms,
                }
            ).append_trace(f"Latency guard opened: {exc}")

    @staticmethod
    def _calculate_indicator_score(state: DiagnosticState) -> tuple[float, tuple[str, ...]]:
        score = 0.0
        reasons: list[str] = []
        biomarkers = state.biomarker_features

        glucose = biomarkers.get("fasting_blood_glucose")
        if glucose is not None:
            if glucose >= 126.0:
                score += 2.5
                reasons.append("Glucose exceeded the highest configured demo threshold.")
            elif glucose >= 100.0:
                score += 1.2
                reasons.append("Glucose exceeded the configured demo reference band.")

        hba1c = biomarkers.get("hba1c")
        if hba1c is not None:
            if hba1c >= 6.5:
                score += 2.5
                reasons.append("HbA1c exceeded the highest configured demo threshold.")
            elif hba1c >= 5.7:
                score += 1.2
                reasons.append("HbA1c exceeded the configured demo reference band.")

        if state.systolic_bp >= 140.0 or state.diastolic_bp >= 90.0:
            score += 2.0
            reasons.append("Blood pressure exceeded the highest configured demo threshold.")
        elif state.systolic_bp >= 130.0 or state.diastolic_bp >= 80.0:
            score += 1.0
            reasons.append("Blood pressure exceeded the configured demo reference band.")

        cholesterol = biomarkers.get("cholesterol")
        if cholesterol is not None:
            if cholesterol >= 240.0:
                score += 1.5
                reasons.append("Cholesterol exceeded the highest configured demo threshold.")
            elif cholesterol >= 200.0:
                score += 0.7
                reasons.append("Cholesterol exceeded the configured demo reference band.")

        if not reasons:
            reasons.append("No configured educational threshold was exceeded.")

        return min(round(score, 2), 10.0), tuple(reasons)

    @staticmethod
    def _classification_for(score: float) -> str:
        if score >= 6.0:
            return "ELEVATED_EDUCATIONAL_RISK_INDICATOR"
        if score >= 2.5:
            return "MODERATE_EDUCATIONAL_RISK_INDICATOR"
        return "LOW_EDUCATIONAL_RISK_INDICATOR"

    @staticmethod
    def _run_educational_safety_review(state: DiagnosticState) -> DiagnosticState:
        """Add a deterministic safety notice without making an external AI claim."""

        return state.model_copy(
            update={
                "llm_compliance_analysis": "EDUCATIONAL_REVIEW_REQUIRED",
                "llm_clinical_suggestions": (
                    "One or more demo thresholds were exceeded. "
                    f"{_EDUCATIONAL_DISCLAIMER}"
                ),
            }
        ).append_trace("Deterministic safety reviewer added the required disclaimer.")
