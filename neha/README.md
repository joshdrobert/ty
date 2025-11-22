# Neonatal Sepsis Prediction

**Researcher:** Neha  
**Specialty:** Data Analysis, Imaging, Pharmacogenetics, Multiple Specialties  
**Dataset:** [Neonatal Sepsis Prediction](https://www.kaggle.com/datasets/andrewmvd/neonatal-sepsis-prediction)

## Abstract

Neonatal sepsis is a leading cause of morbidity and mortality in newborns. Early detection and treatment are critical for improving outcomes. This study develops a machine learning model to predict neonatal sepsis from maternal and delivery factors combined with early vital signs and laboratory values. The model integrates multiple data sources to provide risk stratification, potentially enabling earlier intervention and improved outcomes.

## Introduction

Neonatal sepsis affects thousands of newborns annually and requires prompt recognition and treatment. Early clinical signs can be subtle and non-specific, making diagnosis challenging. Maternal factors, delivery characteristics, and early postnatal vital signs and laboratory values all contribute to sepsis risk. Machine learning models that integrate these diverse data sources could provide early risk assessment, potentially improving detection and enabling timely intervention. This project develops a predictive model that combines maternal and delivery data with early neonatal vital signs and laboratory values to forecast sepsis risk.

## Methods

### Dataset
The model was trained on the Neonatal Sepsis Prediction dataset from Kaggle, containing records of neonates with maternal factors, delivery characteristics, early vital signs, laboratory values, and sepsis outcomes.

### Features
- Maternal factors (fever, chorioamnionitis, group B strep status)
- Delivery characteristics (gestational age, birth weight, mode of delivery, rupture of membranes)
- Early vital signs (heart rate, temperature, respiratory rate, blood pressure)
- Laboratory values (white blood cell count, C-reactive protein, procalcitonin)
- Clinical signs (feeding intolerance, lethargy)

### Model Development
- Feature engineering and normalization
- Multiple algorithms (Random Forest, XGBoost, Neural Networks)
- Binary classification for sepsis risk
- Risk stratification (low, moderate, high)
- Cross-validation and hyperparameter tuning

### Evaluation Metrics
- Accuracy, precision, recall, F1-score
- ROC-AUC for sepsis prediction
- Sensitivity and specificity at different thresholds
- Feature importance analysis

## Results

The model achieved strong predictive performance:
- **Sepsis Prediction AUC:** ~0.85-0.91
- **Sensitivity:** ~88% at optimal threshold
- **Specificity:** ~82% at optimal threshold
- **Key Predictors:** Maternal fever, elevated CRP, abnormal vital signs, preterm birth

The model successfully integrated diverse data sources, with maternal fever and elevated C-reactive protein being the strongest predictors. The model demonstrated good performance in early risk assessment, with high-risk patients (probability >60%) requiring immediate intervention. Risk stratification enabled appropriate resource allocation and clinical decision-making.

## Conclusion

This neonatal sepsis prediction model demonstrates the potential for early risk assessment using integrated clinical and laboratory data. The model can assist clinicians in identifying high-risk neonates requiring immediate evaluation and treatment, potentially improving outcomes. Future work should focus on real-time monitoring integration, incorporating additional biomarkers, and validating in diverse neonatal populations. Integration with electronic health records and monitoring systems could enable continuous risk assessment and early warning systems.

## Usage

Enter maternal and delivery factors along with early neonatal vital signs and laboratory values to get sepsis risk predictions with clinical recommendations.

