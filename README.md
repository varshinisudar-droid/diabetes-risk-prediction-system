# AI-Powered Diabetes Risk Prediction and Evidence-Based Recommendation System

## Project Overview

The AI-Powered Diabetes Risk Prediction and Evidence-Based Recommendation System is an academic healthcare application developed using Python, Streamlit, and Machine Learning. It demonstrates how patient-related measurements can be processed by a machine-learning model to generate an experimental diabetes classification output.

The application provides a patient assessment interface, general health education and recommendations, model performance evaluation, and a clinician review workflow. Its purpose is to demonstrate the use of data science in healthcare-related applications while emphasizing responsible AI use and the importance of professional medical oversight.

**Important:** This project is an educational prototype, not a clinically validated diagnostic system. Its predictions must not be used to diagnose or rule out diabetes, make treatment decisions, or determine medication or dosage.

## Objectives

- Develop a user-friendly healthcare assessment application.
- Apply machine learning to a public diabetes dataset.
- Demonstrate data preprocessing, model training, and evaluation.
- Display experimental predictions based on numerical input features.
- Provide general health education using reputable public-health resources.
- Implement a clinician review workflow for documenting assessment reviews.
- Emphasize the limitations, safety requirements, and responsible use of AI in healthcare.

## Features

### 1. Dashboard
Provides an overview of the application, dataset, trained model, and available modules.

### 2. Patient Assessment
Collects patient profile information and numerical measurements used by the model. Body Mass Index (BMI) is calculated from height and weight. The application displays an experimental model output with appropriate limitations.

### 3. Health Recommendations
Provides general educational information covering:
- Healthy eating
- Physical activity
- Weight management
- Blood glucose testing
- Medication safety
- Professional medical follow-up

The recommendations are educational and are not personalized prescriptions. Users should consult qualified healthcare professionals for individual medical advice.

### 4. Model Performance Dashboard
Displays evaluation results from a held-out test dataset, including:
- Accuracy
- Positive-class precision
- Positive-class recall
- F1-score
- Negative-class recall
- Confusion matrix
- Classification report

### 5. Clinician Review
Provides a workflow for recording review status, model output, and review notes. Review records are stored locally in an SQLite database and can be exported as a CSV file.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| Pandas | Dataset handling and preprocessing |
| Scikit-learn | Machine learning and evaluation |
| Random Forest Classifier | Classification algorithm |
| SimpleImputer | Median imputation for missing measurements |
| Joblib | Saving and loading the trained model |
| SQLite | Local clinician review records |
| Matplotlib / Seaborn | Use only if included in the implementation |

## Dataset

The project uses the **Pima Indians Diabetes dataset**, a public dataset containing 768 records and 8 numerical input features, along with a binary target column named `Outcome`.

The features are:

1. Pregnancies
2. Glucose
3. BloodPressure
4. SkinThickness
5. Insulin
6. BMI
7. DiabetesPedigreeFunction
8. Age

The target column is `Outcome`, which represents the dataset's binary class label.

Some measurements contain zero values that are not physiologically plausible for the corresponding measurement. These are treated as missing values for selected columns and imputed using the median learned from the training data.

The dataset has population-specific limitations and is not sufficient to establish clinical performance in other populations.

## Machine Learning Methodology

### Data preprocessing
- Load the public dataset.
- Replace selected invalid zero measurements with missing values.
- Split the data into training and testing sets.
- Apply median imputation using training data only.

### Model training
A Random Forest Classifier is trained using the following configuration:

- Number of estimators: 100
- Random state: 42
- Class weighting: Balanced
- Test size: 20%
- Stratified train/test split

A scikit-learn pipeline combines the median imputer and classifier so the imputation values learned during training are reused during prediction.

### Evaluation
The model is evaluated on a held-out test set containing 154 records. In the current run, the model achieved approximately **75.3% test accuracy**.

This result represents performance on one split of this particular dataset. It is not evidence of clinical validity or a reliable estimate of an individual's personal risk.

## Project Structure

