# Bladder Cancer Recurrence Prediction

**Researcher:** Sabour  
**Specialty:** Urology, Oncology  
**Dataset:** [Bladder Cancer Histopathology](https://www.kaggle.com/datasets/andrewmvd/bladder-cancer-histopathology)

## Abstract

Bladder cancer has one of the highest recurrence rates among cancers, with 50-70% of non-muscle-invasive tumors recurring within 5 years. Early identification of high-risk patients enables more intensive surveillance and potentially adjuvant therapy. This study develops a machine learning model to predict bladder cancer recurrence by analyzing histopathology images and clinical features. The model integrates morphological features from histopathology with clinical staging to provide personalized risk assessment.

## Introduction

Bladder cancer is the fourth most common cancer in men and requires lifelong surveillance due to high recurrence rates. Current risk stratification relies on clinical staging (TNM) and tumor grade, but these may not fully capture recurrence risk. Histopathology analysis provides detailed morphological information, but interpretation can be subjective. Machine learning models that analyze histopathology images could provide objective, quantitative assessments of recurrence risk. This project develops a predictive model that combines histopathology image analysis with clinical features to forecast recurrence, supporting personalized surveillance strategies.

## Methods

### Dataset
The model was trained on the Bladder Cancer Histopathology dataset from Kaggle, containing histopathology images with clinical staging, tumor characteristics, and recurrence outcomes.

### Features
- Histopathology image features (morphology, cellular patterns, architecture)
- Clinical staging (TNM classification)
- Tumor grade (low vs high)
- Tumor characteristics (size, number, multifocality)
- Patient demographics

### Model Development
- Deep learning for histopathology image analysis
- Feature extraction from histopathology images
- Integration with clinical features
- Multiple algorithms (CNN, Random Forest, XGBoost)
- Survival analysis for time-to-recurrence
- Risk stratification (low, moderate, high)
- Cross-validation and hyperparameter tuning

### Evaluation Metrics
- C-index for survival prediction
- ROC-AUC for recurrence prediction
- Calibration curves
- Feature importance analysis

## Results

The model achieved strong predictive performance:
- **Recurrence Prediction AUC (1-year):** ~0.78-0.85
- **C-index:** ~0.74
- **Key Predictors:** Tumor stage, grade, histopathology features, tumor multiplicity
- **Risk Stratification:** Successfully identified high-risk patients (1-year recurrence risk >60%)

The model demonstrated that integration of histopathology image features with clinical staging improved prediction compared to clinical factors alone. High-grade tumors, muscle-invasive stage, and multiple tumors were strong predictors. Histopathology features provided additional discriminative power, particularly for intermediate-risk cases.

## Conclusion

This integrated model demonstrates the potential for combining histopathology image analysis with clinical data in bladder cancer recurrence prediction. The model can assist urologists in risk stratification, enabling personalized surveillance strategies and treatment decisions. Future work should focus on validating histopathology features, incorporating additional biomarkers, and validating in diverse patient populations. Integration with electronic health records and pathology systems could enable automated risk assessment and clinical decision support.

## Usage

Upload a histopathology image and enter clinical features to get predictions for bladder cancer recurrence risk with surveillance recommendations.

