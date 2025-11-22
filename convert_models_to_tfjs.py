"""
Convert Keras models to TensorFlow.js format
Run this in Google Colab or local environment with TensorFlow.js converter
"""
import os
import subprocess

PROJECTS = [
    'rucha', 'sammy', 'shalini', 'maansi', 'hannah', 'marygrace',
    'charmaine', 'fouzul', 'amirah', 'neha', 'annabelle', 'timi',
    'eric', 'cyril', 'chris', 'stephan', 'sabour', 'musa',
    'aaron', 'josh', 'jenna', 'taha'
]

def convert_model_to_tfjs(project_name):
    """Convert Keras .h5 model to TensorFlow.js format"""
    model_path = f'{project_name}/models/best_model.h5'
    output_dir = f'{project_name}/static_pages/models'
    
    if not os.path.exists(model_path):
        print(f"⚠ {project_name}: No model found at {model_path}")
        return False
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Use tensorflowjs_converter
        cmd = [
            'tensorflowjs_converter',
            '--input_format', 'keras',
            '--output_format', 'tfjs_layers_model',
            model_path,
            output_dir
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ {project_name}: Model converted successfully")
            return True
        else:
            print(f"✗ {project_name}: Conversion failed")
            print(result.stderr)
            return False
    except FileNotFoundError:
        print(f"✗ tensorflowjs_converter not found. Install with: pip install tensorflowjs")
        return False

def main():
    print("="*70)
    print("Converting Keras Models to TensorFlow.js Format")
    print("="*70)
    print("\nThis script converts .h5 models to TensorFlow.js format")
    print("for browser-based inference.\n")
    print("Requirements:")
    print("  pip install tensorflowjs")
    print("="*70)
    
    results = {}
    for project in PROJECTS:
        results[project] = convert_model_to_tfjs(project)
    
    print("\n" + "="*70)
    print("Conversion Summary")
    print("="*70)
    
    successful = sum(1 for v in results.values() if v)
    print(f"✓ Successful: {successful}/22")
    
    if successful < 22:
        print(f"⚠ Failed: {22 - successful}/22")
        print("\nFailed projects:")
        for project, success in results.items():
            if not success:
                print(f"  - {project}")
    
    print("\n" + "="*70)
    print("Next Steps:")
    print("1. Models are now in static_pages/models/ directories")
    print("2. Test static pages locally")
    print("3. Push to GitHub Pages")
    print("="*70)

if __name__ == '__main__':
    main()

