import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

class MathPracticeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Practice App")
        self.root.geometry("700x450")
        self.root.configure(bg="#0f172a")

        self.score = 0
        self.attempts = 0
        self.start_time = None
        self.correct_answer = None

        self.create_ui()

    def create_ui(self):
        title = tk.Label(
            self.root,
            text="🧮 Math Practice App",
            font=("Segoe UI", 20, "bold"),
            bg="#0f172a",
            fg="white"
        )
        title.pack(pady=10)

        frame = tk.Frame(self.root, bg="#1e293b", padx=20, pady=20)
        frame.pack(pady=10)

        # Topic
        tk.Label(frame, text="Topic:", bg="#1e293b", fg="white").grid(row=0, column=0, sticky="w")
        self.topic_var = tk.StringVar(value="Addition")
        topics = ["Addition", "Subtraction", "Multiplication", "Division"]
        ttk.Combobox(frame, textvariable=self.topic_var, values=topics, state="readonly").grid(row=0, column=1)

        # Difficulty
        tk.Label(frame, text="Difficulty:", bg="#1e293b", fg="white").grid(row=1, column=0, sticky="w")
        self.diff_var = tk.StringVar(value="Easy")
        ttk.Combobox(frame, textvariable=self.diff_var,
                     values=["Easy", "Medium", "Hard"], state="readonly").grid(row=1, column=1)

        # Question
        self.question_label = tk.Label(
            frame, text="Click Start to Begin",
            font=("Segoe UI", 14),
            bg="#1e293b", fg="cyan"
        )
        self.question_label.grid(row=2, column=0, columnspan=2, pady=15)

        # Answer
        self.answer_entry = ttk.Entry(frame)
        self.answer_entry.grid(row=3, column=0, columnspan=2, pady=5)

        # Buttons
        ttk.Button(frame, text="Start", command=self.start_practice).grid(row=4, column=0, pady=10)
        ttk.Button(frame, text="Submit", command=self.check_answer).grid(row=4, column=1, pady=10)

        # Stats
        self.stats_label = tk.Label(
            self.root,
            text="Score: 0 | Attempts: 0 | Accuracy: 0%",
            bg="#0f172a",
            fg="white"
        )
        self.stats_label.pack(pady=10)

    def generate_numbers(self):
        diff = self.diff_var.get()
        if diff == "Easy":
            return random.randint(1, 10), random.randint(1, 10)
        elif diff == "Medium":
            return random.randint(10, 50), random.randint(10, 50)
        else:
            return random.randint(50, 100), random.randint(50, 100)

    def start_practice(self):
        self.start_time = time.time()
        self.new_question()

    def new_question(self):
        a, b = self.generate_numbers()
        topic = self.topic_var.get()

        if topic == "Addition":
            self.correct_answer = a + b
            symbol = "+"
        elif topic == "Subtraction":
            self.correct_answer = a - b
            symbol = "-"
        elif topic == "Multiplication":
            self.correct_answer = a * b
            symbol = "×"
        else:
            b = b if b != 0 else 1
            self.correct_answer = round(a / b, 2)
            symbol = "÷"

        self.question_label.config(text=f"{a} {symbol} {b} = ?")
        self.answer_entry.delete(0, tk.END)

    def check_answer(self):
        try:
            user_answer = float(self.answer_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            return

        self.attempts += 1

        if round(user_answer, 2) == round(self.correct_answer, 2):
            self.score += 1
            messagebox.showinfo("Correct", "✅ Correct Answer!")
        else:
            messagebox.showinfo(
                "Wrong",
                f"❌ Wrong Answer\nCorrect Answer: {self.correct_answer}"
            )

        accuracy = (self.score / self.attempts) * 100
        self.stats_label.config(
            text=f"Score: {self.score} | Attempts: {self.attempts} | Accuracy: {accuracy:.2f}%"
        )

        self.new_question()


if __name__ == "__main__":
    root = tk.Tk()
    app = MathPracticeApp(root)
    root.mainloop()
