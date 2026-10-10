
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split

from utils.data_loader import load_diabetes_data
from utils.preprocessing import replace_invalid_zeros


st.set_page_config(
    page_title="Model Performance | Diabetes Risk System",
    page_icon="📊",
    layout="wide",
)

st.title("Model Performance Dashboard")

st.write(
    "Review the educational machine-learning model's performance "
    "on a held-out test dataset."
)

st.warning(
    "These are experimental results from a limited public dataset. "
    "They do not establish clinical reliability and must not be used "
    "to diagnose, rule out diabetes, or make treatment decisions."
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "diabetes_model.joblib"

if not MODEL_PATH.exists():
    st.error("Model file not found. Run: python -m models.train_model")
    st.stop()

try:
    # Apply the same zero-value handling used during model training.
    data = load_diabetes_data()
    data = replace_invalid_zeros(data)

    X = data.drop(columns=["Outcome"])
    y = data["Outcome"]

    # Reproduce the exact split used in train_model.py.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # Load the complete fitted pipeline: imputer + classifier.
    model = joblib.load(MODEL_PATH)

    predictions = model.predict(X_test)

except Exception as error:
    st.error(f"Could not calculate model performance: {error}")
    st.stop()

accuracy = accuracy_score(y_test, predictions)

report = classification_report(
    y_test,
    predictions,
    labels=[0, 1],
    target_names=["Negative class", "Positive class"],
    output_dict=True,
    zero_division=0,
)

st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total records", f"{len(data):,}")
col2.metric("Training records", f"{len(X_train):,}")
col3.metric("Testing records", f"{len(X_test):,}")

st.subheader("Evaluation Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Test accuracy", f"{accuracy:.1%}")
col2.metric(
    "Positive-class precision",
    f"{report['Positive class']['precision']:.1%}",
)
col3.metric(
    "Positive-class recall",
    f"{report['Positive class']['recall']:.1%}",
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Positive-class F1-score",
    f"{report['Positive class']['f1-score']:.1%}",
)
col2.metric(
    "Negative-class recall",
    f"{report['Negative class']['recall']:.1%}",
)
col3.metric(
    "Positive test cases",
    f"{int((y_test == 1).sum())}",
)

st.subheader("Confusion Matrix")

matrix = confusion_matrix(y_test, predictions, labels=[0, 1])

matrix_df = pd.DataFrame(
    matrix,
    index=["Actual negative", "Actual positive"],
    columns=["Predicted negative", "Predicted positive"],
)

st.dataframe(matrix_df, width="stretch")

st.caption(
    "Rows represent actual classes; columns represent model predictions."
)

st.subheader("Detailed Classification Report")

report_df = pd.DataFrame(report).transpose()
st.dataframe(report_df.round(3), width="stretch")

st.subheader("Metric Explanations")

with st.expander("What do these metrics mean?"):
    st.markdown(
        """
        - **Accuracy:** Fraction of all test records classified correctly.
        - **Precision:** Fraction of positive predictions that were correct.
        - **Recall:** Fraction of actual positive cases identified.
        - **F1-score:** Balance between precision and recall.
        - **Confusion matrix:** Counts correct and incorrect predictions.
        """
    )

st.info(
    "This page evaluates model behavior on one held-out split. "
    "It does not establish performance in other populations or clinical "
    "settings. Independent validation and qualified clinical oversight "
    "would be necessary before any real-world healthcare use."
)

st.caption(
    "Dataset: Public Pima Indians Diabetes dataset, 768 records. "
    "This educational dataset has population-specific limitations."
)
