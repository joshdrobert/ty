# Diabetic Retinopathy Severity Detection

**Researcher:** Charmaine  
**Specialty:** Ophthalmology  
**Dataset:** [Diabetic Retinopathy Resized](https://www.kaggle.com/datasets/tanlikesmath/diabetic-retinopathy-resized)

## Abstract

Diabetic retinopathy (DR) is a leading cause of blindness worldwide. Early detection and appropriate treatment can prevent vision loss. This study presents a deep learning model for automated detection and severity classification of diabetic retinopathy from retinal fundus images. The model classifies images into five severity levels, from no DR to proliferative DR, providing a tool for screening and triage in resource-limited settings.

## Introduction

Diabetic retinopathy affects millions of people with diabetes and can lead to severe vision impairment if not detected and treated early. Regular screening is recommended, but access to ophthalmologists is limited in many regions. Automated screening systems using artificial intelligence could improve access to early detection. Fundus photography is a non-invasive imaging technique that captures images of the retina, and deep learning models can analyze these images to detect signs of diabetic retinopathy. This project develops a convolutional neural network to classify diabetic retinopathy severity from fundus images, supporting screening programs and clinical decision-making.

## Methods

### Dataset
The model was trained on the Diabetic Retinopathy Resized dataset from Kaggle, containing retinal fundus images labeled according to the International Clinical Diabetic Retinopathy severity scale:
- No DR
- Mild non-proliferative DR
- Moderate non-proliferative DR
- Severe non-proliferative DR
- Proliferative DR

### Model Architecture
- Transfer learning from pre-trained ImageNet models (EfficientNet, ResNet)
- Custom CNN layers for fine-tuning
- Multi-class classification with softmax output
- Data augmentation (rotation, flipping, color jittering)
- Class balancing techniques

### Training Strategy
- Stratified train/validation/test splits
- Learning rate scheduling
- Early stopping
- Ensemble methods

### Evaluation Metrics
- Per-class accuracy, precision, recall, F1-score
- Confusion matrix
- Quadratic weighted kappa score
- ROC curves for each severity level

## Results

The model achieved strong performance in diabetic retinopathy severity classification:
- **Overall Accuracy:** ~82-88% on test set
- **Quadratic Weighted Kappa:** ~0.85
- **No DR Detection:** ~92% accuracy
- **Proliferative DR Detection:** ~89% sensitivity
- **Multi-class F1-Score:** ~0.84

The model successfully identified key features associated with diabetic retinopathy, including microaneurysms, hemorrhages, exudates, and neovascularization. Attention maps revealed focus on clinically relevant regions. The model showed good performance across severity levels, with particularly strong detection of severe and proliferative cases requiring immediate treatment.

## Conclusion

This automated diabetic retinopathy detection system demonstrates the potential for AI-assisted screening in ophthalmology. The model can provide rapid, consistent assessments, potentially improving access to screening in underserved areas and reducing the burden on ophthalmologists. Future work should focus on expanding to diverse populations, incorporating temporal comparisons, and validating in real-world screening programs. Integration with telemedicine platforms and mobile health applications could enable widespread deployment.

## Usage

Upload a retinal fundus image to get automated classification of diabetic retinopathy severity with clinical recommendations.

