import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import datetime

try:
    from tkcalendar import DateEntry
    _HAS_TKCAL = True
except Exception:
    DateEntry = None
    _HAS_TKCAL = False

DB_PATH = os.path.join(os.path.dirname(__file__), "tasks.db")


class Task:
    def __init__(self, id_, title, details, category, due_date, repeat, finished, created_at):
        self.id = id_
        self.title = title
        self.details = details
        self.category = category
        self.due_date = due_date
        self.repeat = repeat
        self.finished = bool(finished)
        self.created_at = created_at


class DB:
    def __init__(self, path=DB_PATH):
        self.conn = sqlite3.connect(path)
        self._init()

    def _init(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                details TEXT,
                category TEXT,
                due_date TEXT,
                repeat TEXT,
                finished INTEGER DEFAULT 0,
                created_at TEXT
            )
        """)
        self.conn.commit()

    def add_task(self, title, details, category, due_date, repeat=""):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO tasks (title, details, category, due_date, repeat, finished, created_at) VALUES (?,?,?,?,?,?,?)",
            (title, details, category, due_date, repeat, 0, datetime.datetime.utcnow().isoformat()),
        )
        self.conn.commit()

    def update_task(self, id_, **kwargs):
        keys = [f"{k}=?" for k in kwargs]
        vals = list(kwargs.values()) + [id_]
        cur = self.conn.cursor()
        cur.execute(f"UPDATE tasks SET {', '.join(keys)} WHERE id=?", vals)
        self.conn.commit()

    def delete_task(self, id_):
        self.conn.execute("DELETE FROM tasks WHERE id=?", (id_,))
        self.conn.commit()

    def list_tasks(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id, title, details, category, due_date, repeat, finished, created_at
            FROM tasks
            ORDER BY finished, created_at DESC
        """)
        return [Task(*r) for r in cur.fetchall()]


class TaskDialog(tk.Toplevel):
    def __init__(self, master, db, callback):
        super().__init__(master)
        self.db = db
        self.callback = callback
        self.configure(bg=master.bg)
        self.geometry("400x420")
        self.title("Add Task")
        self.grab_set()
        self._build()

    def _build(self):
        pad = {'padx': 20, 'pady': 10}

        tk.Label(self, text="Task Title", fg="white", bg=self.master.bg).pack(anchor='w', **pad)
        self.title_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.title_var).pack(fill='x', padx=20)

        tk.Label(self, text="Description", fg="white", bg=self.master.bg).pack(anchor='w', **pad)
        self.desc = tk.Text(self, height=4, bg="#062A3D", fg="white")
        self.desc.pack(fill='x', padx=20)

        tk.Label(self, text="Category", fg="white", bg=self.master.bg).pack(anchor='w', **pad)
        self.cat = tk.StringVar(value="Personal")
        ttk.Combobox(self, textvariable=self.cat,
                     values=["Personal", "Work", "Shopping"], state="readonly").pack(fill='x', padx=20)

        ttk.Button(self, text="Save", command=self._save).pack(pady=20)

    def _save(self):
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("Error", "Title required")
            return
        self.db.add_task(title, self.desc.get("1.0", "end").strip(), self.cat.get(), "")
        self.callback()
        self.destroy()


class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("To-Do | Day 2")
        self.geometry("500x700")
        self.bg = "#0D3B66"
        self.card_bg = "#164A7A"
        self.fg = "white"
        self.configure(bg=self.bg)

        self.db = DB()
        self.filter = "All"
        self._ui()
        self._load_tasks()

    def _ui(self):
        header = tk.Label(self, text="My Tasks", bg=self.bg, fg=self.fg,
                          font=("Arial", 22, "bold"))
        header.pack(pady=20)

        self.canvas = tk.Canvas(self, bg=self.bg, highlightthickness=0)
        self.scroll = tk.Frame(self.canvas, bg=self.bg)
        self.canvas.create_window((0, 0), window=self.scroll, anchor="nw")
        self.scroll.bind("<Configure>",
                         lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.pack(fill="both", expand=True)

        self.fab = tk.Button(self, text="+", font=("Arial", 24),
                             bg="#11A3A3", fg="white", bd=0,
                             command=self._add)
        self.fab.place(relx=0.85, rely=0.9, anchor="center")

    def _add(self):
        TaskDialog(self, self.db, self._load_tasks)

    def _load_tasks(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        tasks = [t for t in self.db.list_tasks() if not t.finished]

        if not tasks:
            tk.Label(self.scroll, text="Add First Task",
                     bg=self.bg, fg="#AFC5D9",
                     font=("Arial", 14)).pack(pady=100)
            return

        for t in tasks:
            card = tk.Frame(self.scroll, bg=self.card_bg, padx=15, pady=10)
            card.pack(fill="x", pady=6, padx=20)

            tk.Label(card, text=t.title, fg="white",
                     bg=self.card_bg, font=("Arial", 12, "bold")).pack(side="left")

            tk.Button(card, text="Delete", bg="red", fg="white",
                      bd=0, command=lambda tid=t.id: self._delete(tid)).pack(side="right")

    def _delete(self, tid):
        self.db.delete_task(tid)
        self._load_tasks()


if __name__ == "__main__":
    TodoApp().mainloop()
