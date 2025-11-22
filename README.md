# Medical AI Projects Portfolio

A collection of 22 medical AI classification projects, each trained on real Kaggle datasets and deployed as interactive web applications.

## Overview

This repository contains 22 independent medical AI projects covering various specialties:
- **Dermatology**: Skin cancer classification
- **Radiology**: Chest X-ray, brain MRI, CT scan analysis
- **Ophthalmology**: Diabetic retinopathy detection
- **Cardiology**: Heart failure prediction, echocardiogram analysis
- **Neurology**: EEG/EMG signal classification
- **Oncology**: Cancer detection and classification
- **And more...**

Each project includes:
- ✅ Trained deep learning model
- ✅ Interactive web interface
- ✅ Test dataset for evaluation
- ✅ Professional themed UI

## Projects

| Project | Specialty | Type | Classes |
|---------|-----------|------|---------|
| Rucha | Dermatology | Image | 2 |
| Sammy | Vascular Surgery | Tabular | 2 |
| Shalini | Synthetic Biology | Tabular | 3 |
| Maansi | Radiology | Image | 2 |
| Hannah | Pharmacogenetics | Tabular | 5 |
| MaryGrace | OBGYN | Tabular | 3 |
| Charmaine | Ophthalmology | Image | 5 |
| Fouzul | Vascular Medicine | Tabular | 2 |
| Amirah | Neuromuscular | Time-Series | 5 |
| Neha | Neonatology | Tabular | 2 |
| Annabelle | Pediatrics | Image | 2 |
| Timi | Stroke | Tabular | 2 |
| Eric | BCI/Neurosurgery | Time-Series | 5 |
| Cyril | Hepatology | Tabular | 2 |
| Chris | Neurology | Image | 4 |
| Stephan | Space Medicine | Tabular | 2 |
| Sabour | Urology | Tabular | 2 |
| Musa | Drug Delivery | Tabular | 5 |
| Aaron | Emergency Medicine | Tabular | 2 |
| Josh | Cardiology | Tabular | 2 |
| Jenna | Emergency Medicine | Tabular | 2 |
| Taha | Cardiology | Tabular | 2 |

## Setup

### Prerequisites
- Python 3.13+
- Virtual environment (recommended)

### Installation

```bash
# Clone repository
git clone https://github.com/joshdrobert/ty.git
cd ty

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Download Datasets

Datasets are available on Kaggle. See individual project READMEs for dataset links.

## Usage

### Train All Models

```bash
python3 train_all_models.py
```

This will train models for all 22 projects. Training time varies:
- **Tabular projects**: 1-3 minutes each
- **Image projects**: 15-90 minutes each

### Check Model Status

```bash
python3 check_models.py
```

### Run Individual Project

```bash
cd rucha
python3 app.py
# Visit http://localhost:8000
```

## Deployment

### GitHub Pages (Static Sites)

1. **Convert models to TensorFlow.js**:
   - Use `convert_models_colab.ipynb` in Google Colab
   - Or run locally: `python3 convert_models_to_tfjs.py`

2. **Generate static pages**:
   ```bash
   python3 convert_to_static.py
   python3 setup_github_pages.py
   ```

3. **Push to GitHub**:
   ```bash
   git add docs/ index.html
   git commit -m "Deploy to GitHub Pages"
   git push
   ```

4. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Source: Deploy from branch `main`
   - Folder: `/docs`

### Flask Deployment (Full Functionality)

Deploy individual Flask apps to:
- **Render.com** (free tier)
- **Railway.app** (free tier)
- **PythonAnywhere** (free tier)

## Project Structure

```
ty/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── index.html               # Main landing page
├── train_all_models.py      # Train all models
├── check_models.py          # Check model status
├── [project-name]/          # Individual project
│   ├── train.py            # Training script
│   ├── app.py              # Flask application
│   ├── models/             # Trained models
│   ├── data/               # Dataset
│   ├── templates/          # HTML templates
│   └── static/             # CSS/JS files
└── docs/                    # GitHub Pages output
```

## Technologies

- **Backend**: Flask, TensorFlow/Keras
- **Frontend**: HTML, CSS, JavaScript, TensorFlow.js
- **ML**: CNN, Dense Neural Networks
- **Data**: Pandas, NumPy, scikit-learn

## License

This project is for educational and research purposes.

## Contact

For questions or issues, please open a GitHub issue.
