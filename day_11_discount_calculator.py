import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ------------------ Core Logic ------------------

def apply_discount(price, percent):
    discount = price * (percent / 100)
    final_price = price - discount
    return round(discount, 2), round(final_price, 2)

# ------------------ Main App ------------------

class DiscountCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Discount Calculator App")
        self.root.geometry("780x560")
        self.history = []

        self.create_ui()

    # ------------------ UI ------------------

    def create_ui(self):
        # ===== Header (Canva-Style Blue → Purple) =====
        header = tk.Frame(self.root, height=70, bg="#3b82f6")
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="Discount Calculator",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#3b82f6"
        )
        title.pack(side="left", padx=20, pady=15)

        subtitle = tk.Label(
            header,
            text="Simple • Fast • Shopping Friendly",
            font=("Arial", 10),
            fg="#e0e7ff",
            bg="#3b82f6"
        )
        subtitle.pack(side="left", padx=10)

        # ===== Main Body =====
        main = tk.Frame(self.root, bg="#0f172a")
        main.pack(fill="both", expand=True)

        card = tk.Frame(main, bg="#020617", padx=20, pady=20)
        card.pack(pady=30)

        # Original Price
        tk.Label(card, text="Original Price (₹):", fg="white", bg="#020617").grid(row=0, column=0, sticky="w", pady=5)
        self.price_entry = tk.Entry(card, width=25, bg="#020617", fg="white", insertbackground="white")
        self.price_entry.grid(row=0, column=1, pady=5)

        # Discount Percentage
        tk.Label(card, text="Discount (%):", fg="white", bg="#020617").grid(row=1, column=0, sticky="w", pady=5)
        self.discount_entry = tk.Entry(card, width=25, bg="#020617", fg="white", insertbackground="white")
        self.discount_entry.grid(row=1, column=1, pady=5)

        # Multiple Discounts
        self.multi_var = tk.BooleanVar()
        multi_check = tk.Checkbutton(
            card, text="Apply Multiple Discounts",
            variable=self.multi_var,
            fg="white", bg="#020617",
            activebackground="#020617", activeforeground="white",
            selectcolor="#020617",
            command=self.auto_calculate
        )
        multi_check.grid(row=2, column=0, columnspan=2, pady=5)

        # Results
        self.discount_label = tk.Label(card, text="Discount Amount: ", fg="white", bg="#020617")
        self.discount_label.grid(row=3, column=0, columnspan=2, pady=5)

        self.final_label = tk.Label(card, text="Final Price: ", fg="white", bg="#020617", font=("Arial", 11, "bold"))
        self.final_label.grid(row=4, column=0, columnspan=2, pady=5)

        # Buttons
        btn_frame = tk.Frame(card, bg="#020617")
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Calculate", width=14, bg="#2563eb", fg="white", command=self.calculate).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Clear", width=14, bg="#2563eb", fg="white", command=self.clear).pack(side="left", padx=5)

        # Graph Area
        graph_frame = tk.Frame(main, bg="#0f172a")
        graph_frame.pack(pady=10)

        tk.Label(graph_frame, text="Price Comparison (Before vs After)", fg="white", bg="#0f172a", font=("Arial", 11, "bold")).pack()
        self.canvas = tk.Canvas(graph_frame, width=400, height=200, bg="#020617", highlightthickness=0)
        self.canvas.pack()

        # History
        history_frame = tk.Frame(main, bg="#0f172a")
        history_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(history_frame, text="Recent Calculations", fg="white", bg="#0f172a", font=("Arial", 11, "bold")).pack(anchor="w")
        self.history_box = tk.Listbox(history_frame, height=6, bg="#020617", fg="white")
        self.history_box.pack(fill="x")

        # Real-time calculation
        self.price_entry.bind("<KeyRelease>", self.auto_calculate)
        self.discount_entry.bind("<KeyRelease>", self.auto_calculate)

    # ------------------ Calculation ------------------

    def calculate(self, save=True):
        try:
            price = float(self.price_entry.get())
            percent = float(self.discount_entry.get())

            if price <= 0 or percent < 0 or percent > 100:
                raise ValueError

            if self.multi_var.get():
                # Apply discount twice (example of multiple discount)
                d1, temp_price = apply_discount(price, percent)
                d2, final_price = apply_discount(temp_price, percent)
                discount = round(d1 + d2, 2)
            else:
                discount, final_price = apply_discount(price, percent)

            self.discount_label.config(text=f"Discount Amount: ₹{discount}")
            self.final_label.config(text=f"Final Price: ₹{final_price}")

            self.draw_graph(price, final_price)

            if save:
                self.save_history(price, percent, final_price)

        except:
            messagebox.showerror("Error", "Please enter valid price and discount percentage (0–100).")

    def auto_calculate(self, event=None):
        try:
            if not self.price_entry.get() or not self.discount_entry.get():
                return

            price = float(self.price_entry.get())
            percent = float(self.discount_entry.get())

            if price <= 0 or percent < 0 or percent > 100:
                return

            if self.multi_var.get():
                d1, temp_price = apply_discount(price, percent)
                d2, final_price = apply_discount(temp_price, percent)
                discount = round(d1 + d2, 2)
            else:
                discount, final_price = apply_discount(price, percent)

            self.discount_label.config(text=f"Discount Amount: ₹{discount}")
            self.final_label.config(text=f"Final Price: ₹{final_price}")

            self.draw_graph(price, final_price)

        except:
            pass

    # ------------------ Graph ------------------

    def draw_graph(self, original, final):
        self.canvas.delete("all")

        max_value = max(original, final)
        if max_value == 0:
            return

        original_width = int((original / max_value) * 360)
        final_width = int((final / max_value) * 360)

        # Original Bar
        self.canvas.create_rectangle(20, 60, 20 + original_width, 100, fill="#2563eb")
        self.canvas.create_text(20 + original_width / 2, 115, text="Original", fill="white")

        # Final Bar
        self.canvas.create_rectangle(20, 120, 20 + final_width, 160, fill="#1e40af")
        self.canvas.create_text(20 + final_width / 2, 175, text="Final", fill="white")

    # ------------------ History ------------------

    def save_history(self, price, percent, final_price):
        entry = f"{datetime.now().strftime('%H:%M:%S')} | ₹{price} | {percent}% | Final: ₹{final_price}"
        if not self.history or self.history[0] != entry:
            self.history.insert(0, entry)
            if len(self.history) > 10:
                self.history.pop()

            self.history_box.delete(0, tk.END)
            for item in self.history:
                self.history_box.insert(tk.END, item)

    # ------------------ Clear ------------------

    def clear(self):
        self.price_entry.delete(0, tk.END)
        self.discount_entry.delete(0, tk.END)
        self.multi_var.set(False)
        self.discount_label.config(text="Discount Amount: ")
        self.final_label.config(text="Final Price: ")
        self.canvas.delete("all")


# ------------------ Run App ------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = DiscountCalculator(root)
    root.mainloop()
