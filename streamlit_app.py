"""Streamlit Community Cloud dashboard for the Disease Prediction Capstone.

The application is an educational engineering demonstration. It accepts only
synthetic or non-identifiable values and clearly labels its deterministic,
rule-based output as non-clinical.
"""

from __future__ import annotations

import json
from dataclasses import asdict

import pandas as pd
import streamlit as st

from src.risk_engine import DISCLAIMER, PatientProfile, assess_profile, example_profiles


@st.cache_data(show_spinner=False)
def get_examples() -> dict[str, dict[str, float | int]]:
    """Return serializable fictional profiles for the selector."""

    return {name: asdict(profile) for name, profile in example_profiles().items()}


def _apply_example(name: str) -> None:
    for field_name, value in get_examples()[name].items():
        st.session_state[field_name] = value


def render_sidebar() -> None:
    """Render responsible-use and engineering context."""

    with st.sidebar:
        st.title("🩺 Capstone Controls")
        st.warning(DISCLAIMER)
        st.markdown(
            """
### Public-demo contract
- Use synthetic or non-identifiable values only.
- No data is intentionally persisted by the app.
- Results are transparent threshold indicators, not probabilities.
- The demo is not validated for diagnosis or treatment decisions.
"""
        )

        st.subheader("Fictional examples")
        selected = st.selectbox("Load a preset", tuple(get_examples()))
        if st.button("Load selected example", use_container_width=True):
            _apply_example(selected)
            st.rerun()

        st.divider()
        st.markdown(
            "[View source on GitHub](https://github.com/CoreyLeath-code/Disease_Prediction_Capstone)"
        )
        st.caption("L6 nine-tier deployment-hygiene portfolio implementation")


def render_input_form() -> tuple[PatientProfile | None, bool]:
    """Render bounded feature controls and return a validated profile on submit."""

    with st.form("screening-form"):
        left, middle, right = st.columns(3)

        with left:
            age = st.number_input("Age", 18, 120, key="age", value=45)
            bmi = st.number_input(
                "BMI", 10.0, 80.0, key="bmi", value=26.0, step=0.1
            )
            cholesterol = st.number_input(
                "Total cholesterol (mg/dL)",
                80.0,
                500.0,
                key="cholesterol",
                value=190.0,
                step=1.0,
            )

        with middle:
            systolic_bp = st.number_input(
                "Systolic blood pressure (mmHg)",
                70.0,
                260.0,
                key="systolic_bp",
                value=122.0,
                step=1.0,
            )
            diastolic_bp = st.number_input(
                "Diastolic blood pressure (mmHg)",
                40.0,
                160.0,
                key="diastolic_bp",
                value=78.0,
                step=1.0,
            )
            glucose = st.number_input(
                "Glucose (mg/dL)",
                40.0,
                600.0,
                key="glucose",
                value=95.0,
                step=1.0,
            )

        with right:
            hba1c = st.number_input(
                "HbA1c (%)", 3.0, 20.0, key="hba1c", value=5.4, step=0.1
            )
            insulin = st.number_input(
                "Insulin (demo units)",
                0.0,
                1_000.0,
                key="insulin",
                value=80.0,
                step=1.0,
            )
            skin_thickness = st.number_input(
                "Skin thickness (demo units)",
                0.0,
                100.0,
                key="skin_thickness",
                value=24.0,
                step=1.0,
            )

        submitted = st.form_submit_button(
            "Run educational screening", type="primary", use_container_width=True
        )

    if not submitted:
        return None, False

    try:
        profile = PatientProfile(
            age=int(age),
            bmi=float(bmi),
            systolic_bp=float(systolic_bp),
            diastolic_bp=float(diastolic_bp),
            glucose=float(glucose),
            insulin=float(insulin),
            skin_thickness=float(skin_thickness),
            cholesterol=float(cholesterol),
            hba1c=float(hba1c),
        )
    except ValueError as exc:
        st.error(str(exc))
        return None, True

    return profile, True


