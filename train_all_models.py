"""
Train models for all 22 projects
"""
import os
import subprocess
import sys

# Reordered: Fast tabular projects first, slow image projects last
# This way you get working models quickly while slow ones train in background
PROJECTS = [
    # Fast tabular projects (1-3 min each) - Train first
    'sammy', 'shalini', 'hannah', 'marygrace', 'fouzul', 'neha', 
    'timi', 'cyril', 'stephan', 'sabour', 'musa', 'aaron', 
    'josh', 'jenna', 'taha',
    # Fast time-series (3-5 min each)
    'amirah', 'eric',
    # Slow image projects (15-90 min each) - Train last
    'rucha',      # ~6.5K images, ~15-30 min
    'annabelle',  # ~11K images, ~30-60 min  
    'chris',      # ~7K images, ~20-40 min
    'maansi',     # ~11.7K images, ~30-60 min (PROBLEMATIC - nested dirs)
    'charmaine',  # ~32K images, ~60-90 min (LARGEST - CSV organization)
]

def check_model_exists(project):
    """Check if model already exists"""
    model_path = f'{project}/models/best_model.h5'
    return os.path.exists(model_path)

def train_project(project):
    """Train model for a project"""
    print(f"\n{'='*70}")
    print(f"Training: {project}")
    print(f"{'='*70}")
    
    if check_model_exists(project):
        print(f"✓ Model already exists for {project}, skipping...")
        return True
    
    os.chdir(project)
    try:
        result = subprocess.run(
            [sys.executable, 'train.py'],
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour timeout
        )
        
        if result.returncode == 0:
            print(f"✓ Successfully trained {project}")
            return True
        else:
            print(f"✗ Error training {project}:")
            print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print(f"✗ Timeout training {project}")
        return False
    except Exception as e:
        print(f"✗ Exception training {project}: {e}")
        return False
    finally:
        os.chdir('..')

def main():
    print("="*70)
    print("Training All 22 Medical AI Models")
    print("="*70)
    print(f"This will train models for all projects that don't have models yet.")
    print(f"Training may take 10-60 minutes per project depending on dataset size.")
    print("="*70)
    
    results = {}
    for project in PROJECTS:
        results[project] = train_project(project)
    
    print("\n" + "="*70)
    print("Training Summary")
    print("="*70)
    
    successful = sum(1 for v in results.values() if v)
    failed = sum(1 for v in results.values() if not v)
    
    print(f"✓ Successful: {successful}/22")
    if failed > 0:
        print(f"✗ Failed: {failed}/22")
        print("\nFailed projects:")
        for project, success in results.items():
            if not success:
                print(f"  - {project}")
    
    print("\n" + "="*70)
    print("Next Steps:")
    print("1. Review any failed training runs above")
    print("2. Run: python3 verify_all_projects.py")
    print("3. Start Flask apps: cd [project] && python3 app.py")
    print("="*70)

if __name__ == '__main__':
    main()

