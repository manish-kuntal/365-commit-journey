import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ------------------ Core EMI Logic ------------------

def calculate_emi(P, R, N):
    r = R / (12 * 100)
    emi = P * r * ((1 + r) ** N) / (((1 + r) ** N) - 1)
    total_payable = emi * N
    total_interest = total_payable - P
    return round(emi, 2), round(total_interest, 2), round(total_payable, 2)

# ------------------ Main App ------------------

class EMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Loan EMI Calculator")
        self.root.geometry("820x580")
        self.history = []

        self.create_ui()
        self.apply_theme()

    # ------------------ UI ------------------

    def create_ui(self):
        header = tk.Frame(self.root)
        header.pack(fill="x", pady=10)

        self.title_label = tk.Label(header, text="Loan EMI Calculator", font=("Arial", 18, "bold"))
        self.title_label.pack(side="left", padx=10)

        main = tk.Frame(self.root)
        main.pack(pady=10)

        # Loan Amount
        tk.Label(main, text="Loan Amount (₹):").grid(row=0, column=0, sticky="w", pady=5)
        self.amount_entry = tk.Entry(main, width=25)
        self.amount_entry.grid(row=0, column=1, pady=5)

        # Interest Rate
        tk.Label(main, text="Interest Rate (% p.a.):").grid(row=1, column=0, sticky="w", pady=5)
        self.rate_entry = tk.Entry(main, width=25)
        self.rate_entry.grid(row=1, column=1, pady=5)

        # Tenure
        tk.Label(main, text="Tenure:").grid(row=2, column=0, sticky="w", pady=5)
        tenure_frame = tk.Frame(main)
        tenure_frame.grid(row=2, column=1, pady=5, sticky="w")

        self.tenure_entry = tk.Entry(tenure_frame, width=12)
        self.tenure_entry.pack(side="left")

        self.tenure_unit = tk.StringVar(value="Years")
        ttk.Combobox(
            tenure_frame, textvariable=self.tenure_unit,
            values=["Years", "Months"], state="readonly", width=10
        ).pack(side="left", padx=5)

        # Presets
        preset_frame = tk.Frame(main)
        preset_frame.grid(row=3, column=0, columnspan=2, pady=8)

        tk.Label(preset_frame, text="Presets:").pack(side="left", padx=5)
        tk.Button(preset_frame, text="Home Loan", command=lambda: self.fill_preset(3000000, 8.5, 20)).pack(side="left", padx=5)
        tk.Button(preset_frame, text="Car Loan", command=lambda: self.fill_preset(800000, 9.0, 5)).pack(side="left", padx=5)
        tk.Button(preset_frame, text="Education Loan", command=lambda: self.fill_preset(1000000, 7.5, 10)).pack(side="left", padx=5)
        tk.Button(preset_frame, text="Personal Loan", command=lambda: self.fill_preset(500000, 12.0, 3)).pack(side="left", padx=5)

        # Results
        self.emi_label = tk.Label(main, text="Monthly EMI: ")
        self.emi_label.grid(row=4, column=0, columnspan=2, pady=5)

        self.interest_label = tk.Label(main, text="Total Interest: ")
        self.interest_label.grid(row=5, column=0, columnspan=2, pady=5)

        self.total_label = tk.Label(main, text="Total Payable: ", font=("Arial", 12, "bold"))
        self.total_label.grid(row=6, column=0, columnspan=2, pady=8)

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Calculate", width=18, command=self.calculate).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Clear", width=18, command=self.clear).pack(side="left", padx=5)

        # Graph Canvas
        graph_frame = tk.Frame(self.root)
        graph_frame.pack(pady=10)

        tk.Label(graph_frame, text="Principal vs Interest Breakdown").pack()
        self.canvas = tk.Canvas(graph_frame, width=400, height=200)
        self.canvas.pack()

        # History
        history_frame = tk.Frame(self.root)
        history_frame.pack(pady=10, fill="x")

        tk.Label(history_frame, text="Previous Calculations:").pack(anchor="w", padx=10)
        self.history_box = tk.Listbox(history_frame, height=7)
        self.history_box.pack(fill="x", padx=10)

        # Real-time calculation (NO POPUP)
        self.amount_entry.bind("<KeyRelease>", self.auto_calc)
        self.rate_entry.bind("<KeyRelease>", self.auto_calc)
        self.tenure_entry.bind("<KeyRelease>", self.auto_calc)

    # ------------------ Helpers ------------------

    def get_tenure_in_months(self):
        t = float(self.tenure_entry.get())
        return int(t * 12) if self.tenure_unit.get() == "Years" else int(t)

    def fill_preset(self, amount, rate, years):
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, str(amount))
        self.rate_entry.delete(0, tk.END)
        self.rate_entry.insert(0, str(rate))
        self.tenure_entry.delete(0, tk.END)
        self.tenure_entry.insert(0, str(years))
        self.tenure_unit.set("Years")
        self.calculate()

    # ------------------ Calculation ------------------

    def calculate(self, save=True):
        try:
            P = float(self.amount_entry.get())
            R = float(self.rate_entry.get())
            N = self.get_tenure_in_months()

            if P <= 0 or R <= 0 or N <= 0:
                raise ValueError

            emi, total_interest, total_payable = calculate_emi(P, R, N)

            self.emi_label.config(text=f"Monthly EMI: ₹{emi}")
            self.interest_label.config(text=f"Total Interest: ₹{total_interest}")
            self.total_label.config(text=f"Total Payable: ₹{total_payable}")

            self.draw_graph(P, total_interest)

            if save:
                self.save_history(P, R, N, emi)

        except:
            messagebox.showerror("Error", "Please enter valid positive numbers.")

    def auto_calc(self, event=None):
        try:
            if not self.amount_entry.get() or not self.rate_entry.get() or not self.tenure_entry.get():
                return

            P = float(self.amount_entry.get())
            R = float(self.rate_entry.get())
            N = self.get_tenure_in_months()

            if P <= 0 or R <= 0 or N <= 0:
                return

            emi, total_interest, total_payable = calculate_emi(P, R, N)

            self.emi_label.config(text=f"Monthly EMI: ₹{emi}")
            self.interest_label.config(text=f"Total Interest: ₹{total_interest}")
            self.total_label.config(text=f"Total Payable: ₹{total_payable}")

            self.draw_graph(P, total_interest)

        except:
            pass

    # ------------------ Graph ------------------

    def draw_graph(self, principal, interest):
        self.canvas.delete("all")
        total = principal + interest

        p_width = int((principal / total) * 380)
        i_width = int((interest / total) * 380)

        self.canvas.create_rectangle(10, 50, 10 + p_width, 120, fill="#2563eb")
        self.canvas.create_rectangle(10 + p_width, 50, 10 + p_width + i_width, 120, fill="#1e40af")

        self.canvas.create_text(10 + p_width / 2, 135, text="Principal", fill="white")
        self.canvas.create_text(10 + p_width + i_width / 2, 135, text="Interest", fill="white")

    # ------------------ History ------------------

    def save_history(self, P, R, N, emi):
        entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | P:{P} R:{R}% T:{N}m | EMI:{emi}"
        self.history.insert(0, entry)
        if len(self.history) > 10:
            self.history.pop()

        self.history_box.delete(0, tk.END)
        for item in self.history:
            self.history_box.insert(tk.END, item)

    # ------------------ Clear ------------------

    def clear(self):
        self.amount_entry.delete(0, tk.END)
        self.rate_entry.delete(0, tk.END)
        self.tenure_entry.delete(0, tk.END)
        self.emi_label.config(text="Monthly EMI: ")
        self.interest_label.config(text="Total Interest: ")
        self.total_label.config(text="Total Payable: ")
        self.canvas.delete("all")

    # ------------------ Black + Blue Theme ------------------

    def apply_theme(self):
        bg = "#020617"
        fg = "#e5e7eb"
        accent = "#2563eb"

        self.root.configure(bg=bg)
        for widget in self.root.winfo_children():
            self.apply_widget_theme(widget, bg, fg, accent)

    def apply_widget_theme(self, widget, bg, fg, accent):
        try:
            if isinstance(widget, tk.Button):
                widget.configure(bg=accent, fg="white",
                                 activebackground="#1d4ed8",
                                 activeforeground="white",
                                 borderwidth=0)
            elif isinstance(widget, tk.Entry):
                widget.configure(bg="#020617", fg=fg, insertbackground=fg)
            elif isinstance(widget, tk.Listbox):
                widget.configure(bg="#020617", fg=fg)
            else:
                widget.configure(bg=bg, fg=fg)
        except:
            pass

        for child in widget.winfo_children():
            self.apply_widget_theme(child, bg, fg, accent)


# ------------------ Run App ------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = EMICalculator(root)
    root.mainloop()

