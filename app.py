from pathlib import Path

import streamlit as st

# --------------------------------------------------
# PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_ROOT / "models" / "diabetes_model.joblib"

st.set_page_config(
    page_title="Diabetes Risk Assessment",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# AESTHETIC THEME
# --------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background-color: #F7F0E3;
        color: #37332F;
    }

    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    html, body, [class*="css"] {
        font-family: "Aptos", "Segoe UI", sans-serif;
        color: #37332F;
    }

    h1, h2, h3 {
        color: #37332F !important;
        font-weight: 500 !important;
        letter-spacing: -0.5px;
    }

    p, label, li {
        color: #514940;
    }

    [data-testid="stSidebar"] {
        background-color: #E5D3B3;
        border-right: 1px solid #D2BFA0;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #37332F !important;
    }

    .hero-header {
        padding: 1.5rem 0 2rem 0;
        border-bottom: 1px solid #D9C8AF;
        margin-bottom: 1.8rem;
    }

    .hero-eyebrow {
        color: #A94442;
        font-size: 0.75rem;
        font-weight: 650;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
    }

    .hero-header h1 {
        color: #37332F !important;
        font-size: clamp(2.5rem, 5vw, 4.2rem);
        font-weight: 500 !important;
        letter-spacing: -2px;
        line-height: 1.1;
        margin: 0;
        padding: 0;
    }

    .hero-accent {
        width: 58px;
        height: 3px;
        background-color: #A94442;
        margin: 1.5rem 0 1rem 0;
        border-radius: 3px;
    }

    .hero-subtitle {
        color: #75695B;
        font-size: 1rem;
        line-height: 1.8;
        max-width: 680px;
        margin: 0;
    }

    .section-eyebrow {
        color: #8A7760;
        font-size: 0.72rem;
        font-weight: 650;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    .metric-card {
        background-color: #FBF7EF;
        border: 1px solid #DFD0BA;
        border-radius: 14px;
        padding: 1.35rem 1.4rem;
        min-height: 135px;
        box-shadow: 0 3px 12px rgba(75, 57, 36, 0.035);
    }

    .metric-label {
        color: #796D5E;
        font-size: 0.82rem;
        letter-spacing: 0.4px;
        margin-bottom: 0.8rem;
    }

    .metric-value {
        color: #37332F;
        font-size: 2rem;
        font-weight: 550;
        letter-spacing: -0.8px;
    }

    .metric-note {
        color: #817567;
        font-size: 0.78rem;
        margin-top: 0.5rem;
    }

    .module-card {
        background-color: #FBF7EF;
        border: 1px solid #DFD0BA;
        border-radius: 14px;
        padding: 1.5rem;
        min-height: 180px;
        margin-bottom: 0.8rem;
        transition: border-color 0.2s ease;
    }

    .module-number {
        color: #A94442;
        font-size: 0.75rem;
        font-weight: 650;
        letter-spacing: 2px;
        margin-bottom: 0.9rem;
    }

    .module-title {
        color: #37332F;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.6rem;
    }

    .module-description {
        color: #75695B;
        font-size: 0.9rem;
        line-height: 1.7;
    }

    .stButton > button {
        background-color: #A94442;
        color: #FFF9F0;
        border: 1px solid #A94442;
        border-radius: 8px;
        padding: 0.6rem 1.1rem;
        font-weight: 550;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background-color: #873936;
        border-color: #873936;
        color: #FFFFFF;
    }

    .stButton > button:focus {
        box-shadow: 0 0 0 2px #F7F0E3, 0 0 0 4px #A94442;
    }

    .stTextInput input,
    .stNumberInput input,
    .stDateInput input,
    .stTextArea textarea {
        background-color: #FBF7EF;
        color: #37332F;
        border: 1px solid #CDBB9E;
        border-radius: 8px;
    }

    div[data-baseweb="select"] > div {
        background-color: #E5D3B3;
        color: #37332F;
        border-color: #CDBB9E;
        border-radius: 8px;
    }

    div[role="listbox"] {
        background-color: #E5D3B3;
    }

    div[role="option"] {
        color: #37332F;
    }

    div[role="option"]:hover {
        background-color: #D5BE9A;
    }

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    hr {
        border-color: #D9C8AF;
    }

    div[data-testid="stDataFrame"],
    div[data-testid="stTable"] {
        border: 1px solid #DFD0BA;
        border-radius: 10px;
        overflow: hidden;
    }

    details {
        background-color: #F2E7D5;
        border: 1px solid #DFD0BA;
        border-radius: 10px;
    }

    .app-footer {
        color: #8A7B69;
        font-size: 0.78rem;
        line-height: 1.8;
        text-align: center;
        padding-top: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# SIDEBAR BRANDING
# --------------------------------------------------

with st.sidebar:
    st.markdown(
        """
        <div style="padding: 1.2rem 0 1.5rem 0;">
            <div style="
                color: #A94442;
                font-size: 0.7rem;
                font-weight: 650;
                letter-spacing: 2.5px;
                margin-bottom: 0.8rem;
            ">
                HEALTH INTELLIGENCE
            </div>
            <div style="
                color: #37332F;
                font-size: 1.55rem;
                font-weight: 600;
                line-height: 1.25;
            ">
                Diabetes Risk<br>Assessment
            </div>
            <div style="
                color: #75695B;
                font-size: 0.82rem;
                margin-top: 0.8rem;
            ">
                Machine Learning · Health Insights
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        """
        <div style="
            color: #8A7760;
            font-size: 0.7rem;
            font-weight: 650;
            letter-spacing: 2px;
            margin: 1rem 0 0.5rem 0;
        ">
            WORKSPACE
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("Use the page navigation above to explore each module.")
    st.divider()

    if MODEL_PATH.exists():
        st.markdown(
            """
            <div style="
                background: #DCE6D8;
                border: 1px solid #B7CCB0;
                border-radius: 9px;
                padding: 0.8rem;
                color: #355B3B;
                font-size: 0.84rem;
            ">
                <strong>Model status</strong><br>
                Model file available
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div style="
                background: #F1DDDA;
                border: 1px solid #DDB7B0;
                border-radius: 9px;
                padding: 0.8rem;
                color: #873936;
                font-size: 0.84rem;
            ">
                <strong>Model status</strong><br>
                Model file not found
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div style="
            color: #8A7B69;
            font-size: 0.75rem;
            margin-top: 1.5rem;
            line-height: 1.7;
        ">
            Academic project prototype<br>
            Not for clinical decision-making
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# HERO HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="hero-header">
        <div class="hero-eyebrow">
            HEALTH INTELLIGENCE &nbsp; / &nbsp; 01
        </div>
        <h1>Diabetes Risk<br>Assessment System</h1>
        <div class="hero-accent"></div>
        <p class="hero-subtitle">
            AI-assisted risk estimation, evidence-based health education,
            and model evaluation in one integrated workspace.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# MEDICAL SAFETY NOTICE
# --------------------------------------------------

st.warning(
    "EDUCATIONAL USE ONLY — This application is an academic machine-learning "
    "prototype. Its predictions are not clinically validated and must not "
    "be used to diagnose diabetes or make medication or treatment decisions."
)

# --------------------------------------------------
# DASHBOARD METRICS
# --------------------------------------------------

st.markdown(
    '<div class="section-eyebrow">AT A GLANCE</div>',
    unsafe_allow_html=True,
)
st.subheader("Project Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Dataset Records</div>
            <div class="metric-value">768</div>
            <div class="metric-note">Public educational dataset</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Model Test Accuracy</div>
            <div class="metric-value">75.3%</div>
            <div class="metric-note">Held-out test set · 154 records</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    if MODEL_PATH.exists():
        status_text = "Available"
        status_note = "Saved model file detected"
    else:
        status_text = "Unavailable"
        status_note = "Train the model first"

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Model Status</div>
            <div class="metric-value" style="font-size: 1.65rem;">
                {status_text}
            </div>
            <div class="metric-note">{status_note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
st.divider()

# --------------------------------------------------
# APPLICATION MODULES
# --------------------------------------------------

st.markdown(
    '<div class="section-eyebrow">EXPLORE THE PLATFORM</div>',
    unsafe_allow_html=True,
)
st.subheader("Application Modules")

st.markdown(
    "Select a workspace to explore its features and supporting information."
)

left_col, right_col = st.columns(2, gap="large")

with left_col:
    st.markdown(
        """
        <div class="module-card">
            <div class="module-number">01 / ASSESSMENT</div>
            <div class="module-title">Patient Assessment</div>
            <div class="module-description">
                Enter sample health measurements and review an educational
                machine-learning classification estimate.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "Open Patient Assessment",
        key="open_assessment",
        width="stretch",
    ):
        st.switch_page("pages/1_Patient_Assessment.py")

    st.markdown(
        """
        <div class="module-card">
            <div class="module-number">02 / HEALTH EDUCATION</div>
            <div class="module-title">Evidence-Based Recommendations</div>
            <div class="module-description">
                Explore general health education topics and information
                from established public-health sources.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "Explore Health Recommendations",
        key="open_recommendations",
        width="stretch",
    ):
        st.switch_page("pages/2_Health_Recommendations.py")

with right_col:
    st.markdown(
        """
        <div class="module-card">
            <div class="module-number">03 / MODEL EVALUATION</div>
            <div class="module-title">Model Performance</div>
            <div class="module-description">
                Examine classification metrics, test-set results,
                and the limitations of the machine-learning model.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "View Model Performance",
        key="open_performance",
        width="stretch",
    ):
        st.switch_page("pages/3_Model_Performance.py")

    st.markdown(
        """
        <div class="module-card">
            <div class="module-number">04 / HUMAN OVERSIGHT</div>
            <div class="module-title">Clinician Review</div>
            <div class="module-description">
                Explore a demonstration review workflow for examining
                model outputs with human oversight.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "Open Clinician Review",
        key="open_clinician_review",
        width="stretch",
    ):
        st.switch_page("pages/4_Clinician_Review.py")

# --------------------------------------------------
# TECHNOLOGY AND LIMITATIONS
# --------------------------------------------------

st.write("")
st.divider()

tech_col, limits_col = st.columns(2, gap="large")

with tech_col:
    st.markdown(
        '<div class="section-eyebrow">UNDER THE HOOD</div>',
        unsafe_allow_html=True,
    )
    st.subheader("Technology Stack")

    st.markdown(
        """
        - **Language:** Python
        - **Interface:** Streamlit
        - **Data processing:** Pandas and NumPy
        - **Machine learning:** Scikit-learn Random Forest
        - **Model persistence:** Joblib
        - **Dataset:** Pima Indians Diabetes dataset
        """
    )

with limits_col:
    st.markdown(
        '<div class="section-eyebrow">RESPONSIBLE USE</div>',
        unsafe_allow_html=True,
    )
    st.subheader("Important Limitations")

    st.markdown(
        """
        - The dataset is limited and population-specific.
        - Test accuracy alone does not establish clinical reliability.
        - The model is not a diagnostic tool.
        - Health recommendations are educational, not prescriptions.
        - Clinical validation and real hospital-system integration
          are outside this prototype.
        """
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="app-footer">
        DIABETES RISK ASSESSMENT SYSTEM<br>
        Academic Machine Learning Prototype<br>
        For educational use only · Not for diagnosis or treatment
    </div>
    """,
    unsafe_allow_html=True,
)