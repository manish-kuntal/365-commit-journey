import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ----------------- Core BMI Logic -----------------

def calculate_bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def bmi_tips(category):
    tips = {
        "Underweight": "Increase calorie intake, add protein, and consult a nutritionist.",
        "Normal": "Maintain balanced diet, regular exercise, and good sleep.",
        "Overweight": "Control portions, increase daily activity, and reduce sugar/fat.",
        "Obese": "Structured diet, consistent exercise, and medical guidance recommended."
    }
    return tips.get(category, "")

# ----------------- App Class -----------------

class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator App")
        self.root.geometry("700x520")
        self.history = []

        self.create_ui()
        self.apply_theme()

    # ----------------- UI Setup -----------------

    def create_ui(self):
        header = tk.Frame(self.root)
        header.pack(fill="x", pady=10)

        self.title_label = tk.Label(header, text="BMI Calculator", font=("Arial", 18, "bold"))
        self.title_label.pack(side="left", padx=10)

        # Main Frame
        main = tk.Frame(self.root)
        main.pack(pady=10)

        # Unit Selection
        tk.Label(main, text="Units:").grid(row=0, column=0, sticky="w", pady=5)
        self.unit_var = tk.StringVar(value="Metric")
        unit_combo = ttk.Combobox(main, textvariable=self.unit_var, values=["Metric", "Imperial"], state="readonly")
        unit_combo.grid(row=0, column=1, pady=5)
        unit_combo.bind("<<ComboboxSelected>>", self.on_unit_change)

        # Weight
        self.weight_label = tk.Label(main, text="Weight (kg):")
        self.weight_label.grid(row=1, column=0, sticky="w", pady=5)
        self.weight_entry = tk.Entry(main, width=25)
        self.weight_entry.grid(row=1, column=1, pady=5)

        # Height
        self.height_label = tk.Label(main, text="Height (m):")
        self.height_label.grid(row=2, column=0, sticky="w", pady=5)
        self.height_entry = tk.Entry(main, width=25)
        self.height_entry.grid(row=2, column=1, pady=5)

        # Optional Age & Gender
        tk.Label(main, text="Age (optional):").grid(row=3, column=0, sticky="w", pady=5)
        self.age_entry = tk.Entry(main, width=25)
        self.age_entry.grid(row=3, column=1, pady=5)

        tk.Label(main, text="Gender (optional):").grid(row=4, column=0, sticky="w", pady=5)
        self.gender_combo = ttk.Combobox(main, values=["Male", "Female", "Other"], state="readonly")
        self.gender_combo.grid(row=4, column=1, pady=5)

        # Result
        self.result_label = tk.Label(main, text="BMI: ", font=("Arial", 12, "bold"))
        self.result_label.grid(row=5, column=0, columnspan=2, pady=10)

        self.category_label = tk.Label(main, text="Category: ", font=("Arial", 12))
        self.category_label.grid(row=6, column=0, columnspan=2, pady=5)

        # Progress Bar
        self.progress = ttk.Progressbar(main, orient="horizontal", length=260, mode="determinate")
        self.progress.grid(row=7, column=0, columnspan=2, pady=10)

        # Tips
        self.tips_label = tk.Label(main, text="Tips: ", wraplength=500, justify="left")
        self.tips_label.grid(row=8, column=0, columnspan=2, pady=5)

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.calc_btn = tk.Button(btn_frame, text="Calculate", width=18, command=self.manual_calculate)
        self.calc_btn.pack(side="left", padx=5)

        self.clear_btn = tk.Button(btn_frame, text="Clear", width=18, command=self.clear_inputs)
        self.clear_btn.pack(side="left", padx=5)

        # History
        history_frame = tk.Frame(self.root)
        history_frame.pack(pady=10, fill="x")

        tk.Label(history_frame, text="Last BMI Records:").pack(anchor="w", padx=10)
        self.history_box = tk.Listbox(history_frame, height=7)
        self.history_box.pack(fill="x", padx=10)

        # Real-time Calculation
        self.weight_entry.bind("<KeyRelease>", self.auto_calculate)
        self.height_entry.bind("<KeyRelease>", self.auto_calculate)

    # ----------------- Unit Handling -----------------

    def on_unit_change(self, event=None):
        unit = self.unit_var.get()
        if unit == "Metric":
            self.weight_label.config(text="Weight (kg):")
            self.height_label.config(text="Height (m):")
        else:
            self.weight_label.config(text="Weight (pounds):")
            self.height_label.config(text="Height (inches):")
        self.clear_inputs()

    # ----------------- Validation -----------------

    def validate_inputs(self):
        try:
            w = float(self.weight_entry.get())
            h = float(self.height_entry.get())
            if w <= 0 or h <= 0:
                raise ValueError
            return w, h
        except:
            raise ValueError("Please enter valid positive values for weight and height.")

    # ----------------- Calculation -----------------

    def manual_calculate(self):
        try:
            bmi, category = self.compute_bmi()
            self.update_ui(bmi, category)
            self.save_history(bmi, category)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def auto_calculate(self, event=None):
        try:
            if self.weight_entry.get().strip() == "" or self.height_entry.get().strip() == "":
                return
            bmi, category = self.compute_bmi()
            self.update_ui(bmi, category)
        except:
            pass

    def compute_bmi(self):
        w, h = self.validate_inputs()
        unit = self.unit_var.get()

        # Convert Imperial to Metric if needed
        if unit == "Imperial":
            # pounds to kg, inches to meters
            w = w * 0.453592
            h = h * 0.0254

        bmi = calculate_bmi(w, h)
        category = bmi_category(bmi)
        return round(bmi, 2), category

    # ----------------- UI Update -----------------

    def update_ui(self, bmi, category):
        self.result_label.config(text=f"BMI: {bmi}")
        self.category_label.config(text=f"Category: {category}")
        self.tips_label.config(text=f"Tips: {bmi_tips(category)}")

        # Progress bar (scale BMI 10 to 40)
        value = min(max((bmi - 10) * 3.33, 0), 100)
        self.progress["value"] = value

    # ----------------- History -----------------

    def save_history(self, bmi, category):
        entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | BMI: {bmi} | {category}"
        self.history.insert(0, entry)
        if len(self.history) > 15:
            self.history.pop()

        self.history_box.delete(0, tk.END)
        for item in self.history:
            self.history_box.insert(tk.END, item)

    # ----------------- Utilities -----------------

    def clear_inputs(self):
        self.weight_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.gender_combo.set("")
        self.result_label.config(text="BMI: ")
        self.category_label.config(text="Category: ")
        self.tips_label.config(text="Tips: ")
        self.progress["value"] = 0

    # ----------------- Black + Blue Theme -----------------

    def apply_theme(self):
        bg = "#020617"       # Black
        fg = "#e5e7eb"       # Light text
        accent = "#2563eb"   # Blue

        self.root.configure(bg=bg)
        for widget in self.root.winfo_children():
            self.apply_widget_theme(widget, bg, fg, accent)

    def apply_widget_theme(self, widget, bg, fg, accent):
        try:
            if isinstance(widget, tk.Button):
                widget.configure(bg=accent, fg="white",
                                 activebackground="#1d4ed8",
                                 activeforeground="white",
                                 borderwidth=0)
            elif isinstance(widget, tk.Entry):
                widget.configure(bg="#020617", fg=fg, insertbackground=fg)
            elif isinstance(widget, tk.Listbox):
                widget.configure(bg="#020617", fg=fg)
            else:
                widget.configure(bg=bg, fg=fg)
        except:
            pass

        for child in widget.winfo_children():
            self.apply_widget_theme(child, bg, fg, accent)


# ----------------- Main -----------------

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()
