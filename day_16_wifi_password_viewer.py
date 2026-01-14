import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import re

# ---------- WIFI FUNCTIONS ----------

def get_wifi_profiles():
    try:
        data = subprocess.check_output(["netsh", "wlan", "show", "profiles"], encoding="utf-8", errors="ignore")
        return re.findall(r"All User Profile\s*:\s*(.*)", data)
    except:
        return []

def get_wifi_password(name):
    try:
        data = subprocess.check_output(["netsh", "wlan", "show", "profile", name, "key=clear"], encoding="utf-8", errors="ignore")
        match = re.search(r"Key Content\s*:\s*(.*)", data)
        return match.group(1) if match else "Not Found"
    except:
        return "Permission Denied"

# ---------- UI APP ----------

class WiFiPasswordViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("WiFi Password Viewer")
        self.root.geometry("820x560")
        self.root.configure(bg="#0f172a")

        self.create_header()
        self.create_body()
        self.load_profiles()

    def create_header(self):
        header = tk.Frame(self.root, bg="#312e81", height=70)
        header.pack(fill="x")
        tk.Label(header, text="🔐 WiFi Password Viewer", fg="white", bg="#312e81",
                 font=("Segoe UI", 20, "bold")).pack(pady=15)

    def create_body(self):
        body = tk.Frame(self.root, bg="#0f172a", padx=20, pady=20)
        body.pack(fill="both", expand=True)

        warning = tk.Label(body, text="⚠ Security Notice: Read-only tool. Admin permission required to view passwords.",
                           fg="#facc15", bg="#0f172a", font=("Segoe UI", 10, "bold"))
        warning.pack(anchor="w", pady=(0,10))

        # Search
        search_frame = tk.Frame(body, bg="#0f172a")
        search_frame.pack(fill="x", pady=5)
        tk.Label(search_frame, text="Search Network:", fg="white", bg="#0f172a").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.filter_list())
        tk.Entry(search_frame, textvariable=self.search_var, width=40).pack(side="left", padx=10)

        # Listbox
        self.listbox = tk.Listbox(body, height=12, font=("Segoe UI", 11))
        self.listbox.pack(fill="x", pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.show_password)

        # Output
        out_frame = tk.Frame(body, bg="#0f172a")
        out_frame.pack(fill="x", pady=10)

        tk.Label(out_frame, text="Password:", fg="white", bg="#0f172a",
                 font=("Segoe UI", 10, "bold")).pack(side="left")
        self.pass_var = tk.StringVar()
        tk.Entry(out_frame, textvariable=self.pass_var, width=50,
                 state="readonly", readonlybackground="#111827",
                 fg="#38bdf8", font=("Segoe UI", 11)).pack(side="left", padx=10)

        btn_frame = tk.Frame(body, bg="#0f172a")
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="📋 Copy", command=self.copy_password).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="🔄 Refresh", command=self.load_profiles).grid(row=0, column=1, padx=10)

    def load_profiles(self):
        self.listbox.delete(0, tk.END)
        self.profiles = get_wifi_profiles()
        for p in self.profiles:
            self.listbox.insert(tk.END, p)

    def filter_list(self):
        query = self.search_var.get().lower()
        self.listbox.delete(0, tk.END)
        for p in self.profiles:
            if query in p.lower():
                self.listbox.insert(tk.END, p)

    def show_password(self, event):
        try:
            index = self.listbox.curselection()[0]
            profile = self.listbox.get(index)
            pwd = get_wifi_password(profile)
            self.pass_var.set(pwd)
        except:
            pass

    def copy_password(self):
        pwd = self.pass_var.get()
        if pwd:
            self.root.clipboard_clear()
            self.root.clipboard_append(pwd)
            messagebox.showinfo("Copied", "Password copied to clipboard.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WiFiPasswordViewer(root)
    root.mainloop()
