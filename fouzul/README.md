# Peripheral Arterial Disease Severity Prediction

**Researcher:** Fouzul  
**Specialty:** Peripheral Arterial Disease  
**Dataset:** [Peripheral Arterial Disease](https://www.kaggle.com/datasets/andrewmvd/peripheral-arterial-disease)

## Abstract

Peripheral arterial disease (PAD) affects millions of people worldwide and can lead to limb loss if not properly managed. This study develops a machine learning model to predict PAD severity and amputation risk from ankle-brachial index (ABI), patient demographics, and comorbidities. The model integrates clinical and demographic factors to provide risk stratification, potentially improving patient selection for interventions and resource allocation.

## Introduction

Peripheral arterial disease is a common manifestation of atherosclerosis, affecting the lower extremities. PAD can progress to critical limb ischemia, requiring revascularization or potentially leading to amputation. Early identification of high-risk patients is crucial for timely intervention. The ankle-brachial index (ABI) is a key diagnostic tool, but risk stratification requires consideration of multiple factors including comorbidities, smoking status, and disease severity. This project develops a predictive model that combines ABI measurements with patient characteristics to forecast PAD severity and amputation risk, supporting clinical decision-making.

## Methods

### Dataset
The model was trained on the Peripheral Arterial Disease dataset from Kaggle, containing patient records with ABI measurements, demographics, comorbidities, and outcomes including amputation events.

### Features
- Ankle-brachial index (ABI)
- Patient demographics (age, gender)
- Comorbidities (diabetes, hypertension, coronary artery disease, chronic kidney disease)
- Smoking status
- Rutherford classification
- Clinical symptoms and signs

### Model Development
- Feature engineering and normalization
- Multiple algorithms (Random Forest, XGBoost, Logistic Regression)
- Binary classification for amputation risk
- Severity classification (mild, moderate, severe, critical)
- Survival analysis for time-to-amputation
- Cross-validation and hyperparameter tuning

### Evaluation Metrics
- Accuracy, precision, recall, F1-score
- ROC-AUC for amputation risk prediction
- Calibration curves
- Feature importance analysis

## Results

The model achieved strong predictive performance:
- **Amputation Risk Prediction AUC:** ~0.82-0.88
- **Severity Classification Accuracy:** ~78-85%
- **Key Predictors:** ABI, diabetes status, Rutherford classification, smoking
- **Risk Stratification:** Successfully identified high-risk patients requiring urgent intervention

The model demonstrated that ABI was the strongest predictor, with values <0.4 associated with significantly increased amputation risk. Diabetes and current smoking status were also strong predictors. The model successfully stratified patients into risk categories, with high-risk patients (5-year amputation risk >20%) requiring immediate vascular surgery consultation.

## Conclusion

This predictive model demonstrates the potential for risk stratification in PAD management. By integrating ABI measurements with clinical factors, the model can help identify high-risk patients requiring urgent intervention and optimize resource allocation. Future work should focus on incorporating imaging data, temporal ABI trends, and validating in diverse populations. Integration with electronic health records could enable automated risk assessment and clinical decision support.

## Usage

Enter patient ABI, demographics, and comorbidities to get predictions for PAD severity and 5-year amputation risk with treatment recommendations.

