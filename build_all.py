import os
import subprocess
import sys
import shutil


def run_command(command, description):
    """
    Execute a shell command and handle errors.
    
    :param command: Command to execute
    :param description: Description of the command
    """
    print(f"\n{'='*60}")
    print(f" {description}")
    print('='*60)
    
    result = subprocess.run(command, shell=True)
    
    if result.returncode != 0:
        print(f"\n❌ ERROR: {description} failed!")
        sys.exit(1)
    
    print(f"✓ {description} completed successfully!")


def main():
    """Main build process for Hash Verifier executable files."""
    print("\n" + "="*60)
    print(" Hash Verifier - Build Script")
    print("="*60)
    
    print("\nChecking dependencies...")
    result = subprocess.run("pyinstaller --version", shell=True, capture_output=True)
    
    if result.returncode != 0:
        print("\n❌ PyInstaller is not installed!")
        print("\nPlease install it with:")
        print("  pip install pyinstaller")
        sys.exit(1)
    
    print("✓ PyInstaller is installed")
    
    print("\nCleaning previous builds...")
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"  Removed {folder}/")
    
    for spec_file in ['HashVerifier.spec', 'install.spec', 'uninstall.spec']:
        if os.path.exists(spec_file):
            os.remove(spec_file)
            print(f"  Removed {spec_file}")
    
    run_command(
        "pyinstaller --onefile --windowed --name HashVerifier --clean hash_verifier.py",
        "Building HashVerifier.exe"
    )
    
    run_command(
        "pyinstaller --onefile --windowed --name install --clean installer.py",
        "Building install.exe"
    )
    
    run_command(
        "pyinstaller --onefile --windowed --name uninstall --clean uninstaller.py",
        "Building uninstall.exe"
    )
    
    print("\n" + "="*60)
    print(" ✓ BUILD COMPLETE!")
    print("="*60)
    print("\nYour executables are in the 'dist' folder:")
    print("  - HashVerifier.exe (~15 MB)")
    print("  - install.exe (~10 MB)")
    print("  - uninstall.exe (~10 MB)")
    print("\nTo distribute:")
    print("  1. Copy all 3 .exe files to a folder")
    print("  2. Zip them up")
    print("  3. Users run install.exe to add context menu")
    print("\nDone! 🎉")


if __name__ == "__main__":
    main()
