import tkinter as tk
from tkinter import ttk, messagebox

class TableGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Table Generator")
        self.root.geometry("650x450")
        self.root.configure(bg="#0f172a")

        self.create_ui()

    def create_ui(self):
        title = tk.Label(
            self.root,
            text="📐 Table Generator App",
            font=("Segoe UI", 20, "bold"),
            bg="#0f172a",
            fg="white"
        )
        title.pack(pady=10)

        frame = tk.Frame(self.root, bg="#1e293b", padx=20, pady=20)
        frame.pack(pady=10)

        # Number input
        tk.Label(frame, text="Enter Number(s):", bg="#1e293b", fg="white").grid(row=0, column=0, sticky="w")
        self.num_entry = ttk.Entry(frame, width=25)
        self.num_entry.grid(row=0, column=1, pady=5)
        tk.Label(frame, text="(Example: 2 or 2,5,10)", bg="#1e293b", fg="gray").grid(row=0, column=2)

        # Range
        tk.Label(frame, text="Range:", bg="#1e293b", fg="white").grid(row=1, column=0, sticky="w")
        self.range_var = tk.StringVar(value="10")
        ttk.Combobox(
            frame,
            textvariable=self.range_var,
            values=["10", "20", "Custom"],
            state="readonly",
            width=22
        ).grid(row=1, column=1)

        self.custom_range = ttk.Entry(frame, width=25)
        self.custom_range.grid(row=2, column=1, pady=5)
        self.custom_range.insert(0, "Enter custom range")

        # Buttons
        ttk.Button(frame, text="Generate Table", command=self.generate_table).grid(row=3, column=0, pady=10)
        ttk.Button(frame, text="Clear", command=self.clear_output).grid(row=3, column=1)
        ttk.Button(frame, text="Copy", command=self.copy_output).grid(row=3, column=2)

        # Output
        self.output = tk.Text(
            self.root,
            height=12,
            width=75,
            bg="#020617",
            fg="cyan",
            font=("Consolas", 11)
        )
        self.output.pack(pady=10)

    def generate_table(self):
        self.output.delete("1.0", tk.END)

        try:
            numbers = [int(n.strip()) for n in self.num_entry.get().split(",")]
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
            return

        range_value = self.range_var.get()
        if range_value == "Custom":
            try:
                end = int(self.custom_range.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid custom range")
                return
        else:
            end = int(range_value)

        for num in numbers:
            self.output.insert(tk.END, f"Table of {num}\n")
            self.output.insert(tk.END, "-" * 20 + "\n")
            for i in range(1, end + 1):
                self.output.insert(tk.END, f"{num} x {i} = {num * i}\n")
            self.output.insert(tk.END, "\n")

    def clear_output(self):
        self.output.delete("1.0", tk.END)

    def copy_output(self):
        data = self.output.get("1.0", tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(data)
        messagebox.showinfo("Copied", "Table copied to clipboard!")


if __name__ == "__main__":
    root = tk.Tk()
    app = TableGeneratorApp(root)
    root.mainloop()
