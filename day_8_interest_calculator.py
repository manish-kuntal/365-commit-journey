import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ------------------ Calculation Functions ------------------

def simple_interest(P, R, T):
    SI = (P * R * T) / 100
    A = P + SI
    return round(SI, 2), round(A, 2)

def compound_interest(P, R, T):
    A = P * (1 + (R / 100)) ** T
    CI = A - P
    return round(CI, 2), round(A, 2)

# ------------------ Main App ------------------

class InterestCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Interest Calculator")
        self.root.geometry("760x520")
        self.history = []

        self.create_ui()
        self.apply_theme()

    # ------------------ UI ------------------

    def create_ui(self):
        header = tk.Frame(self.root)
        header.pack(fill="x", pady=10)

        self.title_label = tk.Label(header, text="Interest Calculator App", font=("Arial", 18, "bold"))
        self.title_label.pack(side="left", padx=10)

        main = tk.Frame(self.root)
        main.pack(pady=10)

        # Principal
        tk.Label(main, text="Principal (₹):").grid(row=0, column=0, sticky="w", pady=5)
        self.principal_entry = tk.Entry(main, width=25)
        self.principal_entry.grid(row=0, column=1, pady=5)

        # Rate
        tk.Label(main, text="Rate (% per year):").grid(row=1, column=0, sticky="w", pady=5)
        self.rate_entry = tk.Entry(main, width=25)
        self.rate_entry.grid(row=1, column=1, pady=5)

        # Time
        tk.Label(main, text="Time:").grid(row=2, column=0, sticky="w", pady=5)
        time_frame = tk.Frame(main)
        time_frame.grid(row=2, column=1, pady=5, sticky="w")

        self.time_entry = tk.Entry(time_frame, width=12)
        self.time_entry.pack(side="left")

        self.time_unit = tk.StringVar(value="Years")
        ttk.Combobox(
            time_frame,
            textvariable=self.time_unit,
            values=["Years", "Months"],
            state="readonly",
            width=10
        ).pack(side="left", padx=5)

        # Results
        self.si_label = tk.Label(main, text="Simple Interest: ")
        self.si_label.grid(row=3, column=0, columnspan=2, pady=5)

        self.ci_label = tk.Label(main, text="Compound Interest: ")
        self.ci_label.grid(row=4, column=0, columnspan=2, pady=5)

        self.amount_label = tk.Label(main, text="Final Amount Comparison: ", font=("Arial", 12, "bold"))
        self.amount_label.grid(row=5, column=0, columnspan=2, pady=10)

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.calc_btn = tk.Button(btn_frame, text="Calculate", width=18, command=self.calculate)
        self.calc_btn.pack(side="left", padx=5)

        self.clear_btn = tk.Button(btn_frame, text="Clear", width=18, command=self.clear)
        self.clear_btn.pack(side="left", padx=5)

        # History
        history_frame = tk.Frame(self.root)
        history_frame.pack(pady=10, fill="x")

        tk.Label(history_frame, text="Last Calculations:").pack(anchor="w", padx=10)
        self.history_box = tk.Listbox(history_frame, height=7)
        self.history_box.pack(fill="x", padx=10)

        # Real-time calculation (NO ERROR POPUP)
        self.principal_entry.bind("<KeyRelease>", self.auto_calc)
        self.rate_entry.bind("<KeyRelease>", self.auto_calc)
        self.time_entry.bind("<KeyRelease>", self.auto_calc)

    # ------------------ Helper Functions ------------------

    def get_time_in_years(self):
        t = float(self.time_entry.get())
        if self.time_unit.get() == "Years":
            return t
        else:
            return t / 12

    # ------------------ Calculate ------------------

    def calculate(self, save=True):
        try:
            P = float(self.principal_entry.get())
            R = float(self.rate_entry.get())
            T = self.get_time_in_years()

            if P <= 0 or R <= 0 or T <= 0:
                raise ValueError

            si, A_si = simple_interest(P, R, T)
            ci, A_ci = compound_interest(P, R, T)

            self.si_label.config(text=f"Simple Interest: ₹{si} | Final: ₹{A_si}")
            self.ci_label.config(text=f"Compound Interest: ₹{ci} | Final: ₹{A_ci}")
            self.amount_label.config(text=f"Comparison → SI: ₹{A_si} | CI: ₹{A_ci}")

            if save:
                self.save_history(P, R, T, A_si, A_ci)

        except:
            messagebox.showerror("Error", "Please enter valid positive numbers.")

    # ------------------ Auto Calculate (NO POPUP) ------------------

    def auto_calc(self, event=None):
        try:
            if not self.principal_entry.get() or not self.rate_entry.get() or not self.time_entry.get():
                return

            P = float(self.principal_entry.get())
            R = float(self.rate_entry.get())
            T = self.get_time_in_years()

            if P <= 0 or R <= 0 or T <= 0:
                return

            si, A_si = simple_interest(P, R, T)
            ci, A_ci = compound_interest(P, R, T)

            self.si_label.config(text=f"Simple Interest: ₹{si} | Final: ₹{A_si}")
            self.ci_label.config(text=f"Compound Interest: ₹{ci} | Final: ₹{A_ci}")
            self.amount_label.config(text=f"Comparison → SI: ₹{A_si} | CI: ₹{A_ci}")

        except:
            pass

    # ------------------ History ------------------

    def save_history(self, P, R, T, A_si, A_ci):
        entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | P:{P} R:{R}% T:{round(T,2)}y | SI:{A_si} CI:{A_ci}"
        self.history.insert(0, entry)

        if len(self.history) > 10:
            self.history.pop()

        self.history_box.delete(0, tk.END)
        for item in self.history:
            self.history_box.insert(tk.END, item)

    # ------------------ Clear ------------------

    def clear(self):
        self.principal_entry.delete(0, tk.END)
        self.rate_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.si_label.config(text="Simple Interest: ")
        self.ci_label.config(text="Compound Interest: ")
        self.amount_label.config(text="Final Amount Comparison: ")

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
    app = InterestCalculator(root)
    root.mainloop()


