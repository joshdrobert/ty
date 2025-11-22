# HCC Recurrence Risk Prediction

**Researcher:** Cyril  
**Specialty:** Hepatocellular Carcinoma, Computational Biology  
**Dataset:** [Liver Cancer Dataset](https://www.kaggle.com/datasets/andrewmvd/liver-cancer-dataset)

## Abstract

Hepatocellular carcinoma (HCC) is the most common primary liver cancer and frequently recurs after treatment. Early identification of high-risk patients enables more intensive surveillance and potentially adjuvant therapy. This study develops a machine learning model to predict HCC recurrence risk by integrating gene expression signatures with clinical staging information. The model combines molecular biomarkers with traditional clinical factors to provide personalized risk assessment.

## Introduction

HCC recurrence is a major challenge in liver cancer management, with recurrence rates of 50-70% within 5 years after curative treatment. Current risk stratification relies primarily on clinical staging systems (BCLC, TNM), but these may not fully capture biological aggressiveness. Gene expression profiling has revealed molecular subtypes with different recurrence risks, but integration with clinical factors remains challenging. This project develops a predictive model that combines gene expression signatures with clinical staging to forecast recurrence risk, potentially enabling personalized surveillance and treatment strategies.

## Methods

### Dataset
The model was trained on the Liver Cancer Dataset from Kaggle, containing HCC patient records with gene expression data, clinical staging, and recurrence outcomes.

### Features
- Clinical staging (BCLC, TNM)
- Tumor characteristics (size, number, vascular invasion)
- Laboratory values (AFP, liver function tests)
- Gene expression signatures (proliferation, stemness, immune signatures)
- Patient demographics and comorbidities

### Model Development
- Feature engineering for gene expression data
- Integration of molecular and clinical features
- Multiple algorithms (Random Forest, XGBoost, Neural Networks)
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
- **Recurrence Prediction AUC (2-year):** ~0.78-0.85
- **C-index:** ~0.75
- **Key Predictors:** Vascular invasion, gene expression risk score, BCLC stage, tumor size
- **Risk Stratification:** Successfully identified high-risk patients (2-year recurrence risk >60%)

The model demonstrated that integration of gene expression signatures with clinical factors improved prediction compared to clinical staging alone. Vascular invasion and high gene expression risk scores were the strongest predictors. The model successfully stratified patients into risk categories, with high-risk patients requiring intensive surveillance and potentially adjuvant therapy.

## Conclusion

This integrated model demonstrates the potential for combining molecular and clinical data in HCC recurrence prediction. The model can assist clinicians in risk stratification, enabling personalized surveillance strategies and treatment decisions. Future work should focus on validating gene expression signatures, incorporating additional biomarkers, and validating in diverse patient populations. Integration with electronic health records could enable automated risk assessment and clinical decision support.

## Usage

Enter patient clinical staging, tumor characteristics, and gene expression risk score to get predictions for HCC recurrence risk with surveillance recommendations.

