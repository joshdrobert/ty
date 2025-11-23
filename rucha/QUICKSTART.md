# Quick Start Guide

## Step-by-Step Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download Dataset

```bash
python download_data.py
```

This downloads the Kaggle dataset and prepares 20 test images from each class.

### 3. Generate Image List

```bash
python generate_image_list.py
```

This creates `test_images.json` that the web interface uses to load test images.

### 4. Train Model

```bash
python train_model.py
```

This trains the CNN model and saves it to `models/best_model.h5`.

### 5. Convert to TensorFlow.js

```bash
python convert_to_tfjs.py
```

This converts the Keras model to TensorFlow.js format for browser deployment.

### 6. Deploy to GitHub Pages

1. Commit all files (including `data/test/` images and `models/model.json`)
2. Push to GitHub
3. Enable GitHub Pages in repository settings
4. Your site will be live!

## File Checklist

Before deploying, ensure you have:

- [x] `index.html` - Main interface
- [x] `style.css` - Styling
- [x] `app.js` - JavaScript logic
- [x] `test_images.json` - Image list
- [x] `models/model.json` - TensorFlow.js model
- [x] `data/test/*.jpg` - Test images (at least a few)

## Testing Locally

You can test the interface locally using a simple HTTP server:

```bash
# Python 3
python -m http.server 8000

# Then open http://localhost:8000 in your browser
```

## Troubleshooting

**Model not loading?**
- Ensure `models/model.json` exists
- Check browser console for errors
- Verify model path in `app.js`

**Test images not showing?**
- Run `generate_image_list.py` to create `test_images.json`
- Ensure images are in `data/test/` directory
- Check image paths in the JSON file

**GitHub Pages not working?**
- Ensure all files are committed
- Check that GitHub Pages is enabled
- Verify file paths are relative (not absolute)

