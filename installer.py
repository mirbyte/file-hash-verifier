import ctypes
import winreg
import os
import sys
import shutil
import tkinter as tk
from tkinter import messagebox

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
WINDOW_HEIGHT = 760



class Installer:
    """
    Installer for Hash Verifier that copies files to Program Files
    and adds a context menu entry for file hash verification.
    """
    
    def __init__(self):
        """Initialize installer and check for admin privileges."""
        if not self.is_admin():
            self.run_as_admin()
            sys.exit(0)
        
        self.window = tk.Tk()
        self.window.title("Hash Verifier Installer (github/mirbyte)")
        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.window.resizable(True, True)
        
        self.install_dir = r"C:\Program Files\HashVerifier"
        self.current_dir = self.get_current_dir()
        self.hash_verifier_source = os.path.join(self.current_dir, "HashVerifier.exe")
        
        self.setup_gui()
    
    def get_current_dir(self):
        """
        Get the directory where the installer is running from.
        
        :return: Directory path
        """
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))
    
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
            messagebox.showerror("Error", "Administrator privileges are required for installation.")
            sys.exit(1)
    
    def setup_gui(self):
        """Set up the graphical user interface."""
        main_frame = tk.Frame(self.window, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        info = tk.Label(main_frame,
            text="This will install Hash Verifier to your system and add\n"
                 "'Verify Hash' to the right-click context menu for all files.\n\n"
                 "Administrator privileges are required.",
            font=("Segoe UI", 9),
            justify=tk.LEFT)
        info.pack(anchor=tk.W, pady=(0, 20))
        
        details_frame = tk.LabelFrame(main_frame, text="Installation Details",
            padx=15, pady=15, font=("Segoe UI", 9, "bold"))
        details_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        if os.path.exists(self.hash_verifier_source):
            status_label = tk.Label(details_frame, text="✓ HashVerifier.exe found",
                font=("Segoe UI", 9), fg="#00aa00")
        else:
            status_label = tk.Label(details_frame, text="✗ HashVerifier.exe not found",
                font=("Segoe UI", 9, "bold"), fg="#cc0000")
        status_label.pack(anchor=tk.W, pady=(0, 10))
        
        tk.Label(details_frame, text="Install location:",
            font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(5, 2))
        
        install_display = tk.Text(details_frame, height=2, wrap=tk.WORD,
            font=("Segoe UI", 8), bg="#f0f0f0", relief=tk.FLAT)
        install_display.insert("1.0", self.install_dir)
        install_display.config(state=tk.DISABLED)
        install_display.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(details_frame, text="Files to install:",
            font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(5, 2))
        tk.Label(details_frame, text="• HashVerifier.exe (~15 MB)",
            font=("Segoe UI", 9)).pack(anchor=tk.W, padx=(10, 0))
        
        tk.Label(details_frame, text="Registry location:",
            font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(10, 2))
        
        reg_text = r"HKEY_CURRENT_USER\Software\Classes\*\shell\HashVerifier"
        reg_display = tk.Text(details_frame, height=2, wrap=tk.WORD,
            font=("Segoe UI", 8), bg="#f0f0f0", relief=tk.FLAT)
        reg_display.insert("1.0", reg_text)
        reg_display.config(state=tk.DISABLED)
        reg_display.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(details_frame, text="Context menu entry:",
            font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(10, 2))
        tk.Label(details_frame, text="'Verify Hash' (right-click any file)",
            font=("Segoe UI", 9), fg="#0066cc").pack(anchor=tk.W)
        
        button_frame = tk.Frame(main_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        cancel_btn = tk.Button(button_frame, text="Cancel", width=12,
            command=self.window.quit)
        cancel_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        self.install_btn = tk.Button(button_frame, text="Install", width=12,
            command=self.install,
            bg="#0066cc", fg="white",
            font=("Segoe UI", 9, "bold"))
        self.install_btn.pack(side=tk.RIGHT)
        
        if not os.path.exists(self.hash_verifier_source):
            self.install_btn.config(state=tk.DISABLED)
    
    def install(self):
        """Perform the installation process."""
        if not os.path.exists(self.hash_verifier_source):
            messagebox.showerror("Error",
                "HashVerifier.exe not found!\n\n"
                "Please make sure install.exe and HashVerifier.exe "
                "are in the same folder.")
            return
        
        try:
            os.makedirs(self.install_dir, exist_ok=True)
            
            dest_path = os.path.join(self.install_dir, "HashVerifier.exe")
            shutil.copy2(self.hash_verifier_source, dest_path)
            
            key_path = r"Software\Classes\*\shell\HashVerifier"
            
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "Verify Hash")
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, f'"{dest_path}",0')
            winreg.CloseKey(key)
            
            command_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path + r"\command")
            winreg.SetValueEx(command_key, "", 0, winreg.REG_SZ, f'"{dest_path}" "%1"')
            winreg.CloseKey(command_key)
            
            messagebox.showinfo("Success",
                "Hash Verifier has been successfully installed!\n\n"
                f"Installed to:\n{self.install_dir}\n\n"
                "Right-click any file and select 'Verify Hash' to use it.")
            
            self.window.quit()
            
        except PermissionError:
            messagebox.showerror("Permission Denied",
                "Failed to write to Program Files.\n\n"
                "Please run the installer as Administrator.")
        except OSError as e:
            messagebox.showerror("Installation Failed",
                f"Failed to copy files:\n\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Installation Failed",
                f"Failed to install Hash Verifier:\n\n{str(e)}")
    
    def run(self):
        """Start the application main loop."""
        self.window.mainloop()


if __name__ == "__main__":
    app = Installer()
    app.run()
