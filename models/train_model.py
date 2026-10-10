
from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from utils.data_loader import load_diabetes_data
from utils.preprocessing import replace_invalid_zeros


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "diabetes_model.joblib"

# Load the dataset and replace invalid zero measurements.
data = load_diabetes_data()
data = replace_invalid_zeros(data)

# Separate input features and target.
X = data.drop(columns=["Outcome"])
y = data["Outcome"]

# Split before learning imputation values to prevent data leakage.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

# Imputation is fitted on training data only.
# The same fitted imputer is used for testing and future predictions.
model = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                class_weight="balanced",
            ),
        ),
    ]
)

# Train the complete pipeline.
model.fit(X_train, y_train)

# Evaluate on the held-out test data.
predictions = model.predict(X_test)

print("Model training completed!")
print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))
print("Test accuracy:", round(accuracy_score(y_test, predictions), 3))
print("\nClassification report:")
print(classification_report(y_test, predictions, zero_division=0))

# Save the complete pipeline, including its imputer.
joblib.dump(model, MODEL_PATH)
print("Model pipeline saved to:", MODEL_PATH)
