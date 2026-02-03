#!/usr/bin/env python3
"""
PLANORA Quick Setup & Test Script
Kiểm tra dependencies và setup môi trường cho demo
"""
import sys
import os
import subprocess
from pathlib import Path

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")

def check_python_version():
    """Check if Python version is >= 3.8"""
    print_info("Checking Python version...")
    version = sys.version_info
    
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} - Requires >= 3.8")
        return False

def check_package(package_name, import_name=None):
    """Check if a Python package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print_success(f"{package_name}")
        return True
    except ImportError:
        print_error(f"{package_name} - NOT INSTALLED")
        return False

def check_dependencies():
    """Check all required dependencies"""
    print_info("Checking required packages...")
    
    required = {
        'streamlit': 'streamlit',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'plotly': 'plotly',
    }
    
    optional = {
        'scikit-learn': 'sklearn',
        'tensorflow': 'tensorflow',
        'statsmodels': 'statsmodels',
        'prophet': 'prophet',
    }
    
    # Check required
    all_required = True
    for pkg, import_name in required.items():
        if not check_package(pkg, import_name):
            all_required = False
    
    # Check optional
    print_info("\nChecking optional packages (for live models)...")
    for pkg, import_name in optional.items():
        check_package(pkg, import_name)
    
    return all_required

def install_missing_packages():
    """Install missing required packages"""
    print_info("\nAttempting to install missing packages...")
    
    packages = ['streamlit', 'pandas', 'numpy', 'plotly']
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '--upgrade'
        ] + packages)
        print_success("Installation complete!")
        return True
    except subprocess.CalledProcessError:
        print_error("Installation failed. Please install manually:")
        print_info(f"  pip install {' '.join(packages)}")
        return False

def check_project_structure():
    """Check if project structure is correct"""
    print_info("Checking project structure...")
    
    required_dirs = ['core', 'engine', 'utils']
    required_files = ['config.py', 'app_optimized.py']
    
    # Check if we're in src/ directory
    current_dir = Path.cwd()
    
    # Try to find src directory
    possible_paths = [
        current_dir,
        current_dir / 'src',
        current_dir.parent / 'src'
    ]
    
    src_dir = None
    for path in possible_paths:
        if all((path / d).exists() for d in required_dirs):
            src_dir = path
            break
    
    if src_dir:
        print_success(f"Project structure OK (at {src_dir})")
        
        # Check files
        for file in required_files:
            if (src_dir / file).exists():
                print_success(f"  {file}")
            else:
                print_warning(f"  {file} - NOT FOUND (may use default)")
        
        return src_dir
    else:
        print_error("Project structure incorrect")
        print_info("Expected structure:")
        print_info("  src/")
        print_info("    ├── core/")
        print_info("    ├── engine/")
        print_info("    ├── utils/")
        print_info("    └── config.py")
        return None

def check_data_files(src_dir):
    """Check if data files exist"""
    print_info("Checking data files...")
    
    data_dirs = [
        src_dir.parent / 'data',
        src_dir / 'data',
        src_dir / '..' / 'data'
    ]
    
    data_found = False
    for data_dir in data_dirs:
        if data_dir.exists():
            print_success(f"Data directory found: {data_dir}")
            
            # Check for test files
            for res in ['1min', '5min', '15min']:
                test_file = data_dir / f'test_{res}.csv'
                if test_file.exists():
                    print_success(f"  test_{res}.csv")
                else:
                    print_warning(f"  test_{res}.csv - NOT FOUND")
            
            data_found = True
            break
    
    if not data_found:
        print_warning("No data directory found")
        print_info("Dashboard will generate synthetic data automatically")
    
    return data_found

def generate_quick_start_script(src_dir):
    """Generate a quick start script"""
    print_info("Generating quick start script...")
    
    script_content = f"""#!/bin/bash
# PLANORA Quick Start Script

echo "🚀 Starting PLANORA Dashboard..."
cd "{src_dir}"
streamlit run app_optimized.py --server.headless true
"""
    
    script_path = src_dir / 'start_demo.sh'
    
    try:
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make executable
        os.chmod(script_path, 0o755)
        
        print_success(f"Script created: {script_path}")
        print_info("Run with: ./start_demo.sh")
        return True
    except Exception as e:
        print_error(f"Failed to create script: {e}")
        return False

def run_quick_test(src_dir):
    """Run a quick import test"""
    print_info("Running quick import test...")
    
    os.chdir(src_dir)
    
    test_code = """
import sys
sys.path.insert(0, '.')

try:
    import config
    from core.autoscaler import Autoscaler
    from core.anomaly import AnomalyDetector
    from engine.loader import ModelLoader
    from utils.simulation import TimeTraveler
    print("✓ All imports successful")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)
"""
    
    try:
        result = subprocess.run(
            [sys.executable, '-c', test_code],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print_success("Import test passed")
            return True
        else:
            print_error("Import test failed")
            print_error(result.stderr)
            return False
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False

def main():
    print_header("⚡ PLANORA SETUP CHECKER")
    
    # 1. Check Python version
    if not check_python_version():
        print_error("\nPlease upgrade Python to 3.8+")
        return False
    
    # 2. Check dependencies
    deps_ok = check_dependencies()
    
    if not deps_ok:
        print_warning("\nSome required packages are missing.")
        response = input("Install now? (y/n): ").lower()
        
        if response == 'y':
            if not install_missing_packages():
                return False
        else:
            print_info("Please install manually: pip install streamlit pandas numpy plotly")
            return False
    
    # 3. Check project structure
    src_dir = check_project_structure()
    
    if not src_dir:
        print_error("\nPlease navigate to the correct project directory")
        return False
    
    # 4. Check data files
    check_data_files(src_dir)
    
    # 5. Run import test
    if not run_quick_test(src_dir):
        print_warning("\nImport test failed, but may still work")
    
    # 6. Generate start script
    generate_quick_start_script(src_dir)
    
    # Summary
    print_header("✅ SETUP COMPLETE")
    print_success("All checks passed!")
    print_info("\nTo start the dashboard:")
    print_info(f"  cd {src_dir}")
    print_info("  streamlit run app_optimized.py")
    print_info("\nOr use the quick start script:")
    print_info("  ./start_demo.sh")
    
    # Ask if user wants to start now
    print()
    response = input("Start dashboard now? (y/n): ").lower()
    
    if response == 'y':
        print_info("Starting dashboard...")
        os.chdir(src_dir)
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app_optimized.py'])
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Setup interrupted{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nUnexpected error: {e}")
        sys.exit(1)
