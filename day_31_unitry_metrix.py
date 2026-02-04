import tkinter as tk
from tkinter import messagebox
import numpy as np

class UnitaryCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unitary Matrix Checker")
        self.root.geometry("900x600")
        self.root.configure(bg="#0f172a")

        self.entries = []
        self.size_var = tk.IntVar(value=2)

        self.create_ui()

    def create_ui(self):
        tk.Label(self.root, text="🔷 Unitary Matrix Checker",
                 font=("Segoe UI", 20, "bold"),
                 bg="#0f172a", fg="white").pack(pady=10)

        top = tk.Frame(self.root, bg="#1e293b", padx=20, pady=15)
        top.pack()

        tk.Label(top, text="Matrix Size (n x n):",
                 bg="#1e293b", fg="white").grid(row=0, column=0)

        tk.Spinbox(top, from_=2, to=6, textvariable=self.size_var,
                   width=5).grid(row=0, column=1, padx=5)

        tk.Button(top, text="Create Matrix",
                  bg="#2563eb", fg="white",
                  command=self.create_matrix).grid(row=0, column=2, padx=10)

        self.matrix_frame = tk.Frame(self.root, bg="#0f172a")
        self.matrix_frame.pack(pady=15)

        tk.Button(self.root, text="Check Unitary",
                  bg="#22c55e", fg="white",
                  font=("Segoe UI", 10, "bold"),
                  command=self.check).pack(pady=10)

        self.result = tk.Label(self.root, text="",
                               bg="#0f172a", fg="#93c5fd",
                               font=("Segoe UI", 12))
        self.result.pack(pady=10)

    def create_matrix(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        self.entries = []
        n = self.size_var.get()

        for i in range(n):
            row = []
            for j in range(n):
                e = tk.Entry(self.matrix_frame, width=6,
                             bg="#020617", fg="white",
                             insertbackground="white", justify="center")
                e.grid(row=i, column=j, padx=5, pady=5)
                row.append(e)
            self.entries.append(row)

    def check(self):
        try:
            matrix = []
            for row in self.entries:
                matrix.append([complex(e.get()) for e in row])

            U = np.array(matrix)
            I = np.eye(U.shape[0])
            check = np.allclose(U.conj().T @ U, I)

            if check:
                self.result.config(text="✅ This matrix is UNitary")
            else:
                self.result.config(text="❌ This matrix is NOT unitary")

        except:
            messagebox.showerror("Error", "Please enter valid numbers!")

# ---- RUN ----
if __name__ == "__main__":
    root = tk.Tk()
    app = UnitaryCheckerApp(root)
    root.mainloop()
