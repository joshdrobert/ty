"""
Setup GitHub Pages structure - move static_pages to root for GitHub Pages
"""
import os
import shutil

PROJECTS = [
    'rucha', 'sammy', 'shalini', 'maansi', 'hannah', 'marygrace',
    'charmaine', 'fouzul', 'amirah', 'neha', 'annabelle', 'timi',
    'eric', 'cyril', 'chris', 'stephan', 'sabour', 'musa',
    'aaron', 'josh', 'jenna', 'taha'
]

def setup_github_pages():
    """Move static_pages to root level for GitHub Pages"""
    
    print("Setting up GitHub Pages structure...")
    print("="*70)
    
    # Create docs directory (GitHub Pages can serve from /docs)
    docs_dir = 'docs'
    os.makedirs(docs_dir, exist_ok=True)
    
    # Copy main index.html
    if os.path.exists('index.html'):
        shutil.copy('index.html', os.path.join(docs_dir, 'index.html'))
        print("✓ Copied main index.html")
    
    # Move each project's static_pages to docs/[project]/
    for project in PROJECTS:
        static_source = f'{project}/static_pages'
        static_dest = os.path.join(docs_dir, project)
        
        if os.path.exists(static_source):
            if os.path.exists(static_dest):
                shutil.rmtree(static_dest)
            shutil.copytree(static_source, static_dest)
            print(f"✓ Moved {project}/static_pages → docs/{project}/")
        else:
            print(f"⚠ {project}: static_pages not found (run convert_to_static.py first)")
    
    print("\n" + "="*70)
    print("✅ GitHub Pages structure ready!")
    print("\nNext steps:")
    print("1. Convert models to TensorFlow.js (use Colab notebook)")
    print("2. Copy model.json files to docs/[project]/models/")
    print("3. Copy test data to docs/[project]/data/")
    print("4. Push to GitHub and enable Pages from /docs directory")
    print("="*70)

if __name__ == '__main__':
    setup_github_pages()

