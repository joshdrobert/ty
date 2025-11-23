# Skin Cancer Classification - AI Diagnostic Tool

A professional web-based AI tool for classifying skin lesions as benign or malignant using deep learning. Deployed on GitHub Pages with TensorFlow.js for browser-based inference.

## 🎯 Features

- **Interactive Image Gallery**: Browse and select from pre-loaded test images
- **Real-time AI Analysis**: Instant predictions with confidence scores
- **Visual Results**: Probability bars and confidence indicators
- **Clinical Interpretation**: AI-generated insights with medical disclaimers
- **Professional UI**: Modern, responsive design optimized for medical applications

## 📊 Dataset

**Kaggle Dataset**: [Skin Cancer Malignant vs Benign](https://www.kaggle.com/datasets/fanconic/skin-cancer-malignant-vs-benign)

The dataset contains dermoscopy images of skin lesions labeled as either benign or malignant.

## 🚀 Setup Instructions

### 1. Download Dataset

```bash
# Install kagglehub if needed
pip install kagglehub

# Run the download script
python download_data.py
```

This will:
- Download the dataset from Kaggle
- Select 20 random test images from each class
- Save them to `data/test/` directory

### 2. Train the Model

```bash
python train_model.py
```

This will:
- Train a CNN model on the dataset
- Save the best model to `models/best_model.h5`
- Use data augmentation and validation split

### 3. Convert Model to TensorFlow.js

You need to convert the Keras `.h5` model to TensorFlow.js format:

```bash
# Install tensorflowjs
pip install tensorflowjs

# Convert the model
tensorflowjs_converter --input_format=keras models/best_model.h5 models/
```

This creates `models/model.json` and weight files that can be loaded in the browser.

### 4. Prepare Test Images for GitHub Pages

Copy test images to a location accessible by the HTML file:

```bash
# Create a web-accessible directory
mkdir -p data/test

# Copy test images (already done by download_data.py)
# Ensure images are committed to git for GitHub Pages
```

### 5. Update Model Path

In `app.js`, ensure the `MODEL_PATH` points to your converted model:

```javascript
const MODEL_PATH = 'models/model.json'; // Relative to index.html
```

### 6. Deploy to GitHub Pages

1. Commit all files to your repository
2. Go to repository Settings → Pages
3. Select the branch and folder (usually `docs/` or root)
4. Your site will be available at `https://[username].github.io/[repo]/rucha/`

## 📁 Project Structure

```
rucha/
├── index.html          # Main HTML interface
├── style.css           # Professional styling
├── app.js              # TensorFlow.js inference logic
├── download_data.py    # Kaggle dataset download script
├── train_model.py      # Model training script
├── models/             # Trained models (gitignored)
│   ├── best_model.h5
│   └── model.json      # TensorFlow.js model
├── data/               # Dataset (gitignored)
│   ├── train/
│   └── test/           # Test images for UI
└── README.md           # This file
```

## 🔧 Technical Details

- **Framework**: TensorFlow.js for browser-based inference
- **Model Architecture**: CNN with 4 convolutional layers + dense layers
- **Input Size**: 224x224 RGB images
- **Classes**: Benign (0), Malignant (1)
- **Deployment**: Static HTML/CSS/JS (GitHub Pages compatible)

## ⚠️ Medical Disclaimer

This tool is for **educational and research purposes only**. It should **NOT** be used as a substitute for professional medical diagnosis, treatment, or advice. Always consult with qualified healthcare professionals for medical concerns.

## 📝 Notes

- The model uses a mock prediction function if the actual model file is not found (for development)
- Test images should be committed to the repository for GitHub Pages deployment
- Model files are large and should be handled via Git LFS or external hosting
- The UI automatically handles model loading errors gracefully

## 🎨 UI Features

- **Status Indicator**: Shows model loading status
- **Image Gallery**: Grid layout with hover effects
- **Analysis Panel**: Split view with image and results
- **Confidence Visualization**: Progress bars and percentages
- **Responsive Design**: Works on desktop and mobile devices

