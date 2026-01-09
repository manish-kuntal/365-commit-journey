import tkinter as tk
import math

root = tk.Tk()
root.title("Scientific Calculator")
root.geometry("360x520")
root.configure(bg="black")
root.resizable(False, False)

expression = ""

# ---------------- Display ----------------
display = tk.Entry(
    root,
    font=("Arial", 26),
    bg="black",
    fg="white",
    bd=0,
    justify="right"
)
display.pack(fill="both", padx=10, pady=15, ipady=15)

# ---------------- Functions ----------------
def press(value):
    global expression
    expression += str(value)
    display.delete(0, tk.END)
    display.insert(tk.END, expression)

def clear_all():
    global expression
    expression = ""
    display.delete(0, tk.END)

def calculate():
    global expression
    try:
        result = eval(expression)
        display.delete(0, tk.END)
        display.insert(tk.END, str(result))
        expression = str(result)
    except:
        display.delete(0, tk.END)
        display.insert(tk.END, "Error")
        expression = ""

def sin():
    global expression
    try:
        result = math.sin(math.radians(float(expression)))
        display.delete(0, tk.END)
        display.insert(tk.END, result)
        expression = str(result)
    except:
        display.insert(tk.END, "Error")

def cos():
    global expression
    try:
        result = math.cos(math.radians(float(expression)))
        display.delete(0, tk.END)
        display.insert(tk.END, result)
        expression = str(result)
    except:
        display.insert(tk.END, "Error")

def tan():
    global expression
    try:
        result = math.tan(math.radians(float(expression)))
        display.delete(0, tk.END)
        display.insert(tk.END, result)
        expression = str(result)
    except:
        display.insert(tk.END, "Error")

def log():
    global expression
    try:
        result = math.log10(float(expression))
        display.delete(0, tk.END)
        display.insert(tk.END, result)
        expression = str(result)
    except:
        display.insert(tk.END, "Error")

def sqrt():
    global expression
    try:
        result = math.sqrt(float(expression))
        display.delete(0, tk.END)
        display.insert(tk.END, result)
        expression = str(result)
    except:
        display.insert(tk.END, "Error")

# ---------------- Buttons ----------------
frame = tk.Frame(root, bg="black")
frame.pack(expand=True, fill="both")

buttons = [
    ("sin", sin), ("cos", cos), ("tan", tan), ("√", sqrt),
    ("7", lambda: press(7)), ("8", lambda: press(8)), ("9", lambda: press(9)), ("/", lambda: press("/")),
    ("4", lambda: press(4)), ("5", lambda: press(5)), ("6", lambda: press(6)), ("*", lambda: press("*")),
    ("1", lambda: press(1)), ("2", lambda: press(2)), ("3", lambda: press(3)), ("-", lambda: press("-")),
    ("0", lambda: press(0)), (".", lambda: press(".")), ("+", lambda: press("+")), ("=", calculate),
    ("log", log), ("π", lambda: press(math.pi)), ("^", lambda: press("**")), ("AC", clear_all)
]

row = col = 0
for text, cmd in buttons:
    btn = tk.Button(
        frame,
        text=text,
        command=cmd,
        font=("Arial", 14),
        bg="#333333" if text not in ["=", "AC"] else "#ff9500",
        fg="white",
        bd=0,
        width=6,
        height=2
    )
    btn.grid(row=row, column=col, padx=5, pady=5)
    col += 1
    if col == 4:
        col = 0
        row += 1

root.mainloop()