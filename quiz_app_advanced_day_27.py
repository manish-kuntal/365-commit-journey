import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

# ---------------- QUESTION BANK ---------------- #
QUESTION_BANK = {
    "General": {
        "Easy": [
            ("Capital of India?", ["Delhi", "Mumbai", "Kolkata", "Chennai"], "Delhi"),
            ("2 + 2 = ?", ["3", "4", "5", "6"], "4"),
        ],
        "Medium": [
            ("5 × 6 = ?", ["11", "25", "30", "20"], "30"),
            ("Square root of 81?", ["7", "8", "9", "10"], "9"),
        ],
        "Hard": [
            ("Prime number?", ["21", "39", "37", "51"], "37"),
            ("Value of π (approx)?", ["2.14", "3.14", "4.13", "1.34"], "3.14"),
        ]
    },
    "Python": {
        "Easy": [
            ("Keyword for function?", ["def", "fun", "define", "function"], "def"),
            ("Python file extension?", [".pt", ".pyt", ".py", ".python"], ".py"),
        ],
        "Medium": [
            ("Which is mutable?", ["tuple", "string", "list", "int"], "list"),
            ("Output of len('Hi')?", ["1", "2", "0", "3"], "2"),
        ],
        "Hard": [
            ("Which is not keyword?", ["lambda", "yield", "define", "global"], "define"),
            ("Type of (5)?", ["str", "float", "int", "bool"], "int"),
        ]
    }
}

# ---------------- MAIN APP ---------------- #
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("800x550")
        self.root.configure(bg="#0f172a")

        self.questions = []
        self.index = 0
        self.score = 0
        self.start_time = None

        self.create_ui()

    def create_ui(self):
        title = tk.Label(
            self.root,
            text="🧠 Quiz App",
            font=("Segoe UI", 20, "bold"),
            bg="#0f172a",
            fg="white"
        )
        title.pack(pady=10)

        frame = tk.Frame(self.root, bg="#1e293b", padx=20, pady=20)
        frame.pack(pady=10)

        # Category
        tk.Label(frame, text="Category:", bg="#1e293b", fg="white").grid(row=0, column=0)
        self.category_var = tk.StringVar(value="General")
        ttk.Combobox(
            frame,
            textvariable=self.category_var,
            values=list(QUESTION_BANK.keys()),
            state="readonly",
            width=20
        ).grid(row=0, column=1, padx=5)

        # Difficulty
        tk.Label(frame, text="Difficulty:", bg="#1e293b", fg="white").grid(row=0, column=2)
        self.diff_var = tk.StringVar(value="Easy")
        ttk.Combobox(
            frame,
            textvariable=self.diff_var,
            values=["Easy", "Medium", "Hard"],
            state="readonly",
            width=20
        ).grid(row=0, column=3, padx=5)

        ttk.Button(frame, text="Start Quiz", command=self.start_quiz).grid(row=0, column=4, padx=10)

        # Question
        self.question_label = tk.Label(
            self.root,
            text="Select category & difficulty, then start",
            font=("Segoe UI", 14),
            bg="#0f172a",
            fg="cyan",
            wraplength=650
        )
        self.question_label.pack(pady=20)

        # Options
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

        ttk.Button(self.root, text="Next", command=self.next_question).pack(pady=10)

        self.status_label = tk.Label(
            self.root,
            text="Score: 0 | Time: 0 sec",
            bg="#0f172a",
            fg="white"
        )
        self.status_label.pack()

    def start_quiz(self):
        category = self.category_var.get()
        difficulty = self.diff_var.get()

        self.questions = random.sample(
            QUESTION_BANK[category][difficulty],
            k=len(QUESTION_BANK[category][difficulty])
        )

        self.index = 0
        self.score = 0
        self.start_time = time.time()
        self.load_question()

    def load_question(self):
        q, options, _ = self.questions[self.index]
        self.question_label.config(text=f"Q{self.index+1}. {q}")
        self.option_var.set(None)

        for rb, opt in zip(self.radio_buttons, options):
            rb.config(text=opt, value=opt)

        self.update_time()

    def update_time(self):
        elapsed = int(time.time() - self.start_time)
        self.status_label.config(text=f"Score: {self.score} | Time: {elapsed} sec")

    def next_question(self):
        _, _, correct = self.questions[self.index]

        if self.option_var.get() == correct:
            self.score += 1

        self.index += 1

        if self.index < len(self.questions):
            self.load_question()
        else:
            self.show_result()

    def show_result(self):
        total = len(self.questions)
        accuracy = (self.score / total) * 100
        time_taken = int(time.time() - self.start_time)

        messagebox.showinfo(
            "Quiz Result",
            f"Quiz Completed 🎉\n\n"
            f"Score: {self.score}/{total}\n"
            f"Accuracy: {accuracy:.2f}%\n"
            f"Time Taken: {time_taken} sec"
        )

        self.question_label.config(text="Quiz Finished")
        self.status_label.config(text="")

# ---------------- RUN APP ---------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
