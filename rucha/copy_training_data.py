"""
Copy training data from Kaggle cache to local data/train directory
Run this if you already downloaded test images but need training data
"""
import shutil
from pathlib import Path

# Kaggle cache location (where kagglehub downloads datasets)
kaggle_cache = Path.home() / ".cache" / "kagglehub" / "datasets" / "fanconic" / "skin-cancer-malignant-vs-benign"
dataset_train_path = None

# Find the latest version
if kaggle_cache.exists():
    versions = sorted([d for d in kaggle_cache.iterdir() if d.is_dir() and d.name.isdigit()])
    if versions:
        dataset_train_path = versions[-1] / "data" / "train"
        print(f"Found dataset at: {dataset_train_path}")
    else:
        print("No dataset versions found. Please run download_data.py first.")
        exit(1)
else:
    print("Kaggle cache not found. Please run download_data.py first.")
    exit(1)

# Create local training directory
train_dir = Path("data") / "train"
benign_train_dir = train_dir / "benign"
malignant_train_dir = train_dir / "malignant"
benign_train_dir.mkdir(parents=True, exist_ok=True)
malignant_train_dir.mkdir(parents=True, exist_ok=True)

# Copy training images
benign_path = dataset_train_path / "benign"
malignant_path = dataset_train_path / "malignant"

print("\nCopying training data...")
if benign_path.exists():
    benign_images = list(benign_path.glob("*.jpg")) + list(benign_path.glob("*.png"))
    copied = 0
    for img in benign_images:
        dest = benign_train_dir / img.name
        if not dest.exists():
            shutil.copy2(img, dest)
            copied += 1
    print(f"  Copied {copied} new benign images (total: {len(benign_images)} available)")
    print(f"  Benign training images: {len(list(benign_train_dir.glob('*')))}")

if malignant_path.exists():
    malignant_images = list(malignant_path.glob("*.jpg")) + list(malignant_path.glob("*.png"))
    copied = 0
    for img in malignant_images:
        dest = malignant_train_dir / img.name
        if not dest.exists():
            shutil.copy2(img, dest)
            copied += 1
    print(f"  Copied {copied} new malignant images (total: {len(malignant_images)} available)")
    print(f"  Malignant training images: {len(list(malignant_train_dir.glob('*')))}")

print(f"\n✓ Training data ready at: {train_dir}")
print("You can now run: python train_model.py")

