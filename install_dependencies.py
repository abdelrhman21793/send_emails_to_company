#!/usr/bin/env python3
"""
Install Dependencies Script
This script installs all required dependencies for the email automation system.
"""

import subprocess
import sys
import os

def run_command(command):
    """Run a command and return success status."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)

def install_dependencies():
    """Install all required dependencies."""
    print("🔧 Installing Email Automation Dependencies...")
    print("=" * 50)
    
    dependencies = [
        "requests",
        "beautifulsoup4", 
        "pandas",
        "schedule",
        "pytz"
    ]
    
    print("📦 Required packages:")
    for dep in dependencies:
        print(f"  - {dep}")
    print()
    
    # Install each dependency
    success_count = 0
    for dep in dependencies:
        print(f"Installing {dep}...", end=" ")
        success, output = run_command(f"pip install {dep}")
        
        if success:
            print("✅")
            success_count += 1
        else:
            print("❌")
            print(f"Error: {output}")
    
    print()
    print(f"✅ Successfully installed {success_count}/{len(dependencies)} packages")
    
    if success_count == len(dependencies):
        print("🎉 All dependencies installed successfully!")
        return True
    else:
        print("⚠️  Some dependencies failed to install")
        return False

def check_python_version():
    """Check Python version."""
    print("🐍 Checking Python Version...")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 7:
        print("✅ Python version is compatible")
        return True
    else:
        print("❌ Python 3.7+ is required")
        return False

def create_requirements_file():
    """Create requirements.txt file."""
    print("📄 Creating requirements.txt...")
    
    requirements = [
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3",
        "pandas>=1.3.0",
        "schedule>=1.1.0",
        "pytz>=2021.1"
    ]
    
    try:
        with open('requirements.txt', 'w') as f:
            for req in requirements:
                f.write(req + '\n')
        print("✅ requirements.txt created")
        return True
    except Exception as e:
        print(f"❌ Error creating requirements.txt: {e}")
        return False

def main():
    """Main installation function."""
    print("🚀 EMAIL AUTOMATION SYSTEM - DEPENDENCY INSTALLER")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        print("Please upgrade Python to version 3.7 or higher")
        return
    
    print()
    
    # Create requirements file
    create_requirements_file()
    print()
    
    # Install dependencies
    if install_dependencies():
        print()
        print("=" * 60)
        print("🎉 INSTALLATION COMPLETE!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Run: python3 quick_start.py")
        print("2. Choose option 1 to setup your email credentials")
        print("3. Choose option 4 to start the scheduler")
        print()
        print("Your email automation system is ready! 🚀")
    else:
        print()
        print("❌ Installation failed. Please check the errors above.")
        print("You can try installing manually:")
        print("pip install requests beautifulsoup4 pandas schedule pytz")

if __name__ == "__main__":
    main() 