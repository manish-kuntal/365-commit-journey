import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import socket
import requests
import csv
import os
import platform
import subprocess
import webbrowser
from datetime import datetime

HISTORY_FILE = "ip_history.csv"

# ------------------- NETWORK FUNCTIONS -------------------

def get_private_ip():
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except:
        return "N/A"

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text.strip()
    except:
        return "N/A"

def get_ipv6():
    try:
        return requests.get("https://api64.ipify.org").text.strip()
    except:
        return "N/A"

def get_geo_info(ip):
    """
    Using ip-api.com (free, no key)
    """
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,org,as,timezone,lat,lon,proxy,hosting,query"
        data = requests.get(url, timeout=6).json()

        if data.get("status") != "success":
            return None

        return {
            "country": data.get("country", "N/A"),
            "region": data.get("regionName", "N/A"),
            "city": data.get("city", "N/A"),
            "isp": data.get("isp", "N/A"),
            "org": data.get("org", "N/A"),
            "asn": data.get("as", "N/A"),
            "timezone": data.get("timezone", "N/A"),
            "lat": data.get("lat", "N/A"),
            "lon": data.get("lon", "N/A"),
            "proxy": "Yes" if data.get("proxy") else "No",
            "hosting": "Yes" if data.get("hosting") else "No"
        }
    except:
        return None

def ping_test(host="8.8.8.8"):
    try:
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "1", host]
        result = subprocess.run(command, capture_output=True, text=True)
        if "time=" in result.stdout:
            return result.stdout.split("time=")[-1].split("ms")[0] + " ms"
        return "Timeout"
    except:
        return "N/A"

def save_history(row):
    file_exists = os.path.exists(HISTORY_FILE)
    with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "Timestamp", "Public IP", "IPv6", "Private IP",
                "Country", "Region", "City", "ISP", "Org",
                "ASN", "Timezone", "Proxy", "Hosting",
                "Latitude", "Longitude", "Latency"
            ])
        writer.writerow(row)

# ------------------- UI APP -------------------

class IPFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Finder App - Professional Utility")
        self.root.geometry("820x620")
        self.root.resizable(False, False)

        self.create_theme()
        self.create_widgets()
        self.fetch_ip()

    def create_theme(self):
        self.root.configure(bg="#0f172a")  # Dark Blue

        style = ttk.Style()
        style.theme_use("default")

        style.configure("TButton",
                        font=("Segoe UI", 10, "bold"),
                        padding=6)

    def create_widgets(self):
        # Header
        header = tk.Frame(self.root, bg="#312e81", height=70)
        header.pack(fill="x")

        title = tk.Label(
            header, text="🌐 IP Finder Utility",
            fg="white", bg="#312e81",
            font=("Segoe UI", 20, "bold")
        )
        title.pack(pady=15)

        # Main Frame
        main = tk.Frame(self.root, bg="#0f172a", padx=25, pady=20)
        main.pack(fill="both", expand=True)

        labels = [
            "Public IP", "IPv6", "Private IP",
            "Country", "Region", "City",
            "ISP", "Organization", "ASN",
            "Timezone", "Proxy/VPN", "Hosting",
            "Latitude", "Longitude", "Latency (Ping)"
        ]

        self.vars = {}
        for i, label in enumerate(labels):
            tk.Label(
                main, text=label + ":",
                fg="#e5e7eb", bg="#0f172a",
                anchor="w", font=("Segoe UI", 10, "bold")
            ).grid(row=i, column=0, sticky="w", pady=6)

            var = tk.StringVar()
            entry = tk.Entry(
                main, textvariable=var,
                width=55, state="readonly",
                font=("Segoe UI", 10),
                readonlybackground="#111827",
                fg="#38bdf8"
            )
            entry.grid(row=i, column=1, pady=6, padx=12)
            self.vars[label] = var

        # Buttons
        btn_frame = tk.Frame(main, bg="#0f172a")
        btn_frame.grid(row=len(labels), column=0, columnspan=2, pady=25)

        ttk.Button(btn_frame, text="🔄 Refresh", command=self.fetch_ip).grid(row=0, column=0, padx=12)
        ttk.Button(btn_frame, text="📋 Copy Public IP", command=self.copy_ip).grid(row=0, column=1, padx=12)
        ttk.Button(btn_frame, text="📁 Export CSV", command=self.export_csv).grid(row=0, column=2, padx=12)
        ttk.Button(btn_frame, text="🗺 Open Map", command=self.open_map).grid(row=0, column=3, padx=12)

        # Footer
        footer = tk.Label(
            self.root,
            text="Secure API • VPN Detection • Offline History • Lightweight • VS Code Friendly",
            fg="#94a3b8", bg="#0f172a",
            font=("Segoe UI", 9)
        )
        footer.pack(pady=8)

    # ------------------- ACTIONS -------------------

    def fetch_ip(self):
        public_ip = get_public_ip()
        ipv6 = get_ipv6()
        private_ip = get_private_ip()
        geo = get_geo_info(public_ip)
        latency = ping_test()

        if not geo:
            messagebox.showwarning("Network Error", "Geo information not available. Check internet connection.")
            return

        self.vars["Public IP"].set(public_ip)
        self.vars["IPv6"].set(ipv6)
        self.vars["Private IP"].set(private_ip)
        self.vars["Country"].set(geo["country"])
        self.vars["Region"].set(geo["region"])
        self.vars["City"].set(geo["city"])
        self.vars["ISP"].set(geo["isp"])
        self.vars["Organization"].set(geo["org"])
        self.vars["ASN"].set(geo["asn"])
        self.vars["Timezone"].set(geo["timezone"])
        self.vars["Proxy/VPN"].set(geo["proxy"])
        self.vars["Hosting"].set(geo["hosting"])
        self.vars["Latitude"].set(geo["lat"])
        self.vars["Longitude"].set(geo["lon"])
        self.vars["Latency (Ping)"].set(latency)

        # Save History
        save_history([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            public_ip, ipv6, private_ip,
            geo["country"], geo["region"], geo["city"],
            geo["isp"], geo["org"], geo["asn"],
            geo["timezone"], geo["proxy"], geo["hosting"],
            geo["lat"], geo["lon"], latency
        ])

    def copy_ip(self):
        ip = self.vars["Public IP"].get()
        self.root.clipboard_clear()
        self.root.clipboard_append(ip)
        messagebox.showinfo("Copied", f"Public IP copied:\n{ip}")

    def export_csv(self):
        if not os.path.exists(HISTORY_FILE):
            messagebox.showwarning("No Data", "No history available yet.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )
        if save_path:
            with open(HISTORY_FILE, "r", encoding="utf-8") as src, open(save_path, "w", encoding="utf-8", newline="") as dest:
                dest.write(src.read())
            messagebox.showinfo("Exported", "IP history exported successfully.")

    def open_map(self):
        lat = self.vars["Latitude"].get()
        lon = self.vars["Longitude"].get()
        if lat != "N/A" and lon != "N/A":
            url = f"https://www.google.com/maps?q={lat},{lon}"
            webbrowser.open(url)
        else:
            messagebox.showwarning("Map Error", "Location coordinates not available.")

# ------------------- RUN -------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = IPFinderApp(root)
    root.mainloop()

