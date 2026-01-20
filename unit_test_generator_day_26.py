import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

# ---------------- Question Bank ---------------- #
QUESTION_BANK = {
    "Math": [
        ("2 + 5 = ?", ["5", "7", "9", "10"], "7"),
        ("10 × 4 = ?", ["20", "40", "14", "30"], "40"),
        ("Square of 6 ?", ["12", "18", "36", "30"], "36"),
        ("Prime number ?", ["4", "6", "9", "7"], "7"),
        ("15 ÷ 3 = ?", ["3", "5", "6", "4"], "5"),
    ],
    "Python": [
        ("Which keyword is used for function?", ["def", "fun", "define", "function"], "def"),
        ("List is mutable?", ["Yes", "No", "Sometimes", "Never"], "Yes"),
        ("Correct file extension?", [".py", ".pt", ".pyt", ".python"], ".py"),
        ("Which loop is infinite?", ["for", "while", "do", "if"], "while"),
        ("Output of len('Hi')?", ["1", "2", "3", "0"], "2"),
    ]
}

# ---------------- Main App ---------------- #
class UnitTestGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Unit Test Generator")
        self.root.geometry("750x500")
        self.root.configure(bg="#0f172a")

        self.questions = []
        self.index = 0
        self.score = 0
        self.start_time = None

        self.create_ui()

    def create_ui(self):
        title = tk.Label(
            self.root,
            text="📝 Unit Test Generator",
            font=("Segoe UI", 20, "bold"),
            bg="#0f172a",
            fg="white"
        )
        title.pack(pady=10)

        frame = tk.Frame(self.root, bg="#1e293b", padx=20, pady=20)
        frame.pack(pady=10)

        # Subject selection
        tk.Label(frame, text="Select Subject:", bg="#1e293b", fg="white").grid(row=0, column=0)
        self.subject_var = tk.StringVar(value="Math")
        ttk.Combobox(
            frame,
            textvariable=self.subject_var,
            values=list(QUESTION_BANK.keys()),
            state="readonly",
            width=20
        ).grid(row=0, column=1)

        ttk.Button(frame, text="Start Test", command=self.start_test).grid(row=0, column=2, padx=10)

        # Question
        self.question_label = tk.Label(
            self.root,
            text="Click 'Start Test'",
            font=("Segoe UI", 14),
            bg="#0f172a",
            fg="cyan",
            wraplength=600
        )
        self.question_label.pack(pady=20)

        # Options
        self.option_var = tk.StringVar()
        self.options_frame = tk.Frame(self.root, bg="#0f172a")
        self.options_frame.pack()

        self.radio_buttons = []
        for _ in range(4):
            rb = ttk.Radiobutton(self.options_frame, text="", variable=self.option_var, value="")
            rb.pack(anchor="w", pady=2)
            self.radio_buttons.append(rb)

        ttk.Button(self.root, text="Next", command=self.next_question).pack(pady=10)

        self.status_label = tk.Label(
            self.root,
            text="Score: 0",
            bg="#0f172a",
            fg="white"
        )
        self.status_label.pack()

    def start_test(self):
        subject = self.subject_var.get()
        self.questions = random.sample(QUESTION_BANK[subject], k=5)
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

    def next_question(self):
        _, _, correct = self.questions[self.index]

        if self.option_var.get() == correct:
            self.score += 1

        self.index += 1

        if self.index < len(self.questions):
            self.load_question()
            self.status_label.config(text=f"Score: {self.score}")
        else:
            self.show_result()

    def show_result(self):
        time_taken = int(time.time() - self.start_time)
        messagebox.showinfo(
            "Result",
            f"Test Completed!\n\nScore: {self.score}/5\nTime Taken: {time_taken} sec"
        )
        self.question_label.config(text="Test Finished")
        self.status_label.config(text="")

# ---------------- Run App ---------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = UnitTestGenerator(root)
    root.mainloop()
