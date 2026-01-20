import tkinter as tk
from tkinter import ttk, messagebox

class SquareCubeFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("Square & Cube Finder")
        self.root.geometry("600x420")
        self.root.configure(bg="#0f172a")

        self.history = []
        self.create_ui()

    def create_ui(self):
        title = tk.Label(
            self.root,
            text="🔢 Square & Cube Finder",
            font=("Segoe UI", 20, "bold"),
            bg="#0f172a",
            fg="white"
        )
        title.pack(pady=10)

        frame = tk.Frame(self.root, bg="#1e293b", padx=20, pady=20)
        frame.pack(pady=10)

        tk.Label(frame, text="Enter Number:", bg="#1e293b", fg="white").grid(row=0, column=0, sticky="w")
        self.num_entry = ttk.Entry(frame, width=25)
        self.num_entry.grid(row=0, column=1, pady=5)

        ttk.Button(frame, text="Calculate", command=self.calculate).grid(row=1, column=0, pady=10)
        ttk.Button(frame, text="Clear", command=self.clear).grid(row=1, column=1)

        self.result_label = tk.Label(
            frame,
            text="Result will appear here",
            bg="#1e293b",
            fg="cyan",
            font=("Segoe UI", 12)
        )
        self.result_label.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(frame, text="Copy Result", command=self.copy_result).grid(row=3, column=0, columnspan=2)

        # History box
        tk.Label(self.root, text="History", bg="#0f172a", fg="white").pack()
        self.history_box = tk.Text(
            self.root,
            height=6,
            width=70,
            bg="#020617",
            fg="lightgreen",
            font=("Consolas", 10)
        )
        self.history_box.pack(pady=5)

    def calculate(self):
        try:
            n = int(self.num_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")
            return

        square = n ** 2
        cube = n ** 3

        result_text = f"Number: {n} | Square: {square} | Cube: {cube}"
        self.result_label.config(text=result_text)

        self.history.append(result_text)
        self.history_box.insert(tk.END, result_text + "\n")

    def clear(self):
        self.num_entry.delete(0, tk.END)
        self.result_label.config(text="Result will appear here")

    def copy_result(self):
        text = self.result_label.cget("text")
        if "Square" in text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("Copied", "Result copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No result to copy")


if __name__ == "__main__":
    root = tk.Tk()
    app = SquareCubeFinder(root)
    root.mainloop()
