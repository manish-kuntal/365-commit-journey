import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class FolderSizeAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Size Analyzer")
        self.root.geometry("900x600")
        self.root.configure(bg="#0f172a")

        self.create_header()
        self.create_body()

    def create_header(self):
        header = tk.Frame(self.root, bg="#312e81", height=70)
        header.pack(fill="x")
        tk.Label(header, text="📁 Folder Size Analyzer", fg="white", bg="#312e81",
                 font=("Segoe UI", 20, "bold")).pack(pady=15)

    def create_body(self):
        body = tk.Frame(self.root, bg="#0f172a", padx=20, pady=20)
        body.pack(fill="both", expand=True)

        btn_frame = tk.Frame(body, bg="#0f172a")
        btn_frame.pack(anchor="w", pady=5)
        ttk.Button(btn_frame, text="📂 Select Folder", command=self.select_folder).pack(side="left")

        self.path_var = tk.StringVar()
        tk.Entry(body, textvariable=self.path_var, width=90, state="readonly",
                 readonlybackground="#111827", fg="#38bdf8").pack(pady=10)

        # Treeview
        columns = ("Name", "Size (MB)")
        self.tree = ttk.Treeview(body, columns=columns, show="headings", height=18)
        self.tree.heading("Name", text="Name")
        self.tree.heading("Size (MB)", text="Size (MB)")
        self.tree.column("Name", width=600)
        self.tree.column("Size (MB)", width=150)
        self.tree.pack(fill="both", expand=True)

        # Total size
        self.total_var = tk.StringVar()
        tk.Label(body, text="Total Size:", fg="white", bg="#0f172a",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=5)
        tk.Entry(body, textvariable=self.total_var, width=40, state="readonly",
                 readonlybackground="#111827", fg="#38bdf8").pack(anchor="w")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_var.set(folder)
            self.analyze_folder(folder)

    def analyze_folder(self, folder):
        self.tree.delete(*self.tree.get_children())
        total_size = 0

        try:
            for root, dirs, files in os.walk(folder):
                for f in files:
                    path = os.path.join(root, f)
                    try:
                        size = os.path.getsize(path)
                        size_mb = round(size / (1024 * 1024), 3)
                        total_size += size
                        self.tree.insert("", "end", values=(path, size_mb))
                    except:
                        pass

            total_mb = round(total_size / (1024 * 1024), 3)
            self.total_var.set(f"{total_mb} MB")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderSizeAnalyzer(root)
    root.mainloop()
