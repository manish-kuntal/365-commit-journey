import tkinter as tk
from tkinter import ttk
from datetime import datetime
import math

# ------------------ Core Logic ------------------

def calculate_tip(bill, percent):
    tip = bill * (percent / 100)
    total = bill + tip
    return round(tip, 2), round(total, 2)

# ------------------ Main App ------------------

class TipCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Tip Calculator App")
        self.root.geometry("760x520")
        self.history = []

        self.create_ui()

    # ------------------ UI ------------------

    def create_ui(self):
        # ===== Header (Canva-style Blue → Purple) =====
        header = tk.Frame(self.root, height=70, bg="#3b82f6")
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="Tip Calculator",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#3b82f6"
        )
        title.pack(side="left", padx=20, pady=15)

        subtitle = tk.Label(
            header,
            text="Fast • Simple • Travel Friendly",
            font=("Arial", 10),
            fg="#e0e7ff",
            bg="#3b82f6"
        )
        subtitle.pack(side="left", padx=10)

        # ===== Main Content =====
        main = tk.Frame(self.root, bg="#0f172a")
        main.pack(fill="both", expand=True)

        card = tk.Frame(main, bg="#020617", padx=20, pady=20)
        card.pack(pady=30)

        # Bill Amount
        tk.Label(card, text="Bill Amount (₹):", fg="white", bg="#020617").grid(row=0, column=0, sticky="w", pady=5)
        self.bill_entry = tk.Entry(card, width=25, bg="#020617", fg="white", insertbackground="white")
        self.bill_entry.grid(row=0, column=1, pady=5)

        # Tip Percentage Slider
        tk.Label(card, text="Tip Percentage (%):", fg="white", bg="#020617").grid(row=1, column=0, sticky="w", pady=5)
        self.tip_var = tk.IntVar(value=10)
        self.tip_slider = tk.Scale(
            card, from_=0, to=50, orient="horizontal",
            variable=self.tip_var, bg="#020617", fg="white",
            highlightthickness=0, troughcolor="#1e293b",
            command=self.auto_calculate
        )
        self.tip_slider.grid(row=1, column=1, pady=5, sticky="we")

        # Preset Buttons
        preset_frame = tk.Frame(card, bg="#020617")
        preset_frame.grid(row=2, column=0, columnspan=2, pady=5)

        tk.Label(preset_frame, text="Presets:", fg="white", bg="#020617").pack(side="left", padx=5)
        tk.Button(preset_frame, text="10%", command=lambda: self.set_tip(10)).pack(side="left", padx=5)
        tk.Button(preset_frame, text="15%", command=lambda: self.set_tip(15)).pack(side="left", padx=5)
        tk.Button(preset_frame, text="20%", command=lambda: self.set_tip(20)).pack(side="left", padx=5)

        # Split
        tk.Label(card, text="Split Between (People):", fg="white", bg="#020617").grid(row=3, column=0, sticky="w", pady=5)
        self.split_entry = tk.Entry(card, width=25, bg="#020617", fg="white", insertbackground="white")
        self.split_entry.grid(row=3, column=1, pady=5)
        self.split_entry.insert(0, "1")

        # Rounding Option
        self.round_var = tk.BooleanVar()
        round_check = tk.Checkbutton(
            card, text="Round to nearest rupee",
            variable=self.round_var,
            fg="white", bg="#020617",
            activebackground="#020617", activeforeground="white",
            selectcolor="#020617",
            command=self.auto_calculate
        )
        round_check.grid(row=4, column=0, columnspan=2, pady=5)

        # Results
        self.tip_label = tk.Label(card, text="Tip Amount: ", fg="white", bg="#020617")
        self.tip_label.grid(row=5, column=0, columnspan=2, pady=5)

        self.total_label = tk.Label(card, text="Total Payable: ", fg="white", bg="#020617", font=("Arial", 11, "bold"))
        self.total_label.grid(row=6, column=0, columnspan=2, pady=5)

        self.split_label = tk.Label(card, text="Per Person: ", fg="white", bg="#020617")
        self.split_label.grid(row=7, column=0, columnspan=2, pady=5)

        # Buttons
        btn_frame = tk.Frame(card, bg="#020617")
        btn_frame.grid(row=8, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Clear", width=14, bg="#2563eb", fg="white", command=self.clear).pack(side="left", padx=5)

        # History
        history_frame = tk.Frame(main, bg="#0f172a")
        history_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(history_frame, text="Recent Bills", fg="white", bg="#0f172a", font=("Arial", 11, "bold")).pack(anchor="w")
        self.history_box = tk.Listbox(history_frame, height=6, bg="#020617", fg="white")
        self.history_box.pack(fill="x")

        # Real-time calculation (NO POPUPS)
        self.bill_entry.bind("<KeyRelease>", self.auto_calculate)
        self.split_entry.bind("<KeyRelease>", self.auto_calculate)

    # ------------------ Helpers ------------------

    def set_tip(self, value):
        self.tip_var.set(value)
        self.auto_calculate()

    def auto_calculate(self, event=None):
        try:
            if not self.bill_entry.get():
                return

            bill = float(self.bill_entry.get())
            percent = self.tip_var.get()

            if bill <= 0:
                return

            tip, total = calculate_tip(bill, percent)

            # Rounding
            if self.round_var.get():
                total = round(total)
                tip = round(tip)

            # Split
            try:
                people = int(self.split_entry.get())
                if people <= 0:
                    people = 1
            except:
                people = 1

            per_person = round(total / people, 2)

            self.tip_label.config(text=f"Tip Amount: ₹{tip}")
            self.total_label.config(text=f"Total Payable: ₹{total}")
            self.split_label.config(text=f"Per Person: ₹{per_person}")

            self.save_history(bill, percent, total, people)

        except:
            pass

    # ------------------ History ------------------

    def save_history(self, bill, percent, total, people):
        entry = f"{datetime.now().strftime('%H:%M:%S')} | ₹{bill} | {percent}% | Total: ₹{total} | Split: {people}"
        if not self.history or self.history[0] != entry:
            self.history.insert(0, entry)
            if len(self.history) > 10:
                self.history.pop()

            self.history_box.delete(0, tk.END)
            for item in self.history:
                self.history_box.insert(tk.END, item)

    # ------------------ Clear ------------------

    def clear(self):
        self.bill_entry.delete(0, tk.END)
        self.split_entry.delete(0, tk.END)
        self.split_entry.insert(0, "1")
        self.tip_var.set(10)
        self.round_var.set(False)
        self.tip_label.config(text="Tip Amount: ")
        self.total_label.config(text="Total Payable: ")
        self.split_label.config(text="Per Person: ")


# ------------------ Run App ------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = TipCalculator(root)
    root.mainloop()
