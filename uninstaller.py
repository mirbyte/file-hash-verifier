import ctypes
import winreg
import os
import shutil
import sys
import tkinter as tk
from tkinter import messagebox
import time

# DPI Awareness
try:
    ctypes.windll.shcore.SetProcessDpiAwarenessContext(-2)
except (AttributeError, OSError):
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except (AttributeError, OSError):
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except (AttributeError, OSError):
            pass

# Constants
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 600


class Uninstaller:
    """
    Uninstaller for Hash Verifier that removes program files
    and registry entries from the system.
    """
    
    def __init__(self):
        """Initialize uninstaller and check for admin privileges."""
        if not self.is_admin():
            self.run_as_admin()
            sys.exit(0)
        
        self.window = tk.Tk()
        self.window.title("Hash Verifier Uninstaller (github/mirbyte)")
        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.window.resizable(True, True)
        
        self.install_dir = r"C:\Program Files\HashVerifier"
        
        self.setup_gui()
    
    def is_admin(self):
        """
        Check if running with administrator privileges.
        
        :return: True if admin, False otherwise
        """
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except AttributeError:
            return False
    
    def run_as_admin(self):
        """Restart the program with administrator privileges."""
        try:
            if getattr(sys, 'frozen', False):
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, "", None, 1
                )
            else:
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, f'"{__file__}"', None, 1
                )
        except Exception:
            messagebox.showerror("Error", "Administrator privileges are required for uninstallation.")
            sys.exit(1)
    
    def setup_gui(self):
        """Set up the graphical user interface."""
        main_frame = tk.Frame(self.window, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        info = tk.Label(main_frame,
            text="This will remove Hash Verifier from your system.\n\n"
                 "This will:\n"
                 "• Remove the context menu entry\n"
                 f"• Delete all files from {self.install_dir}\n\n"
                 "Administrator privileges are required.",
            font=("Segoe UI", 9),
            justify=tk.LEFT)
        info.pack(anchor=tk.W, pady=(0, 20))
        
        details_frame = tk.LabelFrame(main_frame, text="Current Status",
            padx=15, pady=15, font=("Segoe UI", 9, "bold"))
        details_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        registry_installed = self.is_registry_installed()
        files_exist = os.path.exists(self.install_dir)
        
        if registry_installed:
            status1 = tk.Label(details_frame, text="✓ Context menu entry is installed",
                font=("Segoe UI", 9), fg="#00aa00")
        else:
            status1 = tk.Label(details_frame, text="✗ Context menu entry not found",
                font=("Segoe UI", 9), fg="#666666")
        status1.pack(anchor=tk.W, pady=2)
        
        if files_exist:
            status2 = tk.Label(details_frame, text=f"✓ Program files exist in {self.install_dir}",
                font=("Segoe UI", 9), fg="#00aa00")
        else:
            status2 = tk.Label(details_frame, text="✗ Program files not found",
                font=("Segoe UI", 9), fg="#666666")
        status2.pack(anchor=tk.W, pady=2)
        
        if not registry_installed and not files_exist:
            tk.Label(details_frame, text="\n⚠ Hash Verifier appears to be already uninstalled",
                font=("Segoe UI", 9, "bold"), fg="#ff6600").pack(anchor=tk.W)
        
        button_frame = tk.Frame(main_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        
        cancel_btn = tk.Button(button_frame, text="Cancel", width=12,
            command=self.window.quit)
        cancel_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        uninstall_btn = tk.Button(button_frame, text="Uninstall", width=12,
            command=self.uninstall,
            bg="#cc0000", fg="white",
            font=("Segoe UI", 9, "bold"))
        uninstall_btn.pack(side=tk.RIGHT)
    
    def is_registry_installed(self):
        """
        Check if the registry entry exists.
        
        :return: True if installed, False otherwise
        """
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"Software\Classes\*\shell\HashVerifier",
                0, winreg.KEY_READ)
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            return False
        except Exception:
            return False
    
    def delete_registry_key_recursive(self, key, subkey):
        """
        Recursively delete a registry key and all its subkeys.
        
        :param key: Root registry key
        :param subkey: Path to subkey
        """
        try:
            with winreg.OpenKey(key, subkey, 0, winreg.KEY_ALL_ACCESS) as handle:
                subkeys = []
                try:
                    i = 0
                    while True:
                        subkeys.append(winreg.EnumKey(handle, i))
                        i += 1
                except OSError:
                    pass
                
                for sk in subkeys:
                    self.delete_registry_key_recursive(key, f"{subkey}\\{sk}")
            
            winreg.DeleteKey(key, subkey)
        except FileNotFoundError:
            pass
        except Exception as e:
            raise e
    
    def remove_directory_with_retry(self, path, retries=3, delay=0.5):
        """
        Remove directory with retry logic for locked files.
        
        :param path: Directory path to remove
        :param retries: Number of retry attempts
        :param delay: Delay between retries in seconds
        :return: True if successful
        """
        for attempt in range(retries):
            try:
                if os.path.exists(path):
                    shutil.rmtree(path)
                return True
            except PermissionError:
                if attempt < retries - 1:
                    time.sleep(delay)
                else:
                    raise
            except Exception:
                raise
        return False
    
    def uninstall(self):
        """Perform the uninstallation process."""
        try:
            try:
                self.delete_registry_key_recursive(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Classes\*\shell\HashVerifier"
                )
            except FileNotFoundError:
                pass
            except Exception as e:
                messagebox.showwarning("Registry Warning",
                    f"Failed to remove registry entries:\n{str(e)}\n\n"
                    "Continuing with file deletion...")
            
            if os.path.exists(self.install_dir):
                try:
                    self.remove_directory_with_retry(self.install_dir)
                except PermissionError:
                    messagebox.showerror("Permission Denied",
                        "Some files are in use and cannot be deleted.\n\n"
                        "Please close any running Hash Verifier instances and try again.")
                    return
            
            messagebox.showinfo("Success",
                "Hash Verifier has been successfully uninstalled!\n\n"
                "The context menu entry and all program files have been removed.")
            
            self.window.quit()
            
        except Exception as e:
            messagebox.showerror("Uninstall Failed",
                f"Failed to uninstall Hash Verifier:\n\n{str(e)}")
    
    def run(self):
        """Start the application main loop."""
        self.window.mainloop()


if __name__ == "__main__":
    app = Uninstaller()
    app.run()
