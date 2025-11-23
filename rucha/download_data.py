"""
Download Kaggle dataset and prepare test images for GitHub Pages
"""
import kagglehub
import os
import shutil
from pathlib import Path
import random

# Download latest version
print("Downloading dataset from Kaggle...")
path = kagglehub.dataset_download("fanconic/skin-cancer-malignant-vs-benign")
print(f"Path to dataset files: {path}")

# Create data directory structure
data_dir = Path("data")
train_dir = data_dir / "train"
test_dir = data_dir / "test"
train_dir.mkdir(parents=True, exist_ok=True)
test_dir.mkdir(parents=True, exist_ok=True)

# Find train directories in downloaded dataset
dataset_train_path = Path(path) / "data" / "train"
benign_path = dataset_train_path / "benign"
malignant_path = dataset_train_path / "malignant"

# Copy training data to local data/train directory
print("\nCopying training data...")
if benign_path.exists():
    benign_train_dir = train_dir / "benign"
    benign_train_dir.mkdir(parents=True, exist_ok=True)
    benign_images = list(benign_path.glob("*.jpg")) + list(benign_path.glob("*.png"))
    for img in benign_images:
        dest = benign_train_dir / img.name
        if not dest.exists():  # Skip if already copied
            shutil.copy2(img, dest)
    print(f"  Copied {len(benign_images)} benign training images")

if malignant_path.exists():
    malignant_train_dir = train_dir / "malignant"
    malignant_train_dir.mkdir(parents=True, exist_ok=True)
    malignant_images = list(malignant_path.glob("*.jpg")) + list(malignant_path.glob("*.png"))
    for img in malignant_images:
        dest = malignant_train_dir / img.name
        if not dest.exists():  # Skip if already copied
            shutil.copy2(img, dest)
    print(f"  Copied {len(malignant_images)} malignant training images")

# Configuration: Number of test images per class
# Increase this if you want more test images in the web interface
TEST_IMAGES_PER_CLASS = 50  # Change this number as needed

# Select random test images from training data (before copying to avoid duplicates)
print(f"\nSelecting {TEST_IMAGES_PER_CLASS} test images per class...")
test_images = []

if benign_path.exists():
    benign_images = list(benign_path.glob("*.jpg")) + list(benign_path.glob("*.png"))
    num_benign = min(TEST_IMAGES_PER_CLASS, len(benign_images))
    selected_benign = random.sample(benign_images, num_benign)
    for img in selected_benign:
        dest = test_dir / f"benign_{img.name}"
        shutil.copy2(img, dest)
        test_images.append(("benign", str(dest)))
    print(f"  Selected {len(selected_benign)} benign test images (out of {len(benign_images)} available)")

if malignant_path.exists():
    malignant_images = list(malignant_path.glob("*.jpg")) + list(malignant_path.glob("*.png"))
    num_malignant = min(TEST_IMAGES_PER_CLASS, len(malignant_images))
    selected_malignant = random.sample(malignant_images, num_malignant)
    for img in selected_malignant:
        dest = test_dir / f"malignant_{img.name}"
        shutil.copy2(img, dest)
        test_images.append(("malignant", str(dest)))
    print(f"  Selected {len(selected_malignant)} malignant test images (out of {len(malignant_images)} available)")

print(f"\n✓ Total test images prepared: {len(test_images)}")
print(f"✓ Test images saved to: {test_dir}")

