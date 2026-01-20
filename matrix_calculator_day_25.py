import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

class MatrixCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Calculator")
        self.root.geometry("900x600")
        self.root.configure(bg="#0f172a")

        self.create_ui()

    def create_ui(self):
        title = tk.Label(
            self.root,
            text="🧮 Matrix Calculator",
            font=("Segoe UI", 20, "bold"),
            bg="#0f172a",
            fg="white"
        )
        title.pack(pady=10)

        frame = tk.Frame(self.root, bg="#1e293b", padx=20, pady=20)
        frame.pack(pady=10)

        # Matrix size
        tk.Label(frame, text="Rows:", bg="#1e293b", fg="white").grid(row=0, column=0)
        tk.Label(frame, text="Columns:", bg="#1e293b", fg="white").grid(row=0, column=2)

        self.rows_entry = ttk.Entry(frame, width=10)
        self.rows_entry.grid(row=0, column=1)
        self.cols_entry = ttk.Entry(frame, width=10)
        self.cols_entry.grid(row=0, column=3)

        ttk.Button(frame, text="Create Matrices", command=self.create_matrices).grid(row=0, column=4, padx=10)

        # Matrix inputs
        self.matrix_frame = tk.Frame(self.root, bg="#0f172a")
        self.matrix_frame.pack()

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#0f172a")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Add", command=self.add).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Subtract", command=self.subtract).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Multiply", command=self.multiply).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Determinant (A)", command=self.determinant).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear).grid(row=0, column=4, padx=5)

        # Output
        self.output = tk.Text(
            self.root,
            height=10,
            width=100,
            bg="#020617",
            fg="cyan",
            font=("Consolas", 11)
        )
        self.output.pack(pady=10)

    def create_matrices(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        try:
            self.r = int(self.rows_entry.get())
            self.c = int(self.cols_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter valid rows & columns")
            return

        self.entries_A = []
        self.entries_B = []

        tk.Label(self.matrix_frame, text="Matrix A", bg="#0f172a", fg="white").grid(row=0, column=0, columnspan=self.c)
        tk.Label(self.matrix_frame, text="Matrix B", bg="#0f172a", fg="white").grid(row=0, column=self.c+1, columnspan=self.c)

        for i in range(self.r):
            rowA, rowB = [], []
            for j in range(self.c):
                e1 = ttk.Entry(self.matrix_frame, width=6)
                e1.grid(row=i+1, column=j, padx=2, pady=2)
                rowA.append(e1)

                e2 = ttk.Entry(self.matrix_frame, width=6)
                e2.grid(row=i+1, column=j+self.c+1, padx=2, pady=2)
                rowB.append(e2)

            self.entries_A.append(rowA)
            self.entries_B.append(rowB)

    def read_matrix(self, entries):
        try:
            return np.array([[float(e.get()) for e in row] for row in entries])
        except ValueError:
            messagebox.showerror("Error", "Fill all matrix values correctly")
            return None

    def display(self, result, title):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, title + "\n")
        self.output.insert(tk.END, "-" * 60 + "\n")
        self.output.insert(tk.END, str(result))

    def add(self):
        A = self.read_matrix(self.entries_A)
        B = self.read_matrix(self.entries_B)
        if A is not None and B is not None:
            self.display(A + B, "Matrix Addition Result")

    def subtract(self):
        A = self.read_matrix(self.entries_A)
        B = self.read_matrix(self.entries_B)
        if A is not None and B is not None:
            self.display(A - B, "Matrix Subtraction Result")

    def multiply(self):
        A = self.read_matrix(self.entries_A)
        B = self.read_matrix(self.entries_B)
        if A is not None and B is not None:
            try:
                self.display(np.dot(A, B), "Matrix Multiplication Result")
            except ValueError:
                messagebox.showerror("Error", "Invalid dimensions for multiplication")

    def determinant(self):
        A = self.read_matrix(self.entries_A)
        if A is not None:
            if A.shape[0] != A.shape[1]:
                messagebox.showerror("Error", "Determinant only for square matrix")
                return
            self.display(np.linalg.det(A), "Determinant of Matrix A")

    def clear(self):
        self.output.delete("1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixCalculatorApp(root)
    root.mainloop()
