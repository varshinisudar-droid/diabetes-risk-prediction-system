
import pandas as pd


MEASUREMENT_COLUMNS = [
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
]


def replace_invalid_zeros(data):
    """Replace impossible zero measurements with missing values."""

    cleaned_data = data.copy()

    columns_to_clean = [
        column
        for column in MEASUREMENT_COLUMNS
        if column in cleaned_data.columns
    ]

    cleaned_data[columns_to_clean] = (
        cleaned_data[columns_to_clean].replace(0, float("nan"))
    )

    return cleaned_data


def preprocess_diabetes_data(data):
    """Clean data for inspection without changing the original dataset."""

    return replace_invalid_zeros(data)


if __name__ == "__main__":
    from utils.data_loader import load_diabetes_data

    diabetes_data = load_diabetes_data()
    cleaned_data = preprocess_diabetes_data(diabetes_data)

    print("Preprocessing check completed!")
    print("Dataset shape:", cleaned_data.shape)
    print("Missing values after zero handling:")
    print(cleaned_data.isnull().sum())
