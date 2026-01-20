import tkinter as tk
from tkinter import ttk, messagebox
import math

class FactorFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Factor Finder")
        self.root.geometry("700x500")
        self.root.configure(bg="#0f172a")

        self.history = []
        self.create_ui()

    def create_ui(self):
        title = tk.Label(
            self.root,
            text="🧮 Factor Finder App",
            font=("Segoe UI", 20, "bold"),
            bg="#0f172a",
            fg="white"
        )
        title.pack(pady=10)

        frame = tk.Frame(self.root, bg="#1e293b", padx=20, pady=20)
        frame.pack(pady=10)

        # Input
        tk.Label(frame, text="Enter Number:", bg="#1e293b", fg="white").grid(row=0, column=0, sticky="w")
        self.num_entry = ttk.Entry(frame, width=25)
        self.num_entry.grid(row=0, column=1, pady=5)

        # Buttons
        ttk.Button(frame, text="Find Factors", command=self.find_factors).grid(row=1, column=0, pady=10)
        ttk.Button(frame, text="Clear", command=self.clear).grid(row=1, column=1)
        ttk.Button(frame, text="Copy", command=self.copy_output).grid(row=1, column=2)

        # Output
        self.output = tk.Text(
            self.root,
            height=10,
            width=80,
            bg="#020617",
            fg="cyan",
            font=("Consolas", 11)
        )
        self.output.pack(pady=10)

        # History
        tk.Label(self.root, text="History", bg="#0f172a", fg="white").pack()
        self.history_box = tk.Text(
            self.root,
            height=6,
            width=80,
            bg="#020617",
            fg="lightgreen",
            font=("Consolas", 10)
        )
        self.history_box.pack(pady=5)

    def find_factors(self):
        self.output.delete("1.0", tk.END)

        try:
            n = int(self.num_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")
            return

        if n == 0:
            messagebox.showwarning("Warning", "0 has infinite factors")
            return

        num = abs(n)
        factors = set()

        for i in range(1, int(math.sqrt(num)) + 1):
            if num % i == 0:
                factors.add(i)
                factors.add(num // i)

        factors = sorted(factors)

        # Display factors
        self.output.insert(tk.END, f"Factors of {n}:\n")
        self.output.insert(tk.END, "-" * 40 + "\n")
        self.output.insert(tk.END, ", ".join(map(str, factors)) + "\n\n")

        # Prime factorization
        self.output.insert(tk.END, "Prime Factorization:\n")
        self.output.insert(tk.END, "-" * 40 + "\n")
        self.output.insert(tk.END, self.prime_factorization(num))

        record = f"{n} → Factors: {factors}"
        self.history.append(record)
        self.history_box.insert(tk.END, record + "\n")

    def prime_factorization(self, n):
        factors = []
        temp = n

        for i in range(2, int(math.sqrt(n)) + 1):
            while temp % i == 0:
                factors.append(i)
                temp //= i

        if temp > 1:
            factors.append(temp)

        return " × ".join(map(str, factors)) if factors else "None"

    def clear(self):
        self.num_entry.delete(0, tk.END)
        self.output.delete("1.0", tk.END)

    def copy_output(self):
        text = self.output.get("1.0", tk.END)
        if text.strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("Copied", "Output copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "Nothing to copy")


if __name__ == "__main__":
    root = tk.Tk()
    app = FactorFinderApp(root)
    root.mainloop()
