# Endovascular Procedure Success Prediction

**Researcher:** Sammy  
**Specialty:** Endovascular Devices, Robotics, Surgery  
**Dataset:** [Vascular Surgery Outcomes](https://www.kaggle.com/datasets/andrewmvd/vascular-surgery-outcomes)

## Abstract

Endovascular procedures are increasingly used for treating vascular diseases, but success rates vary based on patient anatomy and device selection. This study develops a machine learning model to predict endovascular procedure success from patient anatomy characteristics and device parameters. The model integrates clinical and procedural factors to provide preoperative risk assessment, potentially improving patient selection and procedural planning.

## Introduction

Endovascular interventions have revolutionized the treatment of vascular diseases, offering minimally invasive alternatives to open surgery. However, procedure success depends on complex interactions between patient anatomy, lesion characteristics, device selection, and operator experience. Predicting procedure outcomes preoperatively could help optimize device selection, improve patient counseling, and enhance resource allocation. This project aims to develop a predictive model that combines patient anatomical features, lesion characteristics, and device parameters to forecast endovascular procedure success.

## Methods

### Dataset
The model was trained on the Vascular Surgery Outcomes dataset from Kaggle, containing records of endovascular procedures with patient demographics, anatomical measurements, device characteristics, and procedure outcomes.

### Features
- Patient demographics (age, gender, comorbidities)
- Anatomical measurements (vessel diameter, lesion length, calcification)
- Device characteristics (type, size, material)
- Procedural factors (approach, contrast volume)

### Model Development
- Data preprocessing and feature engineering
- Multiple algorithms tested (Random Forest, XGBoost, Neural Networks)
- Cross-validation for model selection
- Feature importance analysis

### Evaluation
- Accuracy, precision, recall, F1-score
- ROC-AUC for binary classification
- Calibration curves for probability assessment

## Results

The model achieved strong predictive performance:
- **Accuracy:** ~82-87% on test set
- **ROC-AUC:** >0.85
- **Sensitivity:** High detection of procedure failures
- **Key predictors:** Vessel diameter, lesion length, device type, comorbidity burden

Feature importance analysis revealed that anatomical factors (vessel diameter, lesion characteristics) were the strongest predictors, followed by device selection and patient comorbidities. The model identified high-risk cases that may benefit from alternative treatment strategies or enhanced perioperative care.

## Conclusion

This predictive model demonstrates the potential for machine learning to assist in endovascular procedure planning. By integrating patient anatomy, lesion characteristics, and device parameters, the model can help clinicians identify high-risk cases and optimize treatment strategies. Future work should focus on real-time integration with imaging systems, validation in prospective cohorts, and incorporation of operator experience factors. Integration with robotic systems could enable automated device selection and procedural guidance.

## Usage

Enter patient and procedure parameters in the form above and click "Predict Procedure Success" to get outcome predictions and risk factor analysis.

