"""
Check which models are trained across all 22 projects
"""
import os

PROJECTS = [
    'rucha', 'sammy', 'shalini', 'maansi', 'hannah', 'marygrace',
    'charmaine', 'fouzul', 'amirah', 'neha', 'annabelle', 'timi',
    'eric', 'cyril', 'chris', 'stephan', 'sabour', 'musa',
    'aaron', 'josh', 'jenna', 'taha'
]

def check_model(project_name):
    """Check if model exists and get file size"""
    model_path = f'{project_name}/models/best_model.h5'
    
    if os.path.exists(model_path):
        size = os.path.getsize(model_path)
        size_mb = size / (1024 * 1024)
        return True, size_mb
    return False, 0

def main():
    print("="*70)
    print("Checking Trained Models - All 22 Projects")
    print("="*70)
    print()
    
    trained = []
    not_trained = []
    
    for project in PROJECTS:
        has_model, size_mb = check_model(project)
        if has_model:
            trained.append((project, size_mb))
        else:
            not_trained.append(project)
    
    # Display trained models
    if trained:
        print("✅ TRAINED MODELS:")
        print("-"*70)
        for project, size in sorted(trained):
            print(f"  ✓ {project:15} {size:6.2f} MB")
        print()
    
    # Display untrained models
    if not_trained:
        print("⚠️  MODELS NOT TRAINED:")
        print("-"*70)
        for project in sorted(not_trained):
            print(f"  ✗ {project}")
        print()
    
    # Summary
    print("="*70)
    print(f"SUMMARY: {len(trained)}/22 models trained ({len(trained)*100//22}%)")
    print("="*70)
    
    if len(trained) < 22:
        print(f"\nTo train remaining {22 - len(trained)} models:")
        print("  python3 train_all_models.py")
    else:
        print("\n🎉 All models are trained!")
        print("\nNext step: Convert to TensorFlow.js for GitHub Pages")
        print("  Use convert_models_colab.ipynb in Google Colab")

if __name__ == '__main__':
    main()

