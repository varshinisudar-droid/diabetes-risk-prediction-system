
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "data" / "diabetes.csv"


def load_diabetes_data():
    """Load the public diabetes dataset from the data folder."""
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {DATASET_PATH}"
        )

    return pd.read_csv(DATASET_PATH)


if __name__ == "__main__":
    try:
        diabetes_data = load_diabetes_data()

        print("Dataset loaded successfully!")
        print("Dataset shape:", diabetes_data.shape)
        print("\nColumn names:")
        print(diabetes_data.columns.tolist())
        print("\nFirst five rows:")
        print(diabetes_data.head())

    except Exception as error:
        print("Error:", error)