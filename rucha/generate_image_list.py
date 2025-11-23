"""
Generate a JSON file listing all test images for the web interface
"""
import json
import os
from pathlib import Path

test_dir = Path("data/test")
output_file = "test_images.json"

if not test_dir.exists():
    print(f"Error: Test directory not found at {test_dir}")
    print("Please run download_data.py first to download and prepare test images.")
    exit(1)

# Find all test images
test_images = []
for img_file in sorted(test_dir.glob("*.jpg")) + sorted(test_dir.glob("*.png")):
    label = "benign" if "benign" in img_file.name.lower() else "malignant"
    test_images.append({
        "path": f"data/test/{img_file.name}",
        "label": label,
        "id": len(test_images)
    })

# Save to JSON
with open(output_file, 'w') as f:
    json.dump(test_images, f, indent=2)

print(f"✓ Generated {output_file} with {len(test_images)} test images")
print(f"  - Benign: {sum(1 for img in test_images if img['label'] == 'benign')}")
print(f"  - Malignant: {sum(1 for img in test_images if img['label'] == 'malignant')}")

