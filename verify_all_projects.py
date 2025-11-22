"""
Verify all 22 projects are set up correctly
"""
import os
import subprocess
import sys

PROJECTS = [
    'rucha', 'sammy', 'shalini', 'maansi', 'hannah', 'marygrace',
    'charmaine', 'fouzul', 'amirah', 'neha', 'annabelle', 'timi',
    'eric', 'cyril', 'chris', 'stephan', 'sabour', 'musa',
    'aaron', 'josh', 'jenna', 'taha'
]

def check_file_exists(project, filename):
    """Check if a file exists"""
    return os.path.exists(f'{project}/{filename}')

def check_model_exists(project):
    """Check if model exists"""
    return os.path.exists(f'{project}/models/best_model.h5')

def check_data_exists(project):
    """Check if data directory exists and has files"""
    data_dir = f'{project}/data'
    if not os.path.exists(data_dir):
        return False
    # Check if directory has files
    for root, dirs, files in os.walk(data_dir):
        if files:
            return True
    return False

def verify_project(project):
    """Verify a project is set up correctly"""
    issues = []
    
    # Check required files
    required_files = [
        'app.py',
        'train.py',
        'templates/index.html',
        'static/style.css',
        'static/app.js'
    ]
    
    for file in required_files:
        if not check_file_exists(project, file):
            issues.append(f"Missing: {file}")
    
    # Check data
    if not check_data_exists(project):
        issues.append("No data files found in data/ directory")
    
    # Check model (optional - may not be trained yet)
    has_model = check_model_exists(project)
    
    return {
        'project': project,
        'valid': len(issues) == 0,
        'issues': issues,
        'has_model': has_model
    }

def main():
    print("="*70)
    print("Verifying All 22 Medical AI Projects")
    print("="*70)
    
    results = []
    for project in PROJECTS:
        result = verify_project(project)
        results.append(result)
    
    print("\n" + "="*70)
    print("Verification Results")
    print("="*70)
    
    valid_count = sum(1 for r in results if r['valid'])
    model_count = sum(1 for r in results if r['has_model'])
    
    print(f"\n✓ Valid Projects: {valid_count}/22")
    print(f"✓ Trained Models: {model_count}/22")
    
    # Show valid projects
    print("\n✅ Valid Projects:")
    for r in results:
        if r['valid']:
            model_status = "✓ Model" if r['has_model'] else "⚠ No Model"
            print(f"  {r['project']:15} {model_status}")
    
    # Show projects with issues
    invalid = [r for r in results if not r['valid']]
    if invalid:
        print("\n⚠ Projects with Issues:")
        for r in invalid:
            print(f"\n  {r['project']}:")
            for issue in r['issues']:
                print(f"    - {issue}")
    
    # Show projects without models
    no_model = [r for r in results if r['valid'] and not r['has_model']]
    if no_model:
        print(f"\n⚠ Projects without trained models ({len(no_model)}):")
        for r in no_model:
            print(f"  - {r['project']}")
        print("\n  To train models, run: python3 train_all_models.py")
    
    print("\n" + "="*70)
    print("Summary")
    print("="*70)
    print(f"Total Projects: 22")
    print(f"Valid Setup: {valid_count}/22")
    print(f"Trained Models: {model_count}/22")
    
    if valid_count == 22 and model_count == 22:
        print("\n🎉 All projects are ready!")
        print("You can start Flask apps with: cd [project] && python3 app.py")
    elif valid_count == 22:
        print(f"\n⚠ All projects are set up, but {22 - model_count} models need training")
        print("Run: python3 train_all_models.py")
    else:
        print(f"\n⚠ {22 - valid_count} projects have setup issues that need to be fixed")
    
    print("="*70)

if __name__ == '__main__':
    main()

