import tkinter as tk
from tkinter import ttk, messagebox
import math

class EquationSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Equation Solver")
        self.root.geometry("750x520")
        self.root.configure(bg="#0f172a")

        self.create_ui()

    def create_ui(self):
        title = tk.Label(
            self.root,
            text="📐 Equation Solver (Linear & Quadratic)",
            font=("Segoe UI", 20, "bold"),
            bg="#0f172a",
            fg="white"
        )
        title.pack(pady=10)

        frame = tk.Frame(self.root, bg="#1e293b", padx=20, pady=20)
        frame.pack(pady=10)

        # Equation type
        tk.Label(frame, text="Equation Type:", bg="#1e293b", fg="white").grid(row=0, column=0, sticky="w")
        self.eq_type = tk.StringVar(value="Linear")
        ttk.Combobox(
            frame,
            textvariable=self.eq_type,
            values=["Linear", "Quadratic"],
            state="readonly",
            width=22
        ).grid(row=0, column=1)

        # Coefficients
        tk.Label(frame, text="a:", bg="#1e293b", fg="white").grid(row=1, column=0, sticky="w")
        self.a_entry = ttk.Entry(frame, width=25)
        self.a_entry.grid(row=1, column=1, pady=3)

        tk.Label(frame, text="b:", bg="#1e293b", fg="white").grid(row=2, column=0, sticky="w")
        self.b_entry = ttk.Entry(frame, width=25)
        self.b_entry.grid(row=2, column=1, pady=3)

        tk.Label(frame, text="c:", bg="#1e293b", fg="white").grid(row=3, column=0, sticky="w")
        self.c_entry = ttk.Entry(frame, width=25)
        self.c_entry.grid(row=3, column=1, pady=3)

        tk.Label(
            frame,
            text="(For Linear: ax + b = 0 | For Quadratic: ax² + bx + c = 0)",
            bg="#1e293b",
            fg="gray"
        ).grid(row=4, column=0, columnspan=2, pady=5)

        # Buttons
        ttk.Button(frame, text="Solve", command=self.solve).grid(row=5, column=0, pady=10)
        ttk.Button(frame, text="Clear", command=self.clear).grid(row=5, column=1)

        # Output
        self.output = tk.Text(
            self.root,
            height=12,
            width=90,
            bg="#020617",
            fg="cyan",
            font=("Consolas", 11)
        )
        self.output.pack(pady=10)

    def solve(self):
        self.output.delete("1.0", tk.END)

        try:
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            c = float(self.c_entry.get()) if self.eq_type.get() == "Quadratic" else None
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric coefficients")
            return

        if self.eq_type.get() == "Linear":
            self.solve_linear(a, b)
        else:
            self.solve_quadratic(a, b, c)

    def solve_linear(self, a, b):
        self.output.insert(tk.END, "Linear Equation: ax + b = 0\n")
        self.output.insert(tk.END, "-" * 50 + "\n")

        if a == 0:
            self.output.insert(tk.END, "Invalid equation (a cannot be 0)\n")
            return

        x = -b / a
        self.output.insert(tk.END, f"Step 1: ax = -b\n")
        self.output.insert(tk.END, f"Step 2: x = -b / a\n")
        self.output.insert(tk.END, f"Solution: x = {x}\n")

    def solve_quadratic(self, a, b, c):
        self.output.insert(tk.END, "Quadratic Equation: ax² + bx + c = 0\n")
        self.output.insert(tk.END, "-" * 50 + "\n")

        if a == 0:
            self.output.insert(tk.END, "This becomes a linear equation (a = 0)\n")
            return

        d = b**2 - 4*a*c
        self.output.insert(tk.END, f"Discriminant (D) = b² - 4ac = {d}\n\n")

        if d > 0:
            x1 = (-b + math.sqrt(d)) / (2*a)
            x2 = (-b - math.sqrt(d)) / (2*a)
            self.output.insert(tk.END, "Roots are real and distinct\n")
            self.output.insert(tk.END, f"x₁ = {x1}\n")
            self.output.insert(tk.END, f"x₂ = {x2}\n")

        elif d == 0:
            x = -b / (2*a)
            self.output.insert(tk.END, "Roots are real and equal\n")
            self.output.insert(tk.END, f"x = {x}\n")

        else:
            real = -b / (2*a)
            imag = math.sqrt(-d) / (2*a)
            self.output.insert(tk.END, "Roots are complex\n")
            self.output.insert(tk.END, f"x₁ = {real} + {imag}i\n")
            self.output.insert(tk.END, f"x₂ = {real} - {imag}i\n")

    def clear(self):
        self.a_entry.delete(0, tk.END)
        self.b_entry.delete(0, tk.END)
        self.c_entry.delete(0, tk.END)
        self.output.delete("1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = EquationSolverApp(root)
    root.mainloop()
