import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
from datetime import datetime

# ------------------- CONFIG -------------------
APP_TITLE = "Study Timer - Pro"
THEME_BG = "#0f172a"
THEME_HEADER = "#312e81"
THEME_TEXT = "#e5e7eb"
THEME_ACCENT = "#38bdf8"

LOG_FILE = "study_sessions.csv"

# ------------------- MAIN APP -------------------
class StudyTimerPro:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("900x600")
        self.root.configure(bg=THEME_BG)
        self.root.resizable(False, False)

        self.seconds = 0
        self.running = False
        self.current_subject = ""

        self.create_header()
        self.create_body()
        self.load_logs()
        self.update_timer()

    # ------------------- UI -------------------
    def create_header(self):
        header = tk.Frame(self.root, bg=THEME_HEADER, height=70)
        header.pack(fill="x")

        tk.Label(
            header, text="📚 Study Timer - Professional",
            fg="white", bg=THEME_HEADER,
            font=("Segoe UI", 20, "bold")
        ).pack(pady=15)

    def create_body(self):
        body = tk.Frame(self.root, bg=THEME_BG, padx=25, pady=25)
        body.pack(fill="both", expand=True)

        # Subject input
        subject_frame = tk.Frame(body, bg=THEME_BG)
        subject_frame.pack(anchor="w")

        tk.Label(subject_frame, text="Subject:", fg=THEME_TEXT, bg=THEME_BG,
                 font=("Segoe UI", 11, "bold")).pack(side="left")
        self.subject_var = tk.StringVar()
        tk.Entry(subject_frame, textvariable=self.subject_var, width=25,
                 font=("Segoe UI", 11)).pack(side="left", padx=10)

        # Break Reminder
        tk.Label(subject_frame, text="Break (min):", fg=THEME_TEXT, bg=THEME_BG,
                 font=("Segoe UI", 11, "bold")).pack(side="left", padx=(20,5))
        self.break_var = tk.StringVar(value="30")
        tk.Entry(subject_frame, textvariable=self.break_var, width=5,
                 font=("Segoe UI", 11)).pack(side="left")

        # Timer Display
        self.time_var = tk.StringVar()
        tk.Label(
            body, textvariable=self.time_var,
            fg=THEME_ACCENT, bg=THEME_BG,
            font=("Segoe UI", 48, "bold")
        ).pack(pady=30)

        # Control Buttons
        btn_frame = tk.Frame(body, bg=THEME_BG)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="▶ Start", command=self.start).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="⏸ Pause", command=self.pause).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="⏹ Stop", command=self.stop).grid(row=0, column=2, padx=10)
        ttk.Button(btn_frame, text="🔄 Reset", command=self.reset).grid(row=0, column=3, padx=10)

        # History Label
        tk.Label(body, text="📊 Study History", fg=THEME_TEXT, bg=THEME_BG,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(20,5))

        # Table
        columns = ("Date", "Subject", "Duration (min)")
        self.tree = ttk.Treeview(body, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=200)

        self.tree.pack(fill="x")

        # Bottom Buttons
        bottom_frame = tk.Frame(body, bg=THEME_BG)
        bottom_frame.pack(pady=15)

        ttk.Button(bottom_frame, text="💾 Save Session", command=self.save_session).grid(row=0, column=0, padx=10)
        ttk.Button(bottom_frame, text="📤 Export CSV", command=self.export_csv).grid(row=0, column=1, padx=10)
        ttk.Button(bottom_frame, text="🗑 Clear History", command=self.clear_history).grid(row=0, column=2, padx=10)

    # ------------------- TIMER FUNCTIONS -------------------
    def start(self):
        if not self.subject_var.get().strip():
            messagebox.showwarning("Subject Missing", "Please enter subject name before starting.")
            return
        self.running = True
        self.current_subject = self.subject_var.get().strip()

    def pause(self):
        self.running = False

    def stop(self):
        if self.seconds > 0:
            self.save_session()
        self.running = False
        self.seconds = 0

    def reset(self):
        self.running = False
        self.seconds = 0

    def update_timer(self):
        mins = self.seconds // 60
        secs = self.seconds % 60
        self.time_var.set(f"{mins:02d}:{secs:02d}")

        if self.running:
            self.seconds += 1
            self.check_break_reminder()

        self.root.after(1000, self.update_timer)

    def check_break_reminder(self):
        try:
            break_minutes = int(self.break_var.get())
            if break_minutes > 0 and self.seconds % (break_minutes * 60) == 0:
                messagebox.showinfo("Break Time", "⏸ Time for a short break!")
        except:
            pass

    # ------------------- DATA FUNCTIONS -------------------
    def save_session(self):
        if self.seconds < 60:
            return

        duration_min = round(self.seconds / 60, 2)
        date = datetime.now().strftime("%Y-%m-%d %H:%M")

        self.tree.insert("", "end", values=(date, self.current_subject, duration_min))

        file_exists = os.path.exists(LOG_FILE)
        with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Date", "Subject", "Duration (min)"])
            writer.writerow([date, self.current_subject, duration_min])

        self.seconds = 0

    def load_logs(self):
        if not os.path.exists(LOG_FILE):
            return

        with open(LOG_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                self.tree.insert("", "end", values=row)

    def export_csv(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not path:
            return

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Subject", "Duration (min)"])
            for row in self.tree.get_children():
                writer.writerow(self.tree.item(row)["values"])

        messagebox.showinfo("Exported", "Study history exported successfully!")

    def clear_history(self):
        if messagebox.askyesno("Confirm", "Clear all study history?"):
            for row in self.tree.get_children():
                self.tree.delete(row)
            if os.path.exists(LOG_FILE):
                os.remove(LOG_FILE)

# ------------------- RUN -------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = StudyTimerPro(root)
    root.mainloop()

