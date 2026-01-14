import tkinter as tk
from tkinter import ttk
import time

class AppUsageTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("App Usage Tracker")
        self.root.geometry("820x520")
        self.root.configure(bg="#0f172a")

        self.start_time = time.time()
        self.create_header()
        self.create_body()
        self.update_timer()

    def create_header(self):
        header = tk.Frame(self.root, bg="#312e81", height=70)
        header.pack(fill="x")
        tk.Label(header, text="📊 App Usage Tracker", fg="white", bg="#312e81",
                 font=("Segoe UI", 20, "bold")).pack(pady=15)

    def create_body(self):
        self.body = tk.Frame(self.root, bg="#0f172a", padx=25, pady=25)
        self.body.pack(fill="both", expand=True)

        self.time_var = tk.StringVar()
        tk.Label(self.body, text="App Running Time:", fg="white", bg="#0f172a",
                 font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="w", pady=10)
        tk.Entry(self.body, textvariable=self.time_var, width=40, state="readonly",
                 readonlybackground="#111827", fg="#38bdf8",
                 font=("Segoe UI", 11)).grid(row=0, column=1, pady=10, padx=10)

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        self.time_var.set(f"{elapsed} seconds")
        self.root.after(1000, self.update_timer)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppUsageTracker(root)
    root.mainloop()