def render_assessment(profile: PatientProfile) -> None:
    """Render explainable score, evidence, and downloadable non-clinical output."""

    assessment = assess_profile(profile)
    category_label = assessment.category.title()

    st.subheader("Educational screening result")
    metric1, metric2, metric3 = st.columns(3)
    metric1.metric("Indicator score", f"{assessment.score:.1f} / 100")
    metric2.metric("Indicator band", category_label)
    metric3.metric("Backend", "Deterministic baseline")

    st.progress(min(assessment.score / 100.0, 1.0))

    if assessment.category == "elevated":
        st.error(
            "Several configured demonstration thresholds were exceeded. "
            "This is not a diagnosis."
        )
    elif assessment.category == "moderate":
        st.warning(
            "Some configured demonstration thresholds were exceeded. "
            "This is not a diagnosis."
        )
    else:
        st.success(
            "Few or no configured demonstration thresholds were exceeded. "
            "This does not establish health status."
        )

    left, right = st.columns([3, 2])
    with left:
        st.markdown("#### Explainability evidence")
        for contributor in assessment.contributors:
            st.write(f"- {contributor}")

        st.markdown("#### Responsible-use notes")
        for note in assessment.educational_notes:
            st.write(f"- {note}")
        st.info(assessment.disclaimer)

    with right:
        st.markdown("#### Submitted feature snapshot")
        feature_frame = pd.DataFrame(
            {
                "feature": list(asdict(profile).keys()),
                "value": list(asdict(profile).values()),
            }
        )
        st.dataframe(feature_frame, hide_index=True, use_container_width=True)

    export_payload = {
        "profile": asdict(profile),
        "assessment": assessment.to_dict(),
    }
    st.download_button(
        "Download demonstration result (JSON)",
        data=json.dumps(export_payload, indent=2),
        file_name="disease_capstone_demo_result.json",
        mime="application/json",
    )


def render_engineering_evidence() -> None:
    """Show architecture and deployment controls without overstating maturity."""

    st.divider()
    st.subheader("Engineering evidence")
    tab1, tab2, tab3 = st.tabs(
        ["Architecture", "Nine-tier hygiene", "Extended Q&A"]
    )

    with tab1:
        st.graphviz_chart(
            """
digraph Capstone {
    rankdir=LR;
    node [shape=box, style=rounded];
    User -> Streamlit;
    Streamlit -> Validation;
    Validation -> RiskEngine;
    RiskEngine -> Explainability;
    Explainability -> Result;
    API -> Validation;
    CI -> Tests;
    CI -> StreamlitSmoke;
    CI -> ContainerSmoke;
}
""",
            use_container_width=True,
        )
        st.caption(
            "The public demo and API share the same validated deterministic domain engine."
        )

    with tab2:
        tiers = {
            "1. Source hygiene": "Typed contracts, bounded inputs, Ruff, compile checks",
            "2. Test engineering": "Python matrix, domain/API tests, coverage, JUnit",
            "3. Static quality": "CodeQL and high-confidence correctness gates",
            "4. Security engineering": "Gitleaks, Trivy, non-root container, safe errors",
            "5. Supply-chain hygiene": "Dependabot, pip-audit, CycloneDX SBOM",
            "6. Reproducible runtime": "Pinned manifests, multi-stage image, Python pin",
            "7. Continuous delivery": "Streamlit and container health smoke tests",
            "8. Release engineering": "Semantic tags, GitHub Releases, GHCR publishing",
            "9. Operational governance": "Security policy, changelog, ownership, runbooks",
        }
        for tier, evidence in tiers.items():
            st.markdown(f"**{tier}** — {evidence}")

    with tab3:
        with st.expander("Is this application a diagnostic medical device?"):
            st.write(
                "No. It is an educational software-engineering portfolio demonstration "
                "and has not been clinically validated or approved for patient care."
            )
        with st.expander("Why use a deterministic baseline in the public demo?"):
            st.write(
                "It keeps the deployment reproducible and explainable without requiring "
                "private datasets, serialized model artifacts, GPUs, or external APIs."
            )
        with st.expander("What would be required before real clinical use?"):
            st.write(
                "Independent validation, representative data, bias and calibration studies, "
                "privacy controls, clinical governance, regulatory review, monitoring, and "
                "licensed professional oversight would all be required."
            )
        with st.expander("Why are model provenance and disclaimers explicit?"):
            st.write(
                "Users should be able to distinguish a transparent educational heuristic "
                "from a trained, calibrated, clinically evaluated model."
            )


def main() -> None:
    """Render the complete Streamlit application."""

    st.set_page_config(
        page_title="Disease Prediction Capstone Demo",
        page_icon="🩺",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    render_sidebar()

    st.title("🩺 Disease Prediction Capstone")
    st.subheader("Explainable educational risk-screening and deployment-hygiene demo")
    st.write(
        "Explore validated input contracts, transparent rule-based scoring, "
        "explainability evidence, and production-oriented deployment controls."
    )
    st.warning(DISCLAIMER)

    profile, submitted = render_input_form()
    if profile is not None:
        render_assessment(profile)
    elif not submitted:
        st.info("Load a fictional preset or enter synthetic values, then run the demo.")

    render_engineering_evidence()

    st.divider()
    st.caption(
        "Portfolio project by Corey Leath · Streamlit · FastAPI · Pydantic · "
        "Docker · GitHub Actions · L6 nine-tier deployment hygiene"
    )


if __name__ == "__main__":
    main()
