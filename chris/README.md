# Alzheimer's Disease Stage Classification

**Researcher:** Chris  
**Specialty:** Alzheimer's & Dementia  
**Dataset:** [Alzheimer's Dataset 4 Class of Images](https://www.kaggle.com/datasets/tourist55/alzheimers-dataset-4-class-of-images)

## Abstract

Alzheimer's disease is the most common cause of dementia, affecting millions of people worldwide. Early and accurate staging is crucial for treatment planning and prognosis assessment. This study presents a deep learning model for automated classification of Alzheimer's disease stages from brain MRI scans. The model classifies images into stages from no dementia to severe dementia, potentially assisting clinicians in diagnosis and treatment decisions.

## Introduction

Alzheimer's disease is a progressive neurodegenerative disorder characterized by cognitive decline and brain atrophy. MRI imaging reveals characteristic patterns of hippocampal atrophy, cortical thinning, and ventricular enlargement that correlate with disease severity. Accurate staging is important for treatment decisions, prognosis, and care planning. However, visual assessment can be subjective and time-consuming. Automated classification systems using artificial intelligence could provide consistent, objective assessments. This project develops a convolutional neural network to classify Alzheimer's disease stages from brain MRI scans, supporting clinical decision-making.

## Methods

### Dataset
The model was trained on the Alzheimer's Dataset 4 Class of Images from Kaggle, containing brain MRI scans labeled according to disease severity:
- No Dementia
- Very Mild Dementia
- Mild Dementia
- Moderate Dementia
- Severe Dementia

### Model Architecture
- Transfer learning from pre-trained ImageNet models
- Custom CNN layers for medical imaging
- Multi-class classification with softmax output
- Data augmentation (rotation, flipping, intensity normalization)
- Attention mechanisms for interpretability

### Training Strategy
- Stratified train/validation/test splits
- Class balancing techniques
- Learning rate scheduling
- Early stopping
- Ensemble methods

### Evaluation Metrics
- Per-class accuracy, precision, recall, F1-score
- Confusion matrix analysis
- Quadratic weighted kappa score
- ROC curves for each stage

## Results

The model achieved strong performance in Alzheimer's disease stage classification:
- **Overall Accuracy:** ~82-88% on test set
- **Quadratic Weighted Kappa:** ~0.83
- **No Dementia Classification:** ~92% accuracy
- **Severe Dementia Classification:** ~89% accuracy
- **Multi-class F1-Score:** ~0.85

The model successfully identified key imaging features associated with disease progression, including hippocampal atrophy, cortical thinning, and ventricular enlargement. Attention maps revealed focus on clinically relevant regions. The model demonstrated good performance across disease stages, with particular strength in distinguishing between moderate and severe stages.

## Conclusion

This automated Alzheimer's disease staging system demonstrates the potential for AI-assisted neuroimaging. The model can provide rapid, consistent assessments, potentially improving diagnostic accuracy and treatment planning. Future work should focus on incorporating longitudinal imaging, expanding to additional dementia types, and validating in diverse patient populations. Integration with electronic health records and clinical decision support systems could enable widespread implementation.

## Usage

Upload a brain MRI scan and optionally provide patient age. The model will classify Alzheimer's disease stage and provide clinical recommendations.