```text
diabetes_risk_system/
│
├── app.py
├── data/
│   ├── diabetes.csv
│   └── clinician_reviews.db
│
├── models/
│   ├── train_model.py
│   └── diabetes_model.joblib
│
├── pages/
│   ├── 1_Patient_Assessment.py
│   ├── 2_Health_Recommendations.py
│   ├── 3_Model_Performance.py
│   └── 4_Clinician_Review.py
│
├── utils/
│   ├── data_loader.py
│   └── preprocessing.py
│
├── requirements.txt
└── README.md
```

*The SQLite database is created locally when the review module initializes, if that is how your implementation is configured. The structure above illustrates the expected organization; retain the actual filenames in your repository.*

## Installation and Setup

### Prerequisites

- Python 3.10 or a compatible version supported by the installed dependencies
- pip
- Visual Studio Code or another Python editor

### 1. Clone the repository

Replace the placeholder URL with your actual GitHub repository URL.

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd diabetes_risk_system
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment on Windows

For Command Prompt:

```bat
.venv\Scripts\activate.bat
```

For PowerShell, if script execution is permitted:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Verify the dataset

Ensure that the public dataset is available at:

```text
data/diabetes.csv
```

The file should contain the eight input columns and the `Outcome` target column described above.

### 6. Train the model

From the project root directory, run:

```bash
python -m models.train_model
```

The trained pipeline should be saved to:

```text
models/diabetes_model.joblib
```

If the trained model is already included in your local project, retraining is not necessary merely to launch the application.

### 7. Launch the application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## Example Model Evaluation

The current training run produced the following results:

| Evaluation detail | Result |
|---|---:|
| Dataset records | 768 |
| Training records | 614 |
| Testing records | 154 |
| Test accuracy | 75.3% |
| Positive-class precision | 64.3% |
| Positive-class recall | 66.7% |
| Positive-class F1-score | 65.5% |
| Negative-class recall | 80.0% |

These figures should be updated if the dataset, preprocessing, model configuration, or evaluation split changes.

## Responsible AI and Safety

- The application is intended for academic demonstration and learning.
- Predictions are experimental and must not be interpreted as a diagnosis.
- A negative model output does not rule out diabetes.
- General educational recommendations are not individualized medical advice.
- The application does not autonomously prescribe medications or dosages.
- Clinical decisions must be made by qualified healthcare professionals.
- The public dataset has limitations and does not establish real-world clinical reliability.
- Do not upload real patient information, credentials, private records, or sensitive health data to the public repository.

## Future Enhancements

- Add automated tests for preprocessing, prediction, and review workflows.
- Improve reproducibility with dependency version pinning.
- Evaluate the model using cross-validation and additional suitable datasets.
- Investigate probability calibration and subgroup performance.
- Improve data validation and error handling.
- Add stronger access controls and privacy safeguards before any real-world use.
- Expand educational content with verified, maintained public-health references.

## Learning Outcomes

This project demonstrates practical skills in:

- Python programming
- Data cleaning and preprocessing
- Machine learning model development
- Train/test splitting and model evaluation
- Streamlit application development
- Data visualization and metric interpretation
- SQLite database integration
- CSV export
- Responsible AI principles in healthcare applications

## Conclusion

The AI-Powered Diabetes Risk Prediction and Evidence-Based Recommendation System demonstrates an end-to-end educational machine-learning workflow through an interactive healthcare-themed application. By combining patient assessment, a Random Forest classification pipeline, evaluation metrics, general health education, and clinician review documentation, the project illustrates how data science components can be integrated into a single prototype while acknowledging the need for further validation, privacy protections, and qualified clinical oversight.

## Disclaimer

This software is provided for educational and academic purposes only. It has not been validated for clinical use and must not be relied upon for diagnosis, prevention, treatment, or medication decisions. Consult a qualified healthcare professional for medical concerns.

## Author

**Varshini A**

M.Sc. Applied Data Science  
SRM Institute of Science and Technology, Ramapuram
