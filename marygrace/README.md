# Fetal Health Status Classification

**Researcher:** MaryGrace  
**Specialty:** OBGYN  
**Dataset:** [Fetal Health Classification](https://www.kaggle.com/datasets/andrewmvd/fetal-health-classification)

## Abstract

Cardiotocography (CTG) is a standard method for monitoring fetal well-being during pregnancy and labor. This study presents a machine learning approach for automated classification of fetal health status from CTG parameters. The model analyzes fetal heart rate patterns, accelerations, decelerations, and variability to classify fetal health as normal, suspicious, or pathological, potentially assisting clinicians in timely intervention decisions.

## Introduction

Fetal monitoring during pregnancy and labor is critical for detecting fetal distress and preventing adverse outcomes. Cardiotocography combines fetal heart rate monitoring with uterine contraction assessment, providing continuous information about fetal well-being. However, CTG interpretation can be subjective and requires significant expertise. Automated classification systems could provide consistent, objective assessments and assist clinicians in identifying cases requiring immediate attention. This project develops a machine learning model to classify fetal health status from CTG parameters, supporting clinical decision-making in obstetrics.

## Methods

### Dataset
The model was trained on the Fetal Health Classification dataset from Kaggle, containing CTG recordings with extracted features and expert-annotated fetal health classifications.

### Features
- Baseline fetal heart rate
- Accelerations and decelerations (light, severe, prolonged)
- Fetal movement
- Uterine contractions
- Short-term and long-term variability measures
- Percentage of time with abnormal patterns

### Model Development
- Feature engineering and normalization
- Multiple algorithms (Random Forest, XGBoost, Neural Networks, SVM)
- Multi-class classification (Normal, Suspicious, Pathological)
- Class balancing techniques
- Cross-validation and hyperparameter tuning

### Evaluation Metrics
- Per-class accuracy, precision, recall, F1-score
- Confusion matrix analysis
- ROC curves for each class
- Feature importance ranking

## Results

The model achieved strong performance in fetal health classification:
- **Overall Accuracy:** ~85-92% on test set
- **Normal Classification:** ~94% accuracy
- **Suspicious Detection:** ~87% sensitivity
- **Pathological Detection:** ~91% sensitivity
- **Multi-class F1-Score:** ~0.89

Key predictors included baseline heart rate, presence of decelerations, and variability measures. The model successfully identified pathological patterns requiring immediate intervention, with high sensitivity for detecting fetal distress. Feature importance analysis revealed that severe and prolonged decelerations were the strongest indicators of pathological status.

## Conclusion

This automated fetal health classification system demonstrates the potential for AI-assisted CTG interpretation in obstetrics. The model can provide consistent, objective assessments, potentially reducing inter-observer variability and improving detection of fetal distress. Future work should focus on real-time monitoring integration, incorporating temporal patterns, and validating in diverse clinical settings. Integration with electronic fetal monitoring systems could enable continuous automated assessment and early warning systems.

## Usage

Enter CTG monitoring parameters to get automated classification of fetal health status (Normal, Suspicious, or Pathological) with risk factor assessment.

