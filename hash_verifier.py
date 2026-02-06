import os
import sys
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import re
import ctypes

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
WINDOW_WIDTH = 750
WINDOW_HEIGHT = 800
BUFFER_SIZE = 65536  # 64KB

class HashVerifier:
    """
    HashVerifier class handles the process of verifying file hashes. 
    It computes hashes for a given file using multiple hashing algorithms 
    and compares them against a user-provided hash.
    """
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.window = tk.Tk()
        self.window.title("Hash Verifier v0.1")
        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.window.resizable(True, True)

        self.hashes = {}
        self.computation_time = 0
        
        self.setup_gui()
        self.window.after(100, self.calculate_hashes)
    
    def setup_gui(self):
        info_frame = tk.Frame(self.window, padx=10, pady=10)
        info_frame.pack(fill=tk.X)
        
        tk.Label(info_frame, text="File:", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W)
        
        filename = os.path.basename(self.filepath)
        file_label = tk.Label(info_frame, text=filename, font=("Segoe UI", 9), fg="#0066cc")
        file_label.pack(anchor=tk.W, pady=(0, 5))
        
        filesize = os.path.getsize(self.filepath)
        size_text = self.format_filesize(filesize)
        tk.Label(info_frame, text=f"Size: {size_text}", font=("Segoe UI", 9)).pack(anchor=tk.W)
        
        ttk.Separator(self.window, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        hash_frame = tk.Frame(self.window, padx=10)
        hash_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(hash_frame, text="Hash Values:", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        self.hash_widgets = {}
        algorithms = ["MD5", "SHA-1", "SHA-256", "SHA-512", "SHA3-256"]
        
        for algo in algorithms:
            row_frame = tk.Frame(hash_frame)
            row_frame.pack(fill=tk.X, pady=5)
            
            label = tk.Label(row_frame, text=f"{algo}:", font=("Segoe UI", 9, "bold"), width=12, anchor=tk.W)
            label.pack(side=tk.LEFT)
            
            value_entry = tk.Entry(row_frame, font=("Courier New", 9), state="readonly", readonlybackground="white")
            value_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
            
            copy_btn = tk.Button(row_frame, text="Copy", width=8, command=lambda a=algo: self.copy_hash(a))
            copy_btn.pack(side=tk.LEFT)
            
            self.hash_widgets[algo] = value_entry
        
        self.progress_frame = tk.Frame(hash_frame)
        self.progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_label = tk.Label(self.progress_frame, text="Computing hashes...", font=("Segoe UI", 9))
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode="determinate", length=400)
        self.progress_bar.pack(pady=5)
        
        self.time_label = tk.Label(hash_frame, text="", font=("Segoe UI", 9), fg="#666666")
        
        ttk.Separator(self.window, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        verify_frame = tk.LabelFrame(self.window, text="Verify Hash", padx=10, pady=10, font=("Segoe UI", 9, "bold"))
        verify_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Label(verify_frame, text="Paste expected hash or load from file:", font=("Segoe UI", 9)).pack(anchor=tk.W)
        
        input_frame = tk.Frame(verify_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        self.verify_entry = tk.Entry(input_frame, font=("Courier New", 9))
        self.verify_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.verify_btn = tk.Button(input_frame, text="Compare", width=10, command=self.verify_hash, state=tk.DISABLED)
        self.verify_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        load_file_btn = tk.Button(input_frame, text="Load File", width=10, command=self.load_hash_from_file, state=tk.DISABLED)
        load_file_btn.pack(side=tk.LEFT)
        self.load_file_btn = load_file_btn
        
        self.result_label = tk.Label(verify_frame, text="", font=("Segoe UI", 9, "bold"))
        self.result_label.pack(anchor=tk.W, pady=(5, 0))
        
        button_frame = tk.Frame(self.window, padx=10, pady=10)
        button_frame.pack(fill=tk.X)
        
        close_btn = tk.Button(button_frame, text="Close", width=12, command=self.window.quit)
        close_btn.pack(side=tk.RIGHT)
    
    def format_filesize(self, size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"
    
    def calculate_hashes(self):
        thread = threading.Thread(target=self._calculate_hashes_thread)
        thread.daemon = True
        thread.start()

    def _calculate_hashes_thread(self):
        try:
            start_time = time.time()

            hashers = {
                'MD5': hashlib.md5(),
                'SHA-1': hashlib.sha1(),
                'SHA-256': hashlib.sha256(),
                'SHA-512': hashlib.sha512(),
                'SHA3-256': hashlib.sha3_256()
            }

            md5 = hashers['MD5']
            sha1 = hashers['SHA-1']
            sha256 = hashers['SHA-256']
            sha512 = hashers['SHA-512']
            sha3_256 = hashers['SHA3-256']
            
            filesize = os.path.getsize(self.filepath)
            bytes_read = 0
            
            with open(self.filepath, 'rb') as f:
                while True:
                    data = f.read(BUFFER_SIZE)
                    if not data:
                        break
                    
                    md5.update(data)
                    sha1.update(data)
                    sha256.update(data)
                    sha512.update(data)
                    sha3_256.update(data)
                    
                    bytes_read += len(data)
                    progress = (bytes_read / filesize) * 100
                    self.window.after(0, lambda p=progress: self.progress_bar.config(value=p))
            
            end_time = time.time()
            self.computation_time = end_time - start_time
            self.hashes = {
                "MD5": md5.hexdigest(),
                "SHA-1": sha1.hexdigest(),
                "SHA-256": sha256.hexdigest(),
                "SHA-512": sha512.hexdigest(),
                "SHA3-256": sha3_256.hexdigest()
            }
            
            self.window.after(0, self.display_hashes)
        
        except PermissionError:
            self.window.after(0, lambda: self.show_error("Permission denied. File may be in use or protected."))
        except FileNotFoundError:
            self.window.after(0, lambda: self.show_error("File not found. It may have been moved or deleted."))
        except Exception as e:
            self.window.after(0, lambda: self.show_error(str(e)))
    
    def display_hashes(self):
        self.progress_frame.pack_forget()
        
        for algo, hash_value in self.hashes.items():
            entry = self.hash_widgets[algo]
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, hash_value)
            entry.config(state="readonly")
        
        time_text = f"Computed in {self.computation_time:.2f} seconds"
        self.time_label.config(text=time_text)
        self.time_label.pack(anchor=tk.W, pady=(5, 0))
        
        self.verify_btn.config(state=tk.NORMAL)
        self.load_file_btn.config(state=tk.NORMAL)
    
    def copy_hash(self, algorithm):
        hash_value = self.hashes.get(algorithm, "")
        if hash_value:
            self.window.clipboard_clear()
            self.window.clipboard_append(hash_value)
            self.window.update()

    def load_hash_from_file(self):
        file_path = filedialog.askopenfilename(
            title="Select hash file",
            filetypes=[("Text files", "*.txt *.md5 *.sha1 *.sha256 *.sha512"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(1024)  # Read first 1KB
                
            hex_pattern = r'\b[a-fA-F0-9]{32,128}\b'
            match = re.search(hex_pattern, content)
            
            if match:
                hash_value = match.group(0)
                self.verify_entry.delete(0, tk.END)
                self.verify_entry.insert(0, hash_value)
                self.verify_hash()  # Auto-verify
            else:
                messagebox.showerror("Error", "No valid hash found in file.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file:\n{str(e)}")

    def verify_hash(self):
        expected_hash = self.verify_entry.get().strip().lower()
        expected_hash = re.sub(r'[\s:\-]', '', expected_hash)
        
        if not expected_hash:
            self.result_label.config(text="⚠ Please enter a hash to compare", fg="#ff6600")
            return
        
        if not re.match(r'^[a-f0-9]+$', expected_hash):
            self.result_label.config(text="⚠ Invalid hash format (must be hexadecimal)", fg="#ff6600")
            return
        
        hash_length = len(expected_hash)
        
        algo_map = {
            32: "MD5",
            40: "SHA-1",
            64: ("SHA-256", "SHA3-256"),
            128: "SHA-512"
        }
        
        detected_algo = algo_map.get(hash_length)
        
        if not detected_algo:
            self.result_label.config(text="⚠ Invalid hash length", fg="#ff6600")
            return
        
        if isinstance(detected_algo, tuple):
            for algo in detected_algo:
                actual_hash = self.hashes.get(algo, "").lower()
                if expected_hash == actual_hash:
                    self.result_label.config(text=f"✓ Match! ({algo})", fg="#00aa00")
                    return
            self.result_label.config(text=f"✗ No Match (compared as SHA-256/SHA3-256)", fg="#cc0000")
        else:
            actual_hash = self.hashes.get(detected_algo, "").lower()
            if expected_hash == actual_hash:
                self.result_label.config(text=f"✓ Match! ({detected_algo})", fg="#00aa00")
            else:
                self.result_label.config(text=f"✗ No Match (compared as {detected_algo})", fg="#cc0000")

    def show_error(self, error_msg):
        self.progress_frame.pack_forget()
        messagebox.showerror("Error", f"Failed to calculate hashes:\n{error_msg}")
        self.window.quit()
    
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        messagebox.showerror("Error", "No file selected.\n\nUsage: HashVerifier.exe <filepath>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not os.path.exists(filepath):
        messagebox.showerror("Error", f"File not found:\n{filepath}")
        sys.exit(1)
    
    if os.path.isdir(filepath):
        messagebox.showerror("Error", "Folders are not supported.\nPlease select a file.")
        sys.exit(1)
    
    app = HashVerifier(filepath)
    app.run()
