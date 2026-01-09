import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser, font
from datetime import datetime

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("BlueNote - Python Notes Application")
root.geometry("900x600")
root.config(bg="#0d1117")   # Dark background

# ---------------- GLOBAL VARIABLES ----------------
current_file = None

# ---------------- FUNCTIONS ----------------

def new_note():
    global current_file
    current_file = None
    text_area.delete(1.0, tk.END)
    update_status("New Note")

def save_note():
    global current_file
    if current_file:
        with open(current_file, "w", encoding="utf-8") as file:
            file.write(text_area.get(1.0, tk.END))
        update_status("Note Saved")
    else:
        save_as_note()

def save_as_note():
    global current_file
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")])
    if file_path:
        current_file = file_path
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text_area.get(1.0, tk.END))
        update_status("Note Saved As")

def open_note():
    global current_file
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        current_file = file_path
        text_area.delete(1.0, tk.END)
        with open(file_path, "r", encoding="utf-8") as file:
            text_area.insert(tk.END, file.read())
        update_status("Note Opened")

def delete_note():
    global current_file
    if messagebox.askyesno("Delete", "Are you sure you want to delete this note?"):
        text_area.delete(1.0, tk.END)
        current_file = None
        update_status("Note Deleted")

def change_text_color():
    color = colorchooser.askcolor()[1]
    if color:
        text_area.config(fg=color)

def change_bg_color():
    color = colorchooser.askcolor()[1]
    if color:
        text_area.config(bg=color)

def change_font_style():
    font_window = tk.Toplevel(root)
    font_window.title("Select Font")
    font_window.geometry("300x300")
    font_window.config(bg="#0d1117")

    fonts = list(font.families())
    fonts.sort()

    font_list = tk.Listbox(font_window)
    font_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    for f in fonts:
        font_list.insert(tk.END, f)

    def apply_font():
        selected_font = font_list.get(tk.ACTIVE)
        text_area.config(font=(selected_font, 12))
        font_window.destroy()

    apply_btn = tk.Button(font_window, text="Apply", command=apply_font, bg="#1f6feb", fg="white")
    apply_btn.pack(pady=10)

def update_status(msg):
    now = datetime.now().strftime("%d-%m-%Y  %I:%M:%S %p")
    status_bar.config(text=f"{msg} | {now}")

# ---------------- MENU BAR ----------------
menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_note)
file_menu.add_command(label="Open", command=open_note)
file_menu.add_command(label="Save", command=save_note)
file_menu.add_command(label="Save As", command=save_as_note)
file_menu.add_separator()
file_menu.add_command(label="Delete", command=delete_note)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

menu_bar.add_cascade(label="File", menu=file_menu)

format_menu = tk.Menu(menu_bar, tearoff=0)
format_menu.add_command(label="Change Text Color", command=change_text_color)
format_menu.add_command(label="Change Background Color", command=change_bg_color)
format_menu.add_command(label="Change Font", command=change_font_style)

menu_bar.add_cascade(label="Format", menu=format_menu)

root.config(menu=menu_bar)

# ---------------- TEXT AREA ----------------
text_area = tk.Text(root, wrap=tk.WORD, font=("Arial", 12),
                    bg="#010409", fg="#1f6feb", insertbackground="white")
text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# ---------------- STATUS BAR (DATE & TIME) ----------------
status_bar = tk.Label(root, text="Welcome to BlueNote",
                      bg="#0d1117", fg="#58a6ff", anchor="e")
status_bar.pack(fill=tk.X, side=tk.BOTTOM)

update_status("Ready")

# ---------------- RUN APP ----------------
root.mainloop()
