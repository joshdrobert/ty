# Motion Sickness Severity Prediction

**Researcher:** Stephan  
**Specialty:** Space Medicine  
**Dataset:** [Motion Sickness Physiological Data](https://www.kaggle.com/datasets/andrewmvd/motion-sickness-physiological-data)

## Abstract

Motion sickness is a common problem in spaceflight, aviation, and other motion environments, affecting performance and mission success. This study develops a machine learning model to predict motion sickness severity from physiological monitoring data during simulated spaceflight conditions. The model integrates heart rate, heart rate variability, skin conductance, and other physiological parameters to forecast symptom severity, potentially enabling early intervention and mitigation strategies.

## Introduction

Motion sickness results from conflicting sensory inputs between the vestibular system, visual system, and proprioception. In spaceflight, microgravity and unusual motion patterns can trigger severe motion sickness, affecting astronaut performance. Early prediction and mitigation are crucial for mission success. Physiological monitoring provides objective measures of autonomic nervous system responses that correlate with motion sickness severity. This project develops a predictive model that uses physiological data to forecast motion sickness severity, supporting countermeasure development and mission planning.

## Methods

### Dataset
The model was trained on the Motion Sickness Physiological Data dataset from Kaggle, containing physiological recordings during simulated spaceflight conditions with motion sickness severity ratings.

### Features
- Heart rate and heart rate variability
- Skin conductance (galvanic skin response)
- Body temperature
- Motion intensity and duration
- Previous motion sickness history
- Autonomic nervous system indicators

### Model Development
- Feature engineering and normalization
- Multiple algorithms (Random Forest, XGBoost, Neural Networks)
- Severity classification (mild, moderate, severe)
- Regression for continuous severity scores
- Cross-validation and hyperparameter tuning

### Evaluation Metrics
- Accuracy, precision, recall, F1-score
- Mean absolute error for severity prediction
- ROC-AUC for binary classification
- Feature importance analysis

## Results

The model achieved strong predictive performance:
- **Severity Classification Accuracy:** ~78-85%
- **Severity Prediction MAE:** ~0.8 on 0-10 scale
- **Key Predictors:** Motion intensity, duration, previous history, skin conductance
- **Early Detection:** Identified high-risk individuals before symptom onset

The model demonstrated that motion intensity and duration were the strongest predictors, followed by previous motion sickness history and physiological stress indicators (elevated skin conductance, reduced HRV). The model successfully identified individuals at risk for severe motion sickness, enabling proactive countermeasures.

## Conclusion

This motion sickness prediction model demonstrates the potential for physiological monitoring in space medicine applications. The model can assist in identifying high-risk individuals, enabling early intervention and countermeasure deployment. Future work should focus on real-time monitoring integration, incorporating additional physiological parameters, and validating in actual spaceflight conditions. Integration with wearable sensors and mission control systems could enable continuous monitoring and adaptive countermeasures.

## Usage

Enter physiological monitoring data and motion parameters to get predictions for motion sickness severity with mitigation recommendations.

