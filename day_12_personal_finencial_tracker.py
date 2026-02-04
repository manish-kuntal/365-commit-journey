import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import json
import os
import csv

DATA_FILE = "finance_data.json"

# -------------------- DATA HANDLING --------------------

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

transactions = load_data()

# -------------------- MAIN APP --------------------

class FinanceTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker - Manish")
        self.root.geometry("1150x700")
        self.root.configure(bg="#0f172a")

        self.budget_limit = tk.DoubleVar(value=0)

        self.create_ui()
        self.update_summary()
        self.load_table(transactions)

    # -------------------- UI --------------------

    def create_ui(self):
        # ===== HEADER =====
        header = tk.Frame(self.root, bg="#3b82f6", height=70)
        header.pack(fill="x")

        tk.Label(
            header, text="💰 Personal Finance Tracker",
            font=("Arial", 20, "bold"), fg="white", bg="#3b82f6"
        ).pack(side="left", padx=20, pady=15)

        tk.Label(
            header, text="Track • Analyze • Save Smarter",
            font=("Arial", 10), fg="#e0e7ff", bg="#3b82f6"
        ).pack(side="left")

        # ===== MAIN =====
        main = tk.Frame(self.root, bg="#0f172a")
        main.pack(fill="both", expand=True, padx=15, pady=15)

        # ===== LEFT PANEL =====
        left = tk.Frame(main, bg="#020617", padx=15, pady=15)
        left.pack(side="left", fill="y")

        tk.Label(left, text="➕ Add Transaction", font=("Arial", 14, "bold"),
                 fg="#38bdf8", bg="#020617").pack(pady=10)

        # Amount
        tk.Label(left, text="Amount (₹)", fg="white", bg="#020617").pack(anchor="w")
        self.amount_entry = tk.Entry(left, bg="#020617", fg="white", insertbackground="white")
        self.amount_entry.pack(fill="x", pady=5)

        # Type
        tk.Label(left, text="Type", fg="white", bg="#020617").pack(anchor="w")
        self.type_var = tk.StringVar(value="Expense")
        ttk.Combobox(left, textvariable=self.type_var,
                     values=["Income", "Expense"], state="readonly").pack(fill="x", pady=5)

        # Category
        tk.Label(left, text="Category", fg="white", bg="#020617").pack(anchor="w")
        self.category_var = tk.StringVar()
        ttk.Combobox(left, textvariable=self.category_var,
                     values=["Food", "Travel", "Shopping", "Bills", "Rent", "Salary", "Investment", "Other"],
                     state="readonly").pack(fill="x", pady=5)

        # Note
        tk.Label(left, text="Note", fg="white", bg="#020617").pack(anchor="w")
        self.note_entry = tk.Entry(left, bg="#020617", fg="white", insertbackground="white")
        self.note_entry.pack(fill="x", pady=5)

        # Budget
        tk.Label(left, text="Monthly Budget (₹)", fg="white", bg="#020617").pack(anchor="w")
        self.budget_entry = tk.Entry(left, textvariable=self.budget_limit,
                                     bg="#020617", fg="white", insertbackground="white")
        self.budget_entry.pack(fill="x", pady=5)

        # Buttons
        tk.Button(left, text="Add Transaction", bg="#2563eb", fg="white",
                  font=("Arial", 11, "bold"), command=self.add_transaction).pack(fill="x", pady=6)

        tk.Button(left, text="Clear", bg="#1e40af", fg="white",
                  font=("Arial", 11, "bold"), command=self.clear_fields).pack(fill="x")

        tk.Button(left, text="Export to CSV", bg="#16a34a", fg="white",
                  font=("Arial", 11, "bold"), command=self.export_csv).pack(fill="x", pady=6)

        # ===== RIGHT PANEL =====
        right = tk.Frame(main, bg="#0f172a")
        right.pack(side="left", fill="both", expand=True, padx=10)

        # ===== SUMMARY =====
        summary = tk.Frame(right, bg="#020617", pady=12)
        summary.pack(fill="x")

        self.income_label = tk.Label(summary, text="Income: ₹0.00", fg="#22c55e", bg="#020617",
                                      font=("Arial", 12, "bold"))
        self.income_label.pack(side="left", padx=20)

        self.expense_label = tk.Label(summary, text="Expense: ₹0.00", fg="#ef4444", bg="#020617",
                                       font=("Arial", 12, "bold"))
        self.expense_label.pack(side="left", padx=20)

        self.balance_label = tk.Label(summary, text="Balance: ₹0.00", fg="#38bdf8", bg="#020617",
                                       font=("Arial", 12, "bold"))
        self.balance_label.pack(side="left", padx=20)

        # ===== FILTER =====
        filter_frame = tk.Frame(right, bg="#020617", pady=10)
        filter_frame.pack(fill="x", pady=8)

        tk.Label(filter_frame, text="From (DD-MM-YYYY)", fg="white", bg="#020617").pack(side="left", padx=5)
        self.from_date = tk.Entry(filter_frame, width=12)
        self.from_date.pack(side="left", padx=5)

        tk.Label(filter_frame, text="To", fg="white", bg="#020617").pack(side="left", padx=5)
        self.to_date = tk.Entry(filter_frame, width=12)
        self.to_date.pack(side="left", padx=5)

        tk.Button(filter_frame, text="Apply Filter", bg="#2563eb", fg="white",
                  command=self.apply_filter).pack(side="left", padx=10)

        tk.Button(filter_frame, text="Reset", bg="#1e40af", fg="white",
                  command=lambda: self.load_table(transactions)).pack(side="left")

        # ===== TABLE =====
        table_frame = tk.Frame(right, bg="#0f172a")
        table_frame.pack(fill="both", expand=True, pady=10)

        columns = ("date", "type", "category", "amount", "note")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.table.heading(col, text=col.capitalize())

        self.table.column("date", width=150)
        self.table.column("type", width=80)
        self.table.column("category", width=120)
        self.table.column("amount", width=100)
        self.table.column("note", width=200)

        self.table.pack(fill="both", expand=True)

        tk.Button(right, text="🗑 Delete Selected", bg="#dc2626", fg="white",
                  font=("Arial", 10, "bold"), command=self.delete_transaction).pack(pady=5)

        # ===== GRAPH =====
        graph_frame = tk.Frame(right, bg="#020617", pady=10)
        graph_frame.pack(fill="x")

        tk.Label(graph_frame, text="Category-wise Expense (Bar Graph)",
                 fg="white", bg="#020617", font=("Arial", 11, "bold")).pack()

        self.canvas = tk.Canvas(graph_frame, width=600, height=200,
                                bg="#020617", highlightthickness=0)
        self.canvas.pack()

    # -------------------- LOGIC --------------------

    def add_transaction(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Enter a valid amount")
            return

        category = self.category_var.get()
        if not category:
            messagebox.showwarning("Missing", "Select a category")
            return

        data = {
            "date": datetime.now().strftime("%d-%m-%Y"),
            "type": self.type_var.get(),
            "category": category,
            "amount": amount,
            "note": self.note_entry.get()
        }

        transactions.append(data)
        save_data(transactions)

        self.load_table(transactions)
        self.update_summary()
        self.clear_fields()
        self.draw_graph(transactions)

    def load_table(self, data):
        self.table.delete(*self.table.get_children())
        for t in data:
            self.table.insert("", "end",
                              values=(t["date"], t["type"], t["category"],
                                      f"₹{t['amount']:.2f}", t["note"]))
        self.draw_graph(data)

    def update_summary(self):
        income = sum(t["amount"] for t in transactions if t["type"] == "Income")
        expense = sum(t["amount"] for t in transactions if t["type"] == "Expense")
        balance = income - expense

        self.income_label.config(text=f"Income: ₹{income:,.2f}")
        self.expense_label.config(text=f"Expense: ₹{expense:,.2f}")
        self.balance_label.config(text=f"Balance: ₹{balance:,.2f}")

        if self.budget_limit.get() > 0 and expense > self.budget_limit.get():
            messagebox.showwarning("Budget Alert",
                                   f"⚠ You crossed your budget of ₹{self.budget_limit.get():,.2f}")

    def clear_fields(self):
        self.amount_entry.delete(0, tk.END)
        self.note_entry.delete(0, tk.END)
        self.category_var.set("")

    def delete_transaction(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Select", "Select a transaction to delete")
            return

        index = self.table.index(selected[0])
        transactions.pop(index)
        save_data(transactions)
        self.load_table(transactions)
        self.update_summary()

    # -------------------- FILTER --------------------

    def apply_filter(self):
        try:
            from_d = datetime.strptime(self.from_date.get(), "%d-%m-%Y")
            to_d = datetime.strptime(self.to_date.get(), "%d-%m-%Y")
        except:
            messagebox.showerror("Error", "Use date format DD-MM-YYYY")
            return

        filtered = []
        for t in transactions:
            t_date = datetime.strptime(t["date"], "%d-%m-%Y")
            if from_d <= t_date <= to_d:
                filtered.append(t)

        self.load_table(filtered)

    # -------------------- GRAPH --------------------

    def draw_graph(self, data):
        self.canvas.delete("all")
        category_sum = {}

        for t in data:
            if t["type"] == "Expense":
                category_sum[t["category"]] = category_sum.get(t["category"], 0) + t["amount"]

        if not category_sum:
            return

        max_val = max(category_sum.values())
        y = 30

        for cat, val in category_sum.items():
            width = int((val / max_val) * 500)
            self.canvas.create_rectangle(20, y, 20 + width, y + 25, fill="#2563eb")
            self.canvas.create_text(25, y + 12, anchor="w",
                                    text=f"{cat} - ₹{val:.2f}", fill="white")
            y += 35

    # -------------------- EXPORT --------------------

    def export_csv(self):
        file = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV Files", "*.csv")])
        if not file:
            return

        with open(file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Type", "Category", "Amount", "Note"])
            for t in transactions:
                writer.writerow([t["date"], t["type"], t["category"], t["amount"], t["note"]])

        messagebox.showinfo("Exported", "Data exported successfully!")

# -------------------- RUN --------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceTracker(root)
    root.mainloop()


