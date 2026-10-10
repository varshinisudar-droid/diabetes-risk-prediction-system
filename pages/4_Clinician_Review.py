from pathlib import Path
import sqlite3
import uuid
from datetime import date, datetime

import pandas as pd
import streamlit as st


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Clinician Review",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "clinician_reviews.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# DATABASE SETUP
# --------------------------------------------------
def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS clinician_reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                review_reference TEXT UNIQUE NOT NULL,
                review_date TEXT NOT NULL,
                review_status TEXT NOT NULL,
                model_output TEXT NOT NULL,
                review_notes TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


def save_review(review_date, review_status, model_output, review_notes):
    reference = "CTR-" + uuid.uuid4().hex[:8].upper()

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO clinician_reviews (
                review_reference,
                review_date,
                review_status,
                model_output,
                review_notes,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                reference,
                review_date.isoformat(),
                review_status,
                model_output,
                review_notes,
                datetime.now().isoformat(timespec="seconds"),
            ),
        )

    return reference


def load_reviews():
    with get_connection() as connection:
        return pd.read_sql_query(
            """
            SELECT
                review_reference AS 'Review Reference',
                review_date AS 'Review Date',
                review_status AS 'Review Status',
                model_output AS 'Model Output',
                review_notes AS 'Review Notes',
                created_at AS 'Created At'
            FROM clinician_reviews
            ORDER BY id DESC
            """,
            connection,
        )


initialize_database()


# --------------------------------------------------
# STYLING
# --------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F7F0E3;
        color: #37332F;
    }

    [data-testid="stSidebar"] {
        background-color: #E5D3B3;
    }

    h1, h2, h3 {
        color: #37332F;
    }

    .review-banner {
        background: #E5D3B3;
        padding: 22px 25px;
        border-radius: 12px;
        border-left: 5px solid #557A5C;
        margin: 12px 0 24px 0;
    }

    .review-card {
        background: #FBF7EF;
        border: 1px solid #DED0BB;
        padding: 18px;
        border-radius: 12px;
        margin-bottom: 12px;
    }

    div.stButton > button[kind="primary"] {
        background-color: #A94442;
        border: 1px solid #A94442;
        color: white;
        border-radius: 8px;
        min-height: 42px;
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: #883936;
        border-color: #883936;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.markdown("## Care Review")
    st.caption("Diabetes Risk Assessment System")
    st.divider()
    st.markdown("**Current module**")
    st.write("Clinician Review")
    st.caption(
        "This page stores demonstration review records "
        "locally in a SQLite database."
    )


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------
st.title("Clinician Review")
st.caption(
    "Review model outputs, document observations, "
    "and maintain a local review history."
)

st.markdown(
    """
    <div class="review-banner">
        <strong>Human review is essential</strong><br>
        The model output is an experimental estimate based on a
        public dataset. It is not a diagnosis and must not be used
        independently to make treatment decisions.
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# REVIEW ENTRY FORM
# --------------------------------------------------
st.subheader("Create a review record")

with st.form("clinician_review_form", clear_on_submit=False):

    col1, col2 = st.columns(2)

    with col1:
        review_date = st.date_input(
            "Review date",
            value=date.today(),
        )

        review_status = st.selectbox(
            "Review status",
            [
                "Pending review",
                "Reviewed",
                "Further assessment needed",
                "Closed",
            ],
        )

    with col2:
        model_output = st.selectbox(
            "Model output being reviewed",
            [
                "Not recorded",
                "Positive model classification",
                "Negative model classification",
                "Output unavailable",
            ],
        )

        st.info(
            "Do not enter patient names, contact details, "
            "identification numbers, or other identifying information."
        )

    review_notes = st.text_area(
        "Review notes",
        placeholder=(
            "Document non-identifying observations, data-quality "
            "concerns, limitations, or questions for professional review."
        ),
        height=150,
        max_chars=3000,
    )

    submitted = st.form_submit_button(
        "Save review record",
        type="primary",
        width="stretch",
    )

    if submitted:
        if not review_notes.strip():
            st.error("Please enter review notes before saving.")
        else:
            try:
                reference = save_review(
                    review_date=review_date,
                    review_status=review_status,
                    model_output=model_output,
                    review_notes=review_notes.strip(),
                )

                st.session_state["last_review_reference"] = reference
                st.success("Review record saved successfully.")
                st.code(reference, language=None)

            except sqlite3.Error as error:
                st.error(f"Unable to save the review record: {error}")


# --------------------------------------------------
# REVIEW HISTORY
# --------------------------------------------------
st.divider()
st.subheader("Saved review history")

try:
    reviews = load_reviews()

    if reviews.empty:
        st.info(
            "No review records have been saved yet. "
            "Your records will appear here after submission."
        )
    else:
        # Convert display columns to consistent text types.
        # This helps prevent PyArrow mixed-type conversion errors.
        for column in reviews.columns:
            reviews[column] = reviews[column].fillna("").astype(str)

        metric_col1, metric_col2, metric_col3 = st.columns(3)

        with metric_col1:
            st.metric("Total records", len(reviews))

        with metric_col2:
            pending_count = int(
                (reviews["Review Status"] == "Pending review").sum()
            )
            st.metric("Pending review", pending_count)

        with metric_col3:
            completed_count = int(
                (reviews["Review Status"] == "Reviewed").sum()
            )
            st.metric("Reviewed", completed_count)

        st.dataframe(
            reviews,
            width="stretch",
            hide_index=True,
        )

        csv_data = reviews.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Export review history as CSV",
            data=csv_data,
            file_name="clinician_review_history.csv",
            mime="text/csv",
            width="stretch",
        )

except (sqlite3.Error, pd.errors.DatabaseError) as error:
    st.error(f"Unable to load review history: {error}")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()
st.caption(
    "Educational prototype only. Records are stored locally without "
    "encryption. Do not use real patient information. This module does "
    "not provide clinical validation, diagnoses, or prescriptions."
)