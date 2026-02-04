import tkinter as tk
from tkinter import ttk, messagebox
import random

# ---------------- MCQ DATABASE ---------------- #
MCQ_DB = {
    "Math": [
        {
            "q": "2 + 3 = ?",
            "options": ["4", "5", "6", "7"],
            "ans": "5",
            "exp": "2 + 3 = 5"
        },
        {
            "q": "Square of 8?",
            "options": ["16", "32", "64", "48"],
            "ans": "64",
            "exp": "8 × 8 = 64"
        },
        {
            "q": "Prime number?",
            "options": ["9", "21", "11", "15"],
            "ans": "11",
            "exp": "11 ke alawa koi factor nahi hota"
        }
    ],
    "Python": [
        {
            "q": "Which is mutable?",
            "options": ["tuple", "list", "string", "int"],
            "ans": "list",
            "exp": "List mutable hoti hai"
        },
        {
            "q": "Correct extension?",
            "options": [".pt", ".pyt", ".py", ".python"],
            "ans": ".py",
            "exp": "Python files .py hoti hain"
        },
        {
            "q": "Keyword for loop?",
            "options": ["repeat", "loop", "for", "iterate"],
            "ans": "for",
            "exp": "Python me loop ke liye 'for' use hota hai"
        }
    ]
}

# ---------------- MAIN APP ---------------- #
class MCQPracticeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MCQ Practice App")
        self.root.geometry("850x550")
        self.root.configure(bg="#0f172a")

        self.questions = []
        self.index = 0
        self.score = 0
        self.wrong = []
        self.bookmarks = []

        self.create_ui()

    def create_ui(self):
        title = tk.Label(
            self.root,
            text="📘 MCQ Practice App",
            font=("Segoe UI", 20, "bold"),
            bg="#0f172a",
            fg="white"
        )
        title.pack(pady=10)

        top = tk.Frame(self.root, bg="#1e293b", padx=20, pady=15)
        top.pack()

        tk.Label(top, text="Topic:", bg="#1e293b", fg="white").grid(row=0, column=0)
        self.topic_var = tk.StringVar(value="Math")
        ttk.Combobox(
            top,
            textvariable=self.topic_var,
            values=list(MCQ_DB.keys()),
            state="readonly",
            width=20
        ).grid(row=0, column=1, padx=5)

        ttk.Button(top, text="Start Practice", command=self.start).grid(row=0, column=2, padx=10)

        self.question_label = tk.Label(
            self.root,
            text="Select topic and start practice",
            font=("Segoe UI", 14),
            bg="#0f172a",
            fg="cyan",
            wraplength=700
        )
        self.question_label.pack(pady=20)

        self.option_var = tk.StringVar()
        self.options_frame = tk.Frame(self.root, bg="#0f172a")
        self.options_frame.pack()

        self.radio_buttons = []
        for _ in range(4):
            rb = ttk.Radiobutton(
                self.options_frame,
                text="",
                variable=self.option_var,
                value=""
            )
            rb.pack(anchor="w", pady=3)
            self.radio_buttons.append(rb)

        btns = tk.Frame(self.root, bg="#0f172a")
        btns.pack(pady=10)

        ttk.Button(btns, text="Submit", command=self.check).grid(row=0, column=0, padx=5)
        ttk.Button(btns, text="Bookmark", command=self.bookmark).grid(row=0, column=1, padx=5)
        ttk.Button(btns, text="Next", command=self.next).grid(row=0, column=2, padx=5)

        self.exp_label = tk.Label(
            self.root,
            text="",
            bg="#0f172a",
            fg="lightgreen",
            wraplength=700
        )
        self.exp_label.pack(pady=10)

        self.status = tk.Label(
            self.root,
            text="Score: 0 | Wrong: 0",
            bg="#0f172a",
            fg="white"
        )
        self.status.pack()

    def start(self):
        self.questions = random.sample(MCQ_DB[self.topic_var.get()],
                                       k=len(MCQ_DB[self.topic_var.get()]))
        self.index = 0
        self.score = 0
        self.wrong.clear()
        self.load()

    def load(self):
        q = self.questions[self.index]
        self.question_label.config(text=f"Q{self.index+1}. {q['q']}")
        self.option_var.set(None)
        self.exp_label.config(text="")

        for rb, opt in zip(self.radio_buttons, q["options"]):
            rb.config(text=opt, value=opt)

    def check(self):
        q = self.questions[self.index]
        if self.option_var.get() == q["ans"]:
            self.score += 1
            self.exp_label.config(text="✅ Correct! " + q["exp"])
        else:
            self.wrong.append(q["q"])
            self.exp_label.config(text=f"❌ Wrong! Correct: {q['ans']} | {q['exp']}")

        self.status.config(text=f"Score: {self.score} | Wrong: {len(self.wrong)}")

    def next(self):
        self.index += 1
        if self.index < len(self.questions):
            self.load()
        else:
            self.show_result()

    def bookmark(self):
        q = self.questions[self.index]["q"]
        if q not in self.bookmarks:
            self.bookmarks.append(q)
            messagebox.showinfo("Bookmarked", "Question bookmarked!")

    def show_result(self):
        total = len(self.questions)
        accuracy = (self.score / total) * 100

        messagebox.showinfo(
            "Practice Summary",
            f"Completed 🎉\n\n"
            f"Score: {self.score}/{total}\n"
            f"Accuracy: {accuracy:.2f}%\n"
            f"Wrong Questions: {len(self.wrong)}\n"
            f"Bookmarked: {len(self.bookmarks)}"
        )

# ---------------- RUN ---------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = MCQPracticeApp(root)
    root.mainloop()
