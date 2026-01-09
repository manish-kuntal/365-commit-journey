import tkinter as tk
from tkinter import ttk

# ----------------- Conversion Logic -----------------

def convert_value(category, value, from_unit, to_unit):
    try:
        value = float(value)
    except:
        raise ValueError("Invalid number")

    # Length (base: meter)
    if category == "Length":
        units = {
            "Meter": 1,
            "Kilometer": 1000,
            "Centimeter": 0.01,
            "Inch": 0.0254,
            "Foot": 0.3048
        }
        return value * units[from_unit] / units[to_unit]

    # Weight (base: kilogram)
    elif category == "Weight":
        units = {
            "Kilogram": 1,
            "Gram": 0.001,
            "Pound": 0.453592,
            "Ton": 1000
        }
        return value * units[from_unit] / units[to_unit]

    # Time (base: second)
    elif category == "Time":
        units = {
            "Second": 1,
            "Minute": 60,
            "Hour": 3600,
            "Day": 86400
        }
        return value * units[from_unit] / units[to_unit]

    # Area (base: square meter)
    elif category == "Area":
        units = {
            "Square Meter": 1,
            "Square Kilometer": 1_000_000,
            "Acre": 4046.86,
            "Hectare": 10000
        }
        return value * units[from_unit] / units[to_unit]

    # Temperature
    elif category == "Temperature":
        if from_unit == "Celsius":
            if to_unit == "Fahrenheit":
                return (value * 9/5) + 32
            elif to_unit == "Kelvin":
                return value + 273.15
            else:
                return value

        elif from_unit == "Fahrenheit":
            if to_unit == "Celsius":
                return (value - 32) * 5/9
            elif to_unit == "Kelvin":
                return (value - 32) * 5/9 + 273.15
            else:
                return value

        elif from_unit == "Kelvin":
            if to_unit == "Celsius":
                return value - 273.15
            elif to_unit == "Fahrenheit":
                return (value - 273.15) * 9/5 + 32
            else:
                return value

    return None


# ----------------- UI Class -----------------

class UnitConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unit Converter App")
        self.root.geometry("540x430")
        self.theme = "blackblue"

        self.categories = {
            "Length": ["Meter", "Kilometer", "Centimeter", "Inch", "Foot"],
            "Weight": ["Kilogram", "Gram", "Pound", "Ton"],
            "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
            "Time": ["Second", "Minute", "Hour", "Day"],
            "Area": ["Square Meter", "Square Kilometer", "Acre", "Hectare"]
        }

        self.create_ui()
        self.apply_theme()

    # ----------------- UI Setup -----------------

    def create_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill="x", pady=10)

        self.title_label = tk.Label(top_frame, text="Unit Converter", font=("Arial", 18, "bold"))
        self.title_label.pack(side="left", padx=10)

        self.theme_btn = tk.Button(top_frame, text="Black–Blue Theme")
        self.theme_btn.pack(side="right", padx=10)

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.tabs = {}
        for category in self.categories:
            tab = tk.Frame(self.notebook)
            self.notebook.add(tab, text=category)
            self.tabs[category] = tab
            self.create_tab_content(tab, category)

    # ----------------- Tab Content -----------------

    def create_tab_content(self, parent, category):
        frame = tk.Frame(parent)
        frame.pack(pady=20)

        tk.Label(frame, text="Enter Value:").grid(row=0, column=0, pady=5, sticky="w")
        value_entry = tk.Entry(frame, width=25)
        value_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="From Unit:").grid(row=1, column=0, pady=5, sticky="w")
        from_unit = ttk.Combobox(frame, values=self.categories[category], state="readonly")
        from_unit.current(0)
        from_unit.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="To Unit:").grid(row=2, column=0, pady=5, sticky="w")
        to_unit = ttk.Combobox(frame, values=self.categories[category], state="readonly")
        to_unit.current(1)
        to_unit.grid(row=2, column=1, pady=5)

        result_label = tk.Label(frame, text="Result: ", font=("Arial", 12, "bold"))
        result_label.grid(row=3, column=0, columnspan=2, pady=10)

        # Real-time Conversion
        def auto_convert(event=None):
            try:
                result = convert_value(category, value_entry.get(), from_unit.get(), to_unit.get())
                result_label.config(text=f"Result: {round(result, 6)}")
            except:
                result_label.config(text="Result: Invalid Input")

        value_entry.bind("<KeyRelease>", auto_convert)
        from_unit.bind("<<ComboboxSelected>>", auto_convert)
        to_unit.bind("<<ComboboxSelected>>", auto_convert)

        # Preset Buttons
        preset_frame = tk.Frame(parent)
        preset_frame.pack(pady=5)

        presets = {
            "Length": [("km → m", "Kilometer", "Meter"), ("m → cm", "Meter", "Centimeter")],
            "Weight": [("kg → g", "Kilogram", "Gram"), ("pound → kg", "Pound", "Kilogram")],
            "Temperature": [("°C → °F", "Celsius", "Fahrenheit"), ("°F → °C", "Fahrenheit", "Celsius")],
            "Time": [("hr → sec", "Hour", "Second"), ("min → sec", "Minute", "Second")],
            "Area": [("acre → sq.m", "Acre", "Square Meter"), ("hectare → sq.m", "Hectare", "Square Meter")]
        }

        for text, f_unit, t_unit in presets[category]:
            btn = tk.Button(
                preset_frame,
                text=text,
                width=14,
                command=lambda fu=f_unit, tu=t_unit: self.set_preset(from_unit, to_unit, fu, tu)
            )
            btn.pack(side="left", padx=5)

    # ----------------- Preset Handler -----------------

    def set_preset(self, from_unit, to_unit, f, t):
        from_unit.set(f)
        to_unit.set(t)

    # ----------------- Black + Blue Theme -----------------

    def apply_theme(self):
        # Black + Blue professional colors
        bg = "#020617"       # Deep Black
        fg = "#e5e7eb"       # Light text
        accent = "#2563eb"   # Blue highlight

        self.root.configure(bg=bg)

        for widget in self.root.winfo_children():
            self.apply_widget_theme(widget, bg, fg, accent)

    def apply_widget_theme(self, widget, bg, fg, accent):
        try:
            if isinstance(widget, tk.Button):
                widget.configure(
                    bg=accent, fg="white",
                    activebackground="#1d4ed8",
                    activeforeground="white",
                    borderwidth=0
                )
            elif isinstance(widget, tk.Entry):
                widget.configure(bg="#020617", fg=fg, insertbackground=fg)
            else:
                widget.configure(bg=bg, fg=fg)
        except:
            pass

        for child in widget.winfo_children():
            self.apply_widget_theme(child, bg, fg, accent)


# ----------------- Main -----------------

if __name__ == "__main__":
    root = tk.Tk()
    app = UnitConverterApp(root)
    root.mainloop()

