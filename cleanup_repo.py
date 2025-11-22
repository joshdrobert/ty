"""
Clean up repository - remove unnecessary files and keep only essential ones
"""
import os
import shutil

# Files to KEEP (essential)
KEEP_FILES = {
    # Core files
    'README.md',
    'requirements.txt',
    '.gitignore',
    'index.html',
    
    # Essential scripts
    'train_all_models.py',
    'check_models.py',
    'verify_all_projects.py',
    'generate_projects.py',
    'professional_themes.py',
    
    # Conversion scripts (for GitHub Pages)
    'convert_to_static.py',
    'convert_models_to_tfjs.py',
    'convert_models_colab.ipynb',
    'setup_github_pages.py',
    'copy_test_data.py',
}

# Directories to KEEP
KEEP_DIRS = {
    'rucha', 'sammy', 'shalini', 'maansi', 'hannah', 'marygrace',
    'charmaine', 'fouzul', 'amirah', 'neha', 'annabelle', 'timi',
    'eric', 'cyril', 'chris', 'stephan', 'sabour', 'musa',
    'aaron', 'josh', 'jenna', 'taha',
    'docs',  # GitHub Pages output
    'venv',  # Virtual environment (if exists)
    '.git',  # Git directory
}

# Files to DELETE (temporary/documentation)
DELETE_PATTERNS = [
    # Temporary markdown files
    'TRAINING_*.md',
    'CHARMAINE_*.md',
    'CLASS_*.md',
    'WHY_*.md',
    'GITHUB_PAGES_*.md',
    'DEPLOYMENT_*.md',
    'DATASET_*.md',
    'FINAL_*.md',
    'VERIFIED_*.md',
    'ALL_*.md',
    'PROJECT_*.md',
    'FIXES_*.md',
    'DOWNLOAD_*.md',
    'SETUP_*.md',
    'QUICK_*.md',
    'README_*.md',  # Keep only main README.md
    
    # Temporary fix scripts
    'fix_*.py',
    'implement_*.py',
    'add_*.py',
    'update_*.py',
    'test_*.py',
    
    # Shell scripts (except essential ones)
    '*.sh',
]

def should_delete(filename):
    """Check if file should be deleted"""
    # Never delete keep files
    if filename in KEEP_FILES:
        return False
    
    # Check patterns
    for pattern in DELETE_PATTERNS:
        if pattern.startswith('*'):
            if filename.endswith(pattern[1:]):
                return True
        elif pattern.endswith('*'):
            if filename.startswith(pattern[:-1]):
                return True
        elif '*' in pattern:
            # Simple glob matching
            parts = pattern.split('*')
            if len(parts) == 2:
                if filename.startswith(parts[0]) and filename.endswith(parts[1]):
                    return True
    
    return False

def cleanup():
    """Clean up repository"""
    print("="*70)
    print("Cleaning Up Repository")
    print("="*70)
    print("\nThis will remove:")
    print("  - Temporary markdown documentation files")
    print("  - Temporary fix/implementation scripts")
    print("  - Duplicate/unnecessary files")
    print("\nKeeping:")
    print("  - All 22 project directories")
    print("  - Essential scripts (train_all_models.py, etc.)")
    print("  - Main README.md")
    print("  - Requirements and config files")
    print("="*70)
    
    deleted = []
    kept = []
    
    # Process files in root directory
    for item in os.listdir('.'):
        if os.path.isfile(item):
            if should_delete(item):
                try:
                    os.remove(item)
                    deleted.append(item)
                    print(f"✓ Deleted: {item}")
                except Exception as e:
                    print(f"✗ Error deleting {item}: {e}")
            else:
                kept.append(item)
    
    print("\n" + "="*70)
    print(f"✅ Cleanup Complete!")
    print(f"   Deleted: {len(deleted)} files")
    print(f"   Kept: {len(kept)} files")
    print("="*70)
    
    if deleted:
        print("\nDeleted files:")
        for f in sorted(deleted):
            print(f"  - {f}")
    
    print("\n" + "="*70)
    print("Repository is now clean and ready for GitHub!")
    print("="*70)

if __name__ == '__main__':
    cleanup()

