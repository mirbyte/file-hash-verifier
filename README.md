# File Hash Verifier

A lightweight Windows application for calculating and verifying file hashes using multiple algorithms. File Hash Verifier supports MD5, SHA-1, SHA-256, SHA-512, and SHA3-256, with seamless Windows Explorer context menu integration for quick file verification.

***

## Features

* **Multiple hash algorithms**: Calculate MD5, SHA-1, SHA-256, SHA-512, and SHA3-256 hashes
* **Hash verification**: Compare computed hashes against expected values
* **Load from file**: Import hash values from text files (*.md5, *.sha256, etc.)
* **Context menu integration**: Right-click any file in Windows Explorer to verify its hash
* **Progress tracking**: Real-time progress bar with computation time display
* **User-friendly GUI**: Clean, intuitive interface built with Tkinter

***

## Installation

### Quick Install

1. Download the latest release from the [releases page](https://github.com/mirbyte/file-hash-verifier/releases)
2. Extract the ZIP file containing three executables:
    - `HashVerifier.exe` - Main application
    - `install.exe` - Installer
    - `uninstall.exe` - Uninstaller
3. Run `install.exe` to install File Hash Verifier
4. The installer will automatically add a "Verify Hash" entry to your right-click context menu

**Note**: Administrator privileges are required for installation to Program Files.

### Uninstall

1. Run `uninstall.exe` from the installation directory or your downloads folder
2. Confirm the uninstallation
3. All program files and registry entries will be removed

***

## Usage

### Via Context Menu

1. Right-click any file in Windows Explorer
2. Select **"Verify Hash"** from the context menu
3. The application opens and automatically calculates all hash values
4. Copy individual hashes or paste an expected hash to verify

### Verifying Hashes

**Method 1: Paste hash directly**

1. Copy the expected hash value
2. Paste it into the "Verify Hash" input field
3. Click **Compare**
4. Result displays as ✓ Match or ✗ No Match

**Method 2: Load from file**

1. Click **Load File**
2. Select a text file containing the hash (*.txt, *.md5, *.sha256, etc.)
3. The application automatically extracts and compares the hash

***

## Building from Source

For developers who want to build from source or contribute:

### Prerequisites

- Python 3.7 or higher
- PyInstaller


### Build Steps

1. Clone the repository:

```bash
git clone https://github.com/mirbyte/file-hash-verifier.git
cd file-hash-verifier
```

2. Install PyInstaller:

```bash
pip install pyinstaller
```

3. Run the build script:

```bash
python build_all.py
```


The `dist` folder will contain:

- `HashVerifier.exe` (~15 MB)
- `install.exe` (~10 MB)
- `uninstall.exe` (~10 MB)

***

## Technical Details

### Supported Hash Algorithms

| Algorithm | Output Length | Use Case |
| :-- | :-- | :-- |
| MD5 | 32 hex chars | Legacy compatibility |
| SHA-1 | 40 hex chars | Legacy compatibility |
| SHA-256 | 64 hex chars | Modern standard |
| SHA-512 | 128 hex chars | High security |
| SHA3-256 | 64 hex chars | Modern alternative |

### System Requirements

- **OS**: Windows 10 or later (Windows 11 supported)
- **Disk Space**: 20 MB for installation
- **Privileges**: Administrator rights required for installation


### Installation Location

- Program files: `C:\Program Files\HashVerifier\`
- Registry key: `HKEY_CURRENT_USER\Software\Classes\*\shell\HashVerifier`


***

## Acknowledgments

- Built with [Python](https://www.python.org/)
- GUI powered by [Tkinter](https://docs.python.org/3/library/tkinter.html)
- Packaged with [PyInstaller](https://pyinstaller.org/)

***

## Author

Created by [@mirbyte](https://github.com/mirbyte)

***

**Star ⭐ this repository if you find it useful!**

