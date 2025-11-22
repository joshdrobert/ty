"""
Copy test data to static_pages directories for GitHub Pages
"""
import os
import shutil

PROJECTS = [
    'rucha', 'sammy', 'shalini', 'maansi', 'hannah', 'marygrace',
    'charmaine', 'fouzul', 'amirah', 'neha', 'annabelle', 'timi',
    'eric', 'cyril', 'chris', 'stephan', 'sabour', 'musa',
    'aaron', 'josh', 'jenna', 'taha'
]

def copy_test_data(project_name):
    """Copy test data to static_pages"""
    data_source = f'{project_name}/data'
    data_dest = f'{project_name}/static_pages/data'
    
    if not os.path.exists(data_source):
        print(f"⚠ {project_name}: No data directory found")
        return False
    
    os.makedirs(data_dest, exist_ok=True)
    
    # Copy test directory if it exists
    test_source = os.path.join(data_source, 'test')
    if os.path.exists(test_source):
        test_dest = os.path.join(data_dest, 'test')
        if os.path.exists(test_dest):
            shutil.rmtree(test_dest)
        shutil.copytree(test_source, test_dest)
        print(f"✓ {project_name}: Copied test/ directory")
    
    # Copy CSV files
    csv_files = [f for f in os.listdir(data_source) if f.endswith('.csv')]
    for csv_file in csv_files:
        src = os.path.join(data_source, csv_file)
        dst = os.path.join(data_dest, csv_file)
        shutil.copy2(src, dst)
        print(f"✓ {project_name}: Copied {csv_file}")
    
    # Copy other data files (for time-series)
    for item in os.listdir(data_source):
        item_path = os.path.join(data_source, item)
        if os.path.isfile(item_path) and item.endswith(('.csv', '.json', '.txt')):
            dst = os.path.join(data_dest, item)
            if not os.path.exists(dst):
                shutil.copy2(item_path, dst)
                print(f"✓ {project_name}: Copied {item}")
    
    return True

def main():
    print("="*70)
    print("Copying Test Data to Static Pages")
    print("="*70)
    
    for project in PROJECTS:
        copy_test_data(project)
    
    print("\n" + "="*70)
    print("✅ Test data copied to static_pages/data/ directories")
    print("="*70)

if __name__ == '__main__':
    main()

