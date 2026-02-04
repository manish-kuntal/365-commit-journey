# ================== Subscription Reminder ==================
# Product-grade desktop app (Python + Tkinter)
# Author: Manish
# ==========================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import json, os, csv

# -------- Optional: PDF Export (requires reportlab) --------
# If not installed: pip install reportlab
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
    from reportlab.lib import colors
    PDF_OK = True
except:
    PDF_OK = False

DATA_FILE = "subscriptions.json"
PIN_FILE = "pin.json"

# -------------------- DATA HANDLING --------------------

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_pin():
    if os.path.exists(PIN_FILE):
        with open(PIN_FILE, "r") as f:
            return json.load(f).get("pin")
    return None

def save_pin(pin):
    with open(PIN_FILE, "w") as f:
        json.dump({"pin": pin}, f)

subscriptions = load_data()

# -------------------- UTILITIES --------------------

def parse_date(s):
    return datetime.strptime(s, "%d-%m-%Y")

def money(v):
    return f"₹{v:,.2f}"

# -------------------- APP --------------------

class SubscriptionReminder:
    def __init__(self, root):
        self.root = root
        self.root.title("Subscription Reminder - Manish")
        self.root.geometry("1200x740")
        self.root.configure(bg="#0f172a")

        self.create_ui()
        self.refresh_all()
        self.check_upcoming()

    # -------------------- UI --------------------

    def create_ui(self):
        # ===== HEADER =====
        header = tk.Frame(self.root, bg="#3b82f6", height=70)
        header.pack(fill="x")

        tk.Label(header, text="💳 Subscription Reminder",
                 font=("Arial", 20, "bold"), fg="white", bg="#3b82f6").pack(side="left", padx=20, pady=15)

        tk.Label(header, text="Track • Save • Cancel Smarter",
                 font=("Arial", 10), fg="#e0e7ff", bg="#3b82f6").pack(side="left", padx=10)

        tk.Button(header, text="🔐 Set / Change PIN", bg="#1e40af", fg="white",
                  command=self.set_pin).pack(side="right", padx=10, pady=15)

        # ===== MAIN =====
        main = tk.Frame(self.root, bg="#0f172a")
        main.pack(fill="both", expand=True, padx=15, pady=15)

        # ===== LEFT: FORM =====
        left = tk.Frame(main, bg="#020617", padx=15, pady=15)
        left.pack(side="left", fill="y")

        tk.Label(left, text="➕ Add / Edit Subscription",
                 font=("Arial", 14, "bold"), fg="#38bdf8", bg="#020617").pack(pady=10)

        def lbl(txt):
            return tk.Label(left, text=txt, fg="white", bg="#020617")

        # Service
        lbl("Service Name").pack(anchor="w")
        self.service_entry = tk.Entry(left, bg="#020617", fg="white", insertbackground="white")
        self.service_entry.pack(fill="x", pady=4)

        # Category
        lbl("Category").pack(anchor="w")
        self.category_var = tk.StringVar()
        ttk.Combobox(left, textvariable=self.category_var,
                     values=["Entertainment", "Tools", "Education", "Utilities", "Other"],
                     state="readonly").pack(fill="x", pady=4)

        # Amount
        lbl("Amount (₹)").pack(anchor="w")
        self.amount_entry = tk.Entry(left, bg="#020617", fg="white", insertbackground="white")
        self.amount_entry.pack(fill="x", pady=4)

        # Billing
        lbl("Billing Cycle").pack(anchor="w")
        self.billing_var = tk.StringVar(value="Monthly")
        ttk.Combobox(left, textvariable=self.billing_var,
                     values=["Monthly", "Yearly"], state="readonly").pack(fill="x", pady=4)

        # Next Date
        lbl("Next Payment Date (DD-MM-YYYY)").pack(anchor="w")
        self.next_entry = tk.Entry(left, bg="#020617", fg="white", insertbackground="white")
        self.next_entry.pack(fill="x", pady=4)

        # Last Used
        lbl("Last Used Date (DD-MM-YYYY)").pack(anchor="w")
        self.last_entry = tk.Entry(left, bg="#020617", fg="white", insertbackground="white")
        self.last_entry.pack(fill="x", pady=4)

        # Note
        lbl("Note").pack(anchor="w")
        self.note_entry = tk.Entry(left, bg="#020617", fg="white", insertbackground="white")
        self.note_entry.pack(fill="x", pady=4)

        # Savings Goal
        lbl("Monthly Savings Goal (₹)").pack(anchor="w")
        self.goal_entry = tk.Entry(left, bg="#020617", fg="white", insertbackground="white")
        self.goal_entry.pack(fill="x", pady=4)

        # Buttons
        tk.Button(left, text="Add", bg="#2563eb", fg="white",
                  font=("Arial", 11, "bold"), command=self.add_item).pack(fill="x", pady=6)
        tk.Button(left, text="Update Selected", bg="#1e40af", fg="white",
                  font=("Arial", 11, "bold"), command=self.update_item).pack(fill="x")
        tk.Button(left, text="Clear", bg="#334155", fg="white",
                  font=("Arial", 11, "bold"), command=self.clear_fields).pack(fill="x", pady=6)

        # Export
        tk.Label(left, text="📤 Export", fg="#38bdf8", bg="#020617",
                 font=("Arial", 12, "bold")).pack(pady=10)
        tk.Button(left, text="Export CSV", bg="#16a34a", fg="white",
                  command=self.export_csv).pack(fill="x", pady=4)
        tk.Button(left, text="Export PDF", bg="#22c55e", fg="white",
                  command=self.export_pdf).pack(fill="x", pady=4)

        # ===== RIGHT =====
        right = tk.Frame(main, bg="#0f172a")
        right.pack(side="left", fill="both", expand=True, padx=10)

        # ===== SUMMARY =====
        summary = tk.Frame(right, bg="#020617", pady=12)
        summary.pack(fill="x")

        self.active_lbl = tk.Label(summary, text="Active: 0", fg="#38bdf8", bg="#020617",
                                    font=("Arial", 12, "bold"))
        self.active_lbl.pack(side="left", padx=20)

        self.monthly_lbl = tk.Label(summary, text="Monthly Spend: ₹0.00", fg="#22c55e", bg="#020617",
                                     font=("Arial", 12, "bold"))
        self.monthly_lbl.pack(side="left", padx=20)

        self.unused_lbl = tk.Label(summary, text="Unused: 0", fg="#ef4444", bg="#020617",
                                    font=("Arial", 12, "bold"))
        self.unused_lbl.pack(side="left", padx=20)

        self.optimize_lbl = tk.Label(summary, text="Optimization: ₹0.00", fg="#f59e0b", bg="#020617",
                                      font=("Arial", 12, "bold"))
        self.optimize_lbl.pack(side="left", padx=20)

        # ===== TABLE =====
        table_frame = tk.Frame(right, bg="#0f172a")
        table_frame.pack(fill="both", expand=True, pady=10)

        cols = ("service", "category", "amount", "billing", "next", "last", "status")
        self.table = ttk.Treeview(table_frame, columns=cols, show="headings")
        for c in cols:
            self.table.heading(c, text=c.capitalize())
        self.table.column("service", width=150)
        self.table.column("category", width=120)
        self.table.column("amount", width=110)
        self.table.column("billing", width=90)
        self.table.column("next", width=130)
        self.table.column("last", width=130)
        self.table.column("status", width=150)
        self.table.pack(fill="both", expand=True)

        tk.Button(right, text="🗑 Delete Selected", bg="#dc2626", fg="white",
                  font=("Arial", 10, "bold"), command=self.delete_item).pack(pady=5)

        # ===== GRAPHS =====
        graphs = tk.Frame(right, bg="#020617", pady=10)
        graphs.pack(fill="x")

        tk.Label(graphs, text="Category-wise Monthly Spend", fg="white", bg="#020617",
                 font=("Arial", 11, "bold")).pack()
        self.canvas_cat = tk.Canvas(graphs, width=600, height=200,
                                    bg="#020617", highlightthickness=0)
        self.canvas_cat.pack()

        tk.Label(graphs, text="Monthly Trend (Jan–Dec)", fg="white", bg="#020617",
                 font=("Arial", 11, "bold")).pack(pady=(10, 0))
        self.canvas_trend = tk.Canvas(graphs, width=600, height=200,
                                      bg="#020617", highlightthickness=0)
        self.canvas_trend.pack()

        # ===== CONCEPT AREA =====
        concept = tk.Frame(right, bg="#0f172a")
        concept.pack(fill="x", pady=8)
        tk.Label(concept, text="🔮 Concepts (Future): Bank/UPI auto-detect • Android (Kivy)",
                 fg="#94a3b8", bg="#0f172a", font=("Arial", 10)).pack(anchor="w")

    # -------------------- CORE LOGIC --------------------

    def add_item(self):
        try:
            amt = float(self.amount_entry.get())
            if amt <= 0: raise ValueError
            parse_date(self.next_entry.get())
            parse_date(self.last_entry.get())
        except:
            messagebox.showerror("Error", "Invalid amount or date (DD-MM-YYYY).")
            return

        if not self.service_entry.get() or not self.category_var.get():
            messagebox.showwarning("Missing", "Service and Category required.")
            return

        data = {
            "service": self.service_entry.get(),
            "category": self.category_var.get(),
            "amount": amt,
            "billing": self.billing_var.get(),
            "next": self.next_entry.get(),
            "last": self.last_entry.get(),
            "note": self.note_entry.get()
        }
        subscriptions.append(data)
        save_data(subscriptions)
        self.refresh_all()

    def update_item(self):
        sel = self.table.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a row to update.")
            return
        idx = self.table.index(sel[0])

        try:
            amt = float(self.amount_entry.get())
            parse_date(self.next_entry.get())
            parse_date(self.last_entry.get())
        except:
            messagebox.showerror("Error", "Invalid values.")
            return

        subscriptions[idx] = {
            "service": self.service_entry.get(),
            "category": self.category_var.get(),
            "amount": amt,
            "billing": self.billing_var.get(),
            "next": self.next_entry.get(),
            "last": self.last_entry.get(),
            "note": self.note_entry.get()
        }
        save_data(subscriptions)
        self.refresh_all()

    def delete_item(self):
        sel = self.table.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a row to delete.")
            return
        idx = self.table.index(sel[0])
        subscriptions.pop(idx)
        save_data(subscriptions)
        self.refresh_all()

    # -------------------- SMART FEATURES --------------------

    def is_unused(self, s):
        last = parse_date(s["last"])
        return (datetime.now() - last).days > 30

    def status(self, s):
        if self.is_unused(s):
            return "⚠ Consider Cancel"
        return "Active"

    def optimization_savings(self):
        # Sum of monthly amounts for unused subscriptions
        return sum(s["amount"] for s in subscriptions
                   if self.is_unused(s) and s["billing"] == "Monthly")

    def check_upcoming(self):
        today = datetime.now()
        for s in subscriptions:
            nxt = parse_date(s["next"])
            # 3-day reminder
            if today + timedelta(days=3) >= nxt:
                messagebox.showinfo("Upcoming Payment",
                                    f"🔔 {s['service']} due on {s['next']} ({money(s['amount'])})")
            # Yearly auto-renew warning
            if s["billing"] == "Yearly" and today + timedelta(days=5) >= nxt:
                messagebox.showwarning("Auto-Renew Alert",
                                       f"⚠ {s['service']} yearly plan auto-renews on {s['next']} ({money(s['amount'])})")

    # -------------------- RENDER --------------------

    def refresh_all(self):
        self.load_table()
        self.update_summary()
        self.draw_category_graph()
        self.draw_monthly_trend()
        self.clear_fields()

    def load_table(self):
        self.table.delete(*self.table.get_children())
        for s in subscriptions:
            self.table.insert("", "end",
                              values=(s["service"], s["category"], money(s["amount"]),
                                      s["billing"], s["next"], s["last"], self.status(s)))

    def update_summary(self):
        active = len(subscriptions)
        monthly = sum(s["amount"] for s in subscriptions if s["billing"] == "Monthly")
        unused = sum(1 for s in subscriptions if self.is_unused(s))
        opt = self.optimization_savings()

        self.active_lbl.config(text=f"Active: {active}")
        self.monthly_lbl.config(text=f"Monthly Spend: {money(monthly)}")
        self.unused_lbl.config(text=f"Unused: {unused}")
        self.optimize_lbl.config(text=f"Optimization: Save {money(opt)} / month")

        # Savings Goal Feedback
        try:
            goal = float(self.goal_entry.get())
            if opt >= goal and goal > 0:
                messagebox.showinfo("Goal Reached", "🎯 Your optimization meets the savings goal!")
        except:
            pass

    # -------------------- GRAPHS --------------------

    def draw_category_graph(self):
        self.canvas_cat.delete("all")
        cat_sum = {}
        for s in subscriptions:
            if s["billing"] == "Monthly":
                cat_sum[s["category"]] = cat_sum.get(s["category"], 0) + s["amount"]
        if not cat_sum:
            return
        maxv = max(cat_sum.values())
        y = 20
        for cat, val in cat_sum.items():
            w = int((val / maxv) * 560)
            self.canvas_cat.create_rectangle(20, y, 20 + w, y + 22, fill="#2563eb")
            self.canvas_cat.create_text(25, y + 11, anchor="w",
                                        text=f"{cat} - {money(val)}", fill="white")
            y += 32

    def draw_monthly_trend(self):
        self.canvas_trend.delete("all")
        months = {i: 0 for i in range(1, 13)}
        for s in subscriptions:
            try:
                d = parse_date(s["next"])
                if s["billing"] == "Monthly":
                    months[d.month] += s["amount"]
            except:
                pass
        maxv = max(months.values()) if months.values() else 0
        if maxv == 0:
            return
        x = 20
        for m in range(1, 13):
            h = int((months[m] / maxv) * 160)
            self.canvas_trend.create_rectangle(x, 180 - h, x + 30, 180, fill="#1e40af")
            self.canvas_trend.create_text(x + 15, 190, text=datetime(2024, m, 1).strftime("%b"),
                                           fill="white")
            x += 45

    # -------------------- EXPORT --------------------

    def export_csv(self):
        file = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV Files", "*.csv")])
        if not file:
            return
        with open(file, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Service", "Category", "Amount", "Billing", "Next", "Last", "Status"])
            for s in subscriptions:
                w.writerow([s["service"], s["category"], s["amount"],
                            s["billing"], s["next"], s["last"], self.status(s)])
        messagebox.showinfo("Exported", "CSV exported successfully!")

    def export_pdf(self):
        if not PDF_OK:
            messagebox.showerror("Missing Library", "Install reportlab: pip install reportlab")
            return
        file = filedialog.asksaveasfilename(defaultextension=".pdf",
                                            filetypes=[("PDF Files", "*.pdf")])
        if not file:
            return
        doc = SimpleDocTemplate(file, pagesize=A4)
        styles = getSampleStyleSheet()
        elems = []
        elems.append(Paragraph("<b>Subscription Reminder Report</b>", styles["Title"]))
        elems.append(Paragraph(f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}", styles["Normal"]))
        data = [["Service", "Category", "Amount", "Billing", "Next", "Last", "Status"]]
        for s in subscriptions:
            data.append([s["service"], s["category"], money(s["amount"]), s["billing"],
                         s["next"], s["last"], self.status(s)])
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey)
        ]))
        elems.append(table)
        doc.build(elems)
        messagebox.showinfo("Exported", "PDF exported successfully!")

    # -------------------- SECURITY --------------------

    def set_pin(self):
        def save():
            p = e.get()
            if len(p) < 4:
                messagebox.showwarning("Weak PIN", "Use at least 4 digits.")
                return
            save_pin(p)
            win.destroy()
            messagebox.showinfo("Saved", "PIN updated.")
        win = tk.Toplevel(self.root)
        win.title("Set PIN")
        tk.Label(win, text="Enter new PIN:").pack(padx=10, pady=5)
        e = tk.Entry(win, show="*")
        e.pack(padx=10, pady=5)
        tk.Button(win, text="Save", command=save).pack(pady=8)

    # -------------------- UTILS --------------------

    def clear_fields(self):
        self.service_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.next_entry.delete(0, tk.END)
        self.last_entry.delete(0, tk.END)
        self.note_entry.delete(0, tk.END)
        self.category_var.set("")
        self.billing_var.set("Monthly")

# -------------------- BOOT --------------------

def ask_pin_if_set(root):
    p = load_pin()
    if not p:
        return True
    ok = {"val": False}
    win = tk.Toplevel(root)
    win.title("Enter PIN")
    tk.Label(win, text="Enter PIN:").pack(padx=10, pady=5)
    e = tk.Entry(win, show="*")
    e.pack(padx=10, pady=5)
    def check():
        if e.get() == p:
            ok["val"] = True
            win.destroy()
        else:
            messagebox.showerror("Wrong", "Incorrect PIN")
    tk.Button(win, text="Unlock", command=check).pack(pady=8)
    root.wait_window(win)
    return ok["val"]

if __name__ == "__main__":
    root = tk.Tk()
    if ask_pin_if_set(root):
        app = SubscriptionReminder(root)
        root.mainloop()
    else:
        root.destroy()

