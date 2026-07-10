"""FastAPI service for the Disease Prediction Capstone portfolio demonstration.

The service exposes a transparent educational risk-screening baseline. It does not
provide diagnoses, treatment recommendations, or clinically validated probabilities.
"""

from __future__ import annotations

from typing import Final, Literal

import prometheus_client as prom
from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import Counter, Histogram
from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.risk_engine import DISCLAIMER, PatientProfile, assess_profile, example_profiles

APP_VERSION: Final[str] = "2.0.0"

REQUEST_COUNTER = Counter(
    "disease_capstone_screening_requests_total",
    "Total educational screening requests.",
    ["category"],
)
ERROR_COUNTER = Counter(
    "disease_capstone_screening_errors_total",
    "Total educational screening request failures.",
)
LATENCY_HISTOGRAM = Histogram(
    "disease_capstone_screening_latency_seconds",
    "Educational screening request latency.",
)

app = FastAPI(
    title="Disease Prediction Capstone API",
    description=(
        "Validated educational risk-screening API for synthetic or non-identifiable "
        "data. Not a medical device and not intended for clinical decisions."
    ),
    version=APP_VERSION,
)


class ScreeningRequest(BaseModel):
    """Bounded input contract shared with the Streamlit demonstration."""

    model_config = ConfigDict(extra="forbid")

    age: int = Field(ge=18, le=120)
    bmi: float = Field(ge=10.0, le=80.0)
    systolic_bp: float = Field(ge=70.0, le=260.0)
    diastolic_bp: float = Field(ge=40.0, le=160.0)
    glucose: float = Field(ge=40.0, le=600.0)
    insulin: float = Field(ge=0.0, le=1_000.0)
    skin_thickness: float = Field(ge=0.0, le=100.0)
    cholesterol: float = Field(ge=80.0, le=500.0)
    hba1c: float = Field(ge=3.0, le=20.0)

    @model_validator(mode="after")
    def validate_blood_pressure_order(self) -> "ScreeningRequest":
        if self.diastolic_bp >= self.systolic_bp:
            raise ValueError("diastolic_bp must be lower than systolic_bp.")
        return self

    def to_profile(self) -> PatientProfile:
        """Convert the API schema into the domain input contract."""

        return PatientProfile(**self.model_dump())


class ScreeningResponse(BaseModel):
    """Explainable response with explicit non-clinical provenance."""

    score: float = Field(ge=0.0, le=100.0)
    category: Literal["low", "moderate", "elevated"]
    contributors: list[str]
    educational_notes: list[str]
    backend: str
    disclaimer: str
    api_version: str = APP_VERSION


class HealthResponse(BaseModel):
    """Lightweight liveness contract for containers and orchestrators."""

    status: Literal["healthy"] = "healthy"
    service: str = "disease-prediction-capstone-api"
    version: str = APP_VERSION
    clinical_use: bool = False


@app.get("/")
def root() -> dict[str, object]:
    """Return service identity and responsible-use metadata."""

    return {
        "status": "ok",
        "service": "Disease_Prediction_Capstone",
        "version": APP_VERSION,
        "clinical_use": False,
        "disclaimer": DISCLAIMER,
    }


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Return a dependency-free liveness response."""

    return HealthResponse()


@app.get("/metrics")
def metrics() -> Response:
    """Expose Prometheus metrics in the standard text format."""

    return Response(prom.generate_latest(), media_type=prom.CONTENT_TYPE_LATEST)


@app.get("/examples")
def examples() -> dict[str, dict[str, object]]:
    """Return fictional, reproducible profiles for API exploration."""

    return {
        name: {
            "profile": profile.__dict__,
            "assessment": assess_profile(profile).to_dict(),
        }
        for name, profile in example_profiles().items()
    }


@app.post("/predict", response_model=ScreeningResponse)
def predict(request: ScreeningRequest) -> ScreeningResponse:
    """Return a transparent educational screening result."""

    try:
        with LATENCY_HISTOGRAM.time():
            assessment = assess_profile(request.to_profile())
    except Exception:
        ERROR_COUNTER.inc()
        raise

    REQUEST_COUNTER.labels(category=assessment.category).inc()
    return ScreeningResponse(**assessment.to_dict())
