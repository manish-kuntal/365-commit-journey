import tkinter as tk
from tkinter import messagebox
import cmath

def solve():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        c = float(entry_c.get())
        d = float(entry_d.get())

        if a == 0:
            messagebox.showerror("Error", "a cannot be zero!")
            return

        p = (3*a*c - b*b) / (3*a*a)
        q = (2*b*b*b - 9*a*b*c + 27*a*a*d) / (27*a*a*a)
        delta = (q/2)**2 + (p/3)**3

        u = (-q/2 + cmath.sqrt(delta))**(1/3)
        v = (-q/2 - cmath.sqrt(delta))**(1/3)

        y1 = u + v
        y2 = -(u+v)/2 + (u-v)*cmath.sqrt(3)/2*1j
        y3 = -(u+v)/2 - (u-v)*cmath.sqrt(3)/2*1j

        x1 = y1 - b/(3*a)
        x2 = y2 - b/(3*a)
        x3 = y3 - b/(3*a)

        result.set(f"x1 = {x1}\n\nx2 = {x2}\n\nx3 = {x3}")

    except:
        messagebox.showerror("Error", "Enter valid numbers!")

# Window
root = tk.Tk()
root.title("Cubic Solver - Dark Blue")
root.geometry("420x360")
root.configure(bg="#0f172a")   # dark blue

tk.Label(root, text="ax³ + bx² + cx + d = 0",
         font=("Segoe UI", 14, "bold"),
         bg="#0f172a", fg="white").pack(pady=12)

frame = tk.Frame(root, bg="#0f172a")
frame.pack()

def styled_entry(row, text):
    tk.Label(frame, text=text, bg="#0f172a", fg="white").grid(row=row, column=0, pady=4)
    e = tk.Entry(frame, bg="#020617", fg="white", insertbackground="white",
                 relief="flat", width=18)
    e.grid(row=row, column=1, pady=4)
    return e

entry_a = styled_entry(0, "a")
entry_b = styled_entry(1, "b")
entry_c = styled_entry(2, "c")
entry_d = styled_entry(3, "d")

tk.Button(root, text="Solve",
          command=solve,
          bg="#2563eb", fg="white",
          font=("Segoe UI", 10, "bold"),
          relief="flat", width=15).pack(pady=12)

result = tk.StringVar()
tk.Label(root, textvariable=result,
         bg="#0f172a", fg="#93c5fd",
         font=("Consolas", 10), wraplength=380).pack(pady=8)

root.mainloop()


