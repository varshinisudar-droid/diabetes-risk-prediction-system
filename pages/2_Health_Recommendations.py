
import streamlit as st

st.set_page_config(
    page_title="Health Recommendations | Diabetes Risk System",
    page_icon="🩺",
    layout="wide",
)

st.title("Evidence-Based Health Recommendations")
st.write(
    "Explore general educational information about diabetes prevention "
    "and healthy living."
)

st.warning(
    "For education only. These suggestions are not personalized medical "
    "advice or prescriptions. Do not start, stop, or change medication "
    "without consulting a qualified healthcare professional."
)

st.subheader("General Health Topics")

topic = st.selectbox(
    "Choose a topic",
    [
        "Healthy Eating",
        "Physical Activity",
        "Weight Management",
        "Blood Glucose Testing",
        "Medication Safety",
        "Professional Follow-up",
    ],
)

recommendations = {
    "Healthy Eating": [
        "Aim for balanced meals with vegetables, whole grains, and suitable "
        "sources of protein.",
        "Choose water or unsweetened drinks more often than sugary drinks.",
        "Individual dietary needs vary. A registered dietitian can help "
        "develop a suitable eating plan.",
    ],
    "Physical Activity": [
        "Regular physical activity can support general health and blood "
        "glucose management.",
        "Choose activities appropriate for your abilities and health status.",
        "Ask a healthcare professional before starting a new exercise "
        "routine if you have medical concerns or activity restrictions.",
    ],
    "Weight Management": [
        "A healthy weight can support metabolic health for some people.",
        "Avoid extreme diets or unverified weight-loss products.",
        "A healthcare professional can help determine appropriate goals "
        "based on individual circumstances.",
    ],
    "Blood Glucose Testing": [
        "Blood glucose testing requirements depend on personal health "
        "circumstances and clinician advice.",
        "A machine-learning estimate from this application cannot diagnose "
        "or rule out diabetes.",
        "Ask a healthcare professional whether laboratory testing is "
        "appropriate for you.",
    ],
    "Medication Safety": [
        "Do not begin, stop, or change medicines based on this application.",
        "Medication choice and dosage require an individualized assessment "
        "by a qualified prescriber.",
        "Discuss possible side effects, interactions, and questions with "
        "your clinician or pharmacist.",
    ],
    "Professional Follow-up": [
        "Discuss health concerns and relevant risk factors with a qualified "
        "healthcare professional.",
        "Bring relevant medical records and a list of current medicines "
        "to appointments.",
        "Seek timely medical advice for concerning symptoms. For a medical "
        "emergency, contact local emergency services.",
    ],
}

st.subheader(topic)

for item in recommendations[topic]:
    st.markdown(f"- {item}")

st.divider()

st.subheader("Evidence and Trusted Sources")

st.write(
    "The following public-health organizations provide guidance and "
    "educational information. Review the original material with a "
    "healthcare professional for advice relevant to your circumstances."
)

st.markdown(
    "- [World Health Organization (WHO): Diabetes](https://www.who.int/news-room/fact-sheets/detail/diabetes)"
)

st.markdown(
    "- [Centers for Disease Control and Prevention (CDC): Diabetes](https://www.cdc.gov/diabetes/)"
)

st.markdown(
    "- [National Institute of Diabetes and Digestive and Kidney Diseases "
    "(NIDDK)](https://www.niddk.nih.gov/health-information/diabetes)"
)

st.info(
    "Clinician review safeguard: This prototype provides general "
    "educational information only. It does not generate prescriptions, "
    "drug names, or medication dosages."
)

st.caption(
    "Project status: Educational recommendations module. "
    "The content is general and is not individualized clinical guidance."
)
