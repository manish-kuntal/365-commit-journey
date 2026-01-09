import tkinter as tk
from tkinter import messagebox
import calendar
from datetime import datetime
import json
import os

# ---------------------- FILE HANDLING ----------------------
FILE_NAME = "notes.json"

def load_notes():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return {}

def save_notes():
    with open(FILE_NAME, "w") as file:
        json.dump(notes_data, file, indent=4)

notes_data = load_notes()

# ---------------------- HOLIDAYS (Sample - India) ----------------------
holidays = {
    "01-01": "New Year",
    "26-01": "Republic Day",
    "15-08": "Independence Day",
    "02-10": "Gandhi Jayanti",
    "25-12": "Christmas"
}

# ---------------------- MAIN WINDOW ----------------------
root = tk.Tk()
root.title("Smart Calendar - Manish")
root.geometry("950x600")
root.configure(bg="#0a0f1f")

current_year = datetime.now().year
current_month = datetime.now().month

# ---------------------- HEADER ----------------------
header = tk.Label(root, text="📅 Smart Calendar", font=("Segoe UI", 22, "bold"),
                  bg="#0a0f1f", fg="#1f6feb")
header.pack(pady=5)

info_label = tk.Label(root, text="", font=("Segoe UI", 12),
                      bg="#0a0f1f", fg="white")
info_label.pack(pady=5)

# ---------------------- NAVIGATION BAR ----------------------
nav_frame = tk.Frame(root, bg="#0a0f1f")
nav_frame.pack(pady=5)

def prev_month():
    global current_month, current_year
    current_month -= 1
    if current_month == 0:
        current_month = 12
        current_year -= 1
    build_calendar(current_year, current_month)

def next_month():
    global current_month, current_year
    current_month += 1
    if current_month == 13:
        current_month = 1
        current_year += 1
    build_calendar(current_year, current_month)

def prev_year():
    global current_year
    current_year -= 1
    build_calendar(current_year, current_month)

def next_year():
    global current_year
    current_year += 1
    build_calendar(current_year, current_month)

tk.Button(nav_frame, text="⏪ Prev Year", command=prev_year,
          bg="#1a1f36", fg="white", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=5)

tk.Button(nav_frame, text="⬅ Prev Month", command=prev_month,
          bg="#1a1f36", fg="white", font=("Segoe UI", 10, "bold")).grid(row=0, column=1, padx=5)

tk.Button(nav_frame, text="Next Month ➡", command=next_month,
          bg="#1a1f36", fg="white", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, padx=5)

tk.Button(nav_frame, text="Next Year ⏩", command=next_year,
          bg="#1a1f36", fg="white", font=("Segoe UI", 10, "bold")).grid(row=0, column=3, padx=5)

# ---------------------- FRAME ----------------------
frame = tk.Frame(root, bg="#0a0f1f")
frame.pack()

calendar_frame = tk.Frame(frame, bg="#0a0f1f")
calendar_frame.grid(row=0, column=0, padx=20)

note_frame = tk.Frame(frame, bg="#0a0f1f")
note_frame.grid(row=0, column=1, padx=20)

# ---------------------- NOTE SECTION ----------------------
note_title = tk.Label(note_frame, text="📝 Notes", font=("Segoe UI", 16, "bold"),
                      bg="#0a0f1f", fg="#1f6feb")
note_title.pack(pady=5)

note_text = tk.Text(note_frame, width=30, height=10, font=("Segoe UI", 11))
note_text.pack(pady=10)

save_btn = tk.Button(note_frame, text="Save Note", bg="#1f6feb", fg="white",
                     font=("Segoe UI", 10, "bold"), command=lambda: save_note())
save_btn.pack(pady=5)

delete_btn = tk.Button(note_frame, text="Delete Note", bg="#ff4c4c", fg="white",
                       font=("Segoe UI", 10, "bold"), command=lambda: delete_note())
delete_btn.pack(pady=5)

selected_date = None

# ---------------------- FUNCTIONS ----------------------
def show_day(day):
    global selected_date
    selected_date = f"{current_year}-{current_month:02d}-{day:02d}"

    date_obj = datetime(current_year, current_month, day)
    day_name = date_obj.strftime("%A")
    formatted = date_obj.strftime("%d %B %Y")

    info_text = f"📌 {formatted} - {day_name}"

    # Check Holiday
    key = f"{day:02d}-{current_month:02d}"
    if key in holidays:
        info_text += f" | 🎉 {holidays[key]}"

    info_label.config(text=info_text)

    # Load Note
    note_text.delete("1.0", tk.END)
    if selected_date in notes_data:
        note_text.insert(tk.END, notes_data[selected_date]["note"])

def save_note():
    if not selected_date:
        messagebox.showwarning("No Date", "Please select a date first.")
        return

    text = note_text.get("1.0", tk.END).strip()
    if text == "":
        messagebox.showwarning("Empty Note", "Note cannot be empty.")
        return

    notes_data[selected_date] = {
        "note": text,
        "time": datetime.now().strftime("%H:%M:%S"),
        "date": datetime.now().strftime("%d-%m-%Y")
    }
    save_notes()
    messagebox.showinfo("Saved", "Note saved successfully.")

def delete_note():
    if not selected_date:
        messagebox.showwarning("No Date", "Please select a date first.")
        return

    if selected_date in notes_data:
        del notes_data[selected_date]
        save_notes()
        note_text.delete("1.0", tk.END)
        messagebox.showinfo("Deleted", "Note deleted.")
    else:
        messagebox.showwarning("Not Found", "No note exists for this date.")

# ---------------------- CALENDAR UI ----------------------
def build_calendar(year, month):
    for widget in calendar_frame.winfo_children():
        widget.destroy()

    cal = calendar.monthcalendar(year, month)

    month_label = tk.Label(calendar_frame, text=f"{calendar.month_name[month]} {year}",
                           font=("Segoe UI", 16, "bold"), bg="#0a0f1f", fg="#1f6feb")
    month_label.grid(row=0, column=0, columnspan=7, pady=10)

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, day in enumerate(days):
        tk.Label(calendar_frame, text=day, bg="#0a0f1f", fg="white",
                 font=("Segoe UI", 10, "bold")).grid(row=1, column=i, pady=5)

    for r, week in enumerate(cal):
        for c, day in enumerate(week):
            if day == 0:
                tk.Label(calendar_frame, text="", bg="#0a0f1f").grid(row=r+2, column=c)
            else:
                key = f"{day:02d}-{month:02d}"
                bg_color = "#1f6feb" if key in holidays else "#1a1f36"

                btn = tk.Button(calendar_frame, text=str(day), width=5, height=2,
                                bg=bg_color, fg="white",
                                font=("Segoe UI", 10, "bold"),
                                command=lambda d=day: show_day(d))
                btn.grid(row=r+2, column=c, padx=2, pady=2)

# ---------------------- INITIAL LOAD ----------------------
build_calendar(current_year, current_month)

# ---------------------- RUN ----------------------
root.mainloop()
