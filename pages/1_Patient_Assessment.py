
import streamlit as st
import pandas as pd
import joblib
from datetime import date
from pathlib import Path

# --------------------------------------------------
# PATHS AND CONFIGURATION
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "models" / "diabetes_model.joblib"

st.set_page_config(
    page_title="Patient Assessment | Diabetes Risk",
    page_icon="🩺",
    layout="wide",
)

# --------------------------------------------------
# STYLING
# --------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #faf6f0;
    }
    h1, h2, h3 {
        color: #684832;
    }
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #eadbca;
        padding: 16px;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------
@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)


model = load_model()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.title("🩺 Diabetes Care")
    st.caption("AI-Powered Diabetes Risk Assessment")
    st.divider()
    st.info(
        "This educational tool estimates risk from entered "
        "measurements. It cannot diagnose diabetes or replace "
        "a qualified healthcare professional."
    )

# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------
st.title("Patient Assessment")
st.write(
    "Enter the available patient information to generate an "
    "educational diabetes risk estimate."
)

if model is None:
    st.error(
        "The trained model was not found. From your project "
        "root folder, run: python -m models.train_model"
    )
    st.stop()

st.divider()

# --------------------------------------------------
# PATIENT INPUT FORM
# --------------------------------------------------
with st.form("patient_assessment_form"):
    st.subheader("1. Patient Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        patient_name = st.text_input("Patient name or reference ID")

    with col2:
        assessment_date = st.date_input(
            "Assessment date",
            value=date.today(),
        )

    with col3:
        age = st.number_input(
            "Age (years)",
            min_value=1,
            max_value=120,
            value=30,
        )

    st.subheader("2. Health Measurements")

    col1, col2 = st.columns(2)

    with col1:
        pregnancies = st.number_input(
            "Number of pregnancies",
            min_value=0,
            max_value=20,
            value=0,
        )
        glucose = st.number_input(
            "Glucose level",
            min_value=0.0,
            max_value=500.0,
            value=120.0,
            help="Use the measurement provided by the healthcare professional.",
        )
        blood_pressure = st.number_input(
            "Diastolic blood pressure",
            min_value=0.0,
            max_value=200.0,
            value=70.0,
        )
        skin_thickness = st.number_input(
            "Skin thickness",
            min_value=0.0,
            max_value=150.0,
            value=20.0,
            help="Enter 0 if unavailable; the model pipeline handles missing values.",
        )

    with col2:
        insulin = st.number_input(
            "Insulin level",
            min_value=0.0,
            max_value=1000.0,
            value=80.0,
            help="Enter 0 if unavailable; the model pipeline handles missing values.",
        )
        bmi = st.number_input(
            "BMI",
            min_value=0.0,
            max_value=100.0,
            value=25.0,
        )
        pedigree = st.number_input(
            "Diabetes pedigree function",
            min_value=0.0,
            max_value=5.0,
            value=0.5,
            help="Enter the dataset-compatible value if known.",
        )

    st.subheader("3. Lifestyle Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        family_history = st.selectbox(
            "Family history of diabetes",
            ["Unknown", "Yes", "No"],
        )

    with col2:
        physical_activity = st.selectbox(
            "Physical activity",
            ["Unknown", "Low", "Moderate", "High"],
        )

    with col3:
        stress_level = st.selectbox(
            "Self-reported stress",
            ["Unknown", "Low", "Moderate", "High"],
        )

    food_habits = st.selectbox(
        "General food habits",
        [
            "Not specified",
            "Balanced",
            "High in processed foods",
            "High in sugary foods",
            "Other",
        ],
    )

    submitted = st.form_submit_button(
        "Assess Diabetes Risk",
        type="primary",
        width="stretch",
    )

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------
if submitted:
    if not patient_name.strip():
        st.error("Please enter a patient name or reference ID.")
        st.stop()

    if glucose <= 0:
        st.error("Enter a valid glucose measurement greater than zero.")
        st.stop()

    if blood_pressure <= 0:
        st.error("Enter a valid blood pressure measurement greater than zero.")
        st.stop()

    if bmi <= 0:
        st.error("Enter a valid BMI greater than zero.")
        st.stop()

    # The model was trained using these feature names.
    input_data = pd.DataFrame(
        [
            {
                "Pregnancies": pregnancies,
                "Glucose": glucose,
                "BloodPressure": blood_pressure,
                "SkinThickness": skin_thickness,
                "Insulin": insulin,
                "BMI": bmi,
                "DiabetesPedigreeFunction": pedigree,
                "Age": age,
            }
        ]
    )

    try:
        prediction = int(model.predict(input_data)[0])

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(input_data)[0]
            classes = list(model.classes_)
            positive_index = classes.index(1) if 1 in classes else None

            risk_probability = (
                float(probabilities[positive_index])
                if positive_index is not None
                else None
            )
        else:
            risk_probability = None

    except Exception as error:
        st.error(f"Prediction failed: {error}")
        st.stop()

    st.divider()
    st.header("Assessment Results")

    if risk_probability is not None:
        metric_col1, metric_col2 = st.columns(2)

        with metric_col1:
            st.metric(
                "Model-estimated probability",
                f"{risk_probability * 100:.1f}%",
            )

        with metric_col2:
            st.metric(
                "Model classification",
                "Higher predicted risk" if prediction == 1
                else "Lower predicted risk",
            )
    else:
        st.metric(
            "Model classification",
            "Higher predicted risk" if prediction == 1
            else "Lower predicted risk",
        )

    if prediction == 1:
        st.warning(
            "The model classified this assessment in the positive "
            "class. This is not a diagnosis. Please consult a "
            "qualified healthcare professional for appropriate "
            "testing and interpretation."
        )
    else:
        st.success(
            "The model classified this assessment in the negative "
            "class. This does not rule out diabetes or guarantee "
            "that the person is healthy. Seek medical advice when "
            "appropriate."
        )

    st.subheader("Recorded Assessment Details")

    profile_data = {
        "Assessment Factor": [
            "Patient reference",
            "Assessment date",
            "Age",
            "Pregnancies",
            "Glucose",
            "Diastolic blood pressure",
            "Skin thickness",
            "Insulin",
            "BMI",
            "Diabetes pedigree function",
            "Family history",
            "Physical activity",
            "Stress level",
            "Food habits",
            "Model classification",
        ],
        "Recorded Information": [
            patient_name.strip(),
            assessment_date.isoformat(),
            str(age),
            str(int(pregnancies)),
            str(glucose),
            str(blood_pressure),
            str(skin_thickness),
            str(insulin),
            str(bmi),
            str(pedigree),
            family_history,
            physical_activity,
            stress_level,
            food_habits,
            "Higher predicted risk" if prediction == 1
            else "Lower predicted risk",
        ],
    }

    profile_df = pd.DataFrame(profile_data).astype(str)

    st.dataframe(
        profile_df,
        width="stretch",
        hide_index=True,
    )

    # Downloadable assessment summary
    report_lines = [
        "AI-POWERED DIABETES RISK ASSESSMENT",
        "=" * 40,
        f"Patient reference: {patient_name.strip()}",
        f"Assessment date: {assessment_date.isoformat()}",
        "",
        "HEALTH MEASUREMENTS",
        f"Age: {age}",
        f"Pregnancies: {pregnancies}",
        f"Glucose: {glucose}",
        f"Diastolic blood pressure: {blood_pressure}",
        f"Skin thickness: {skin_thickness}",
        f"Insulin: {insulin}",
        f"BMI: {bmi}",
        f"Diabetes pedigree function: {pedigree}",
        "",
        "LIFESTYLE INFORMATION",
        f"Family history: {family_history}",
        f"Physical activity: {physical_activity}",
        f"Stress level: {stress_level}",
        f"Food habits: {food_habits}",
        "",
        "MODEL OUTPUT",
        (
            f"Estimated positive-class probability: "
            f"{risk_probability * 100:.1f}%"
            if risk_probability is not None
            else "Probability unavailable"
        ),
        (
            "Classification: Higher predicted risk"
            if prediction == 1
            else "Classification: Lower predicted risk"
        ),
        "",
        "IMPORTANT DISCLAIMER",
        "This report is for educational purposes only. It is not a",
        "medical diagnosis or a prescription. Consult a qualified",
        "healthcare professional for clinical assessment.",
    ]

    st.download_button(
        "Download Assessment Report",
        data="\n".join(report_lines),
        file_name=f"diabetes_assessment_{assessment_date.isoformat()}.txt",
        mime="text/plain",
        width="stretch",
    )

    st.caption(
        "Privacy note: This page does not save assessment details "
        "to a patient database."
    )

st.divider()
st.caption(
    "Educational prototype only | Not for diagnosis, treatment, "
    "or medication prescribing."
)
