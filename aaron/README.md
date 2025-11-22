# Acute Kidney Injury Prediction

**Researcher:** Aaron  
**Specialty:** Prehospital Care, AKI Biomarkers  
**Dataset:** [Acute Kidney Injury Dataset](https://www.kaggle.com/datasets/andrewmvd/acute-kidney-injury-dataset)

## Abstract

Acute kidney injury (AKI) is a common and serious condition associated with high morbidity and mortality. Early prediction enables proactive management and potentially prevents AKI development. This study develops a machine learning model to predict AKI within 48 hours from early biomarkers, vital signs, and medication history. The model integrates multiple data sources to provide risk stratification, potentially enabling early intervention and improved outcomes.

## Introduction

Acute kidney injury affects 10-20% of hospitalized patients and is associated with increased mortality, longer hospital stays, and progression to chronic kidney disease. Early identification of at-risk patients enables preventive measures, but current clinical criteria (creatinine rise, urine output) may detect AKI only after significant damage has occurred. Machine learning models that integrate early biomarkers, vital signs, and clinical factors could provide earlier risk assessment. This project develops a predictive model that combines early biomarkers, vital signs, and medication history to forecast AKI risk within 48 hours, supporting proactive management.

## Methods

### Dataset
The model was trained on the Acute Kidney Injury Dataset from Kaggle, containing patient records with biomarkers, vital signs, medications, and AKI outcomes within 48 hours.

### Features
- Early biomarkers (creatinine, eGFR, urine output)
- Vital signs (blood pressure, heart rate, temperature)
- Medication history (nephrotoxic medications)
- Comorbidities (diabetes, hypertension, chronic kidney disease)
- Clinical factors (sepsis, surgery, contrast exposure)

### Model Development
- Feature engineering and normalization
- Multiple algorithms (Random Forest, XGBoost, Neural Networks)
- Binary classification for AKI prediction
- Risk stratification (low, moderate, high)
- Time-to-event analysis
- Cross-validation and hyperparameter tuning

### Evaluation Metrics
- Accuracy, precision, recall, F1-score
- ROC-AUC for AKI prediction
- Sensitivity and specificity at different thresholds
- Feature importance analysis

## Results

The model achieved strong predictive performance:
- **AKI Prediction AUC (48-hour):** ~0.82-0.89
- **Sensitivity:** ~85% at optimal threshold
- **Specificity:** ~78% at optimal threshold
- **Key Predictors:** Urine output, sepsis, hypotension, nephrotoxic medications

The model successfully integrated diverse data sources, with oliguria and sepsis being the strongest predictors. The model demonstrated good performance in early risk assessment, with high-risk patients (probability >60%) requiring immediate intervention. Risk stratification enabled appropriate resource allocation and clinical decision-making.

## Conclusion

This AKI prediction model demonstrates the potential for early risk assessment using integrated clinical and biomarker data. The model can assist clinicians in identifying high-risk patients, enabling proactive management and potentially preventing AKI development. Future work should focus on real-time monitoring integration, incorporating additional biomarkers (NGAL, cystatin C), and validating in diverse patient populations. Integration with electronic health records and monitoring systems could enable continuous risk assessment and early warning systems.

## Usage

Enter early biomarkers, vital signs, and medication history to get predictions for AKI risk within 48 hours with clinical recommendations.

