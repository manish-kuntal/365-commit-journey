import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
from datetime import datetime

# -------------------- Database Path --------------------
DB_PATH = os.path.join(os.path.dirname(__file__), "tasks.db")

# -------------------- Task Model --------------------
class Task:
    def __init__(self, id_, title, description, category, created_at):
        self.id = id_
        self.title = title
        self.description = description
        self.category = category
        self.created_at = created_at

# -------------------- Database Layer --------------------
class DB:
    def __init__(self, path=DB_PATH):
        self.conn = sqlite3.connect(path)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT,
            created_at TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_task(self, title, description, category):
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "INSERT INTO tasks (title, description, category, created_at) VALUES (?, ?, ?, ?)"
        self.conn.execute(query, (title, description, category, created_at))
        self.conn.commit()

    def get_tasks(self):
        cursor = self.conn.execute("SELECT * FROM tasks ORDER BY id DESC")
        return cursor.fetchall()

    def delete_all(self):
        self.conn.execute("DELETE FROM tasks")
        self.conn.commit()

# -------------------- Main App --------------------
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do | Day 2")
        self.root.geometry("1100x600")
        self.root.configure(bg="#0b2d4d")

        self.db = DB()

        self.build_ui()
        self.load_tasks()

    # -------------------- UI Layout --------------------
    def build_ui(self):
        # Main Container
        main_frame = tk.Frame(self.root, bg="#0b2d4d")
        main_frame.pack(fill="both", expand=True)

        # Left Panel
        self.left_panel = tk.Frame(main_frame, bg="#0b2d4d")
        self.left_panel.pack(side="left", fill="both", expand=True)

        # Right Panel
        self.right_panel = tk.Frame(main_frame, bg="#0f3b66", width=400)
        self.right_panel.pack(side="right", fill="y")

        # ---------------- Left UI ----------------
        title = tk.Label(
            self.left_panel,
            text="My Tasks",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#0b2d4d"
        )
        title.pack(pady=20)

        self.task_list_frame = tk.Frame(self.left_panel, bg="#0b2d4d")
        self.task_list_frame.pack(fill="both", expand=True)

        self.empty_label = tk.Label(
            self.task_list_frame,
            text="Add First Task",
            font=("Arial", 14),
            fg="#9ecbff",
            bg="#0b2d4d"
        )
        self.empty_label.pack(pady=50)

        # Floating + Button
        add_btn = tk.Button(
            self.left_panel,
            text="+",
            font=("Arial", 18, "bold"),
            bg="#14b8a6",
            fg="white",
            width=3,
            height=1,
            bd=0,
            command=self.show_add_panel
        )
        add_btn.place(relx=0.95, rely=0.90, anchor="center")

        # ---------------- Right UI ----------------
        form_title = tk.Label(
            self.right_panel,
            text="Add Task",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#0f3b66"
        )
        form_title.pack(pady=15)

        # Title
        tk.Label(self.right_panel, text="Task Title", fg="white", bg="#0f3b66").pack(anchor="w", padx=20)
        self.title_entry = tk.Entry(self.right_panel, font=("Arial", 12))
        self.title_entry.pack(fill="x", padx=20, pady=5)

        # Description
        tk.Label(self.right_panel, text="Description", fg="white", bg="#0f3b66").pack(anchor="w", padx=20, pady=(10, 0))
        self.desc_text = tk.Text(self.right_panel, height=5, font=("Arial", 12))
        self.desc_text.pack(fill="x", padx=20, pady=5)

        # Category
        tk.Label(self.right_panel, text="Category", fg="white", bg="#0f3b66").pack(anchor="w", padx=20, pady=(10, 0))
        self.category_box = ttk.Combobox(self.right_panel, values=["Personal", "Work", "Study", "Health"])
        self.category_box.current(0)
        self.category_box.pack(fill="x", padx=20, pady=5)

        # Save Button
        save_btn = tk.Button(
            self.right_panel,
            text="Save",
            font=("Arial", 12),
            bg="white",
            fg="#0f3b66",
            command=self.save_task
        )
        save_btn.pack(pady=20)

    # -------------------- Logic --------------------
    def show_add_panel(self):
        self.title_entry.focus()

    def save_task(self):
        title = self.title_entry.get()
        description = self.desc_text.get("1.0", tk.END).strip()
        category = self.category_box.get()

        if title == "":
            messagebox.showwarning("Warning", "Task Title is required!")
            return

        self.db.add_task(title, description, category)
        self.clear_form()
        self.load_tasks()

    def clear_form(self):
        self.title_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.category_box.current(0)

    def load_tasks(self):
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()

        tasks = self.db.get_tasks()

        if not tasks:
            self.empty_label = tk.Label(
                self.task_list_frame,
                text="Add First Task",
                font=("Arial", 14),
                fg="#9ecbff",
                bg="#0b2d4d"
            )
            self.empty_label.pack(pady=50)
            return

        for task in tasks:
            self.create_task_card(task)

    def create_task_card(self, task):
        card = tk.Frame(self.task_list_frame, bg="#12436f", padx=10, pady=8)
        card.pack(fill="x", padx=20, pady=6)

        title = tk.Label(card, text=task[1], font=("Arial", 12, "bold"), fg="white", bg="#12436f")
        title.pack(anchor="w")

        desc = tk.Label(card, text=task[2], font=("Arial", 10), fg="#cde7ff", bg="#12436f", wraplength=600, justify="left")
        desc.pack(anchor="w")

        meta = tk.Label(card, text=f"{task[3]} • {task[4]}", font=("Arial", 9), fg="#9ecbff", bg="#12436f")
        meta.pack(anchor="w")

# -------------------- Run App --------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()


