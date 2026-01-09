import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ------------------ OFFLINE EXCHANGE RATES (Base: USD) ------------------
# You can later replace this with live API
RATES = {
    "USD": 1.0,
    "INR": 83.20,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 147.50,
    "AED": 3.67,
    "AUD": 1.52,
    "CAD": 1.36
}

FAVORITES = [("INR", "USD"), ("USD", "EUR")]

# ------------------ CONVERSION LOGIC ------------------
def convert_currency(amount, from_curr, to_curr):
    try:
        amount = float(amount)
    except:
        raise ValueError("Invalid Amount")

    if from_curr not in RATES or to_curr not in RATES:
        raise ValueError("Invalid Currency")

    usd_value = amount / RATES[from_curr]
    converted = usd_value * RATES[to_curr]
    return round(converted, 4)

# ------------------ MAIN APP ------------------
class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter App")
        self.root.geometry("900x550")
        self.root.configure(bg="#0a0f1f")
        self.history = []

        self.create_ui()

    # ------------------ UI ------------------
    def create_ui(self):
        # ===== Header =====
        header = tk.Frame(self.root, bg="#0a0f1f", height=60)
        header.pack(fill="x")

        title = tk.Label(
            header, text="Currency Converter",
            font=("Segoe UI", 20, "bold"),
            fg="white", bg="#0a0f1f"
        )
        title.pack(side="left", padx=20, pady=10)

        # ===== Main Container =====
        main = tk.Frame(self.root, bg="#0a0f1f")
        main.pack(fill="both", expand=True)

        # ===== Center Card =====
        card = tk.Frame(main, bg="#f3f4f6", bd=0, relief="flat")
        card.place(relx=0.5, rely=0.35, anchor="center", width=380, height=300)

        # Amount
        tk.Label(card, text="Amount:", font=("Segoe UI", 11, "bold"),
                 bg="#f3f4f6").place(x=30, y=30)
        self.amount_entry = tk.Entry(card, font=("Segoe UI", 11), width=25)
        self.amount_entry.place(x=130, y=30)
        self.amount_entry.insert(0, "10000")

        # From Currency
        tk.Label(card, text="From Currency:", font=("Segoe UI", 11, "bold"),
                 bg="#f3f4f6").place(x=30, y=70)
        self.from_currency = ttk.Combobox(card, values=list(RATES.keys()), width=22)
        self.from_currency.place(x=130, y=70)
        self.from_currency.set("EUR")

        # To Currency
        tk.Label(card, text="To Currency:", font=("Segoe UI", 11, "bold"),
                 bg="#f3f4f6").place(x=30, y=110)
        self.to_currency = ttk.Combobox(card, values=list(RATES.keys()), width=22)
        self.to_currency.place(x=130, y=110)
        self.to_currency.set("INR")

        # Result
        self.result_label = tk.Label(
            card, text="Result: 0.0",
            font=("Segoe UI", 12, "bold"),
            bg="#111827", fg="white", width=28, pady=8
        )
        self.result_label.place(x=30, y=160)

        # Convert Button
        convert_btn = tk.Button(
            card, text="Convert",
            bg="#2563eb", fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat", width=20, command=self.convert
        )
        convert_btn.place(x=95, y=210)

        # ===== Favorites =====
        fav_frame = tk.Frame(main, bg="#0a0f1f")
        fav_frame.place(relx=0.5, rely=0.62, anchor="center")

        tk.Label(
            fav_frame, text="★ Favorites:",
            font=("Segoe UI", 11, "bold"),
            fg="white", bg="#0a0f1f"
        ).pack(side="left", padx=5)

        for f, t in FAVORITES:
            btn = tk.Button(
                fav_frame, text=f"{f} → {t}",
                bg="#1f2937", fg="white",
                relief="flat", padx=10, command=lambda a=f, b=t: self.set_favorite(a, b)
            )
            btn.pack(side="left", padx=5)

        # ===== History Panel =====
        history_frame = tk.Frame(self.root, bg="#020617", height=120)
        history_frame.pack(side="bottom", fill="x")

        tk.Label(
            history_frame, text="Last Conversions:",
            font=("Segoe UI", 11, "bold"),
            fg="white", bg="#020617"
        ).pack(anchor="w", padx=10, pady=5)

        self.history_box = tk.Listbox(
            history_frame, bg="#020617", fg="white",
            font=("Consolas", 10), height=5, bd=0
        )
        self.history_box.pack(fill="both", padx=10, pady=5)

    # ------------------ ACTIONS ------------------
    def convert(self):
        amount = self.amount_entry.get()
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()

        try:
            result = convert_currency(amount, from_curr, to_curr)
            self.result_label.config(text=f"Result: {result}")

            timestamp = datetime.now().strftime("%H:%M:%S")
            record = f"{timestamp} | {amount} {from_curr} → {result} {to_curr}"
            self.history.insert(0, record)

            self.history_box.delete(0, tk.END)
            for item in self.history[:5]:
                self.history_box.insert(tk.END, item)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def set_favorite(self, f, t):
        self.from_currency.set(f)
        self.to_currency.set(t)

# ------------------ RUN APP ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
