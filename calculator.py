
import tkinter as tk
import sympy

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")

        self.result_displayed = False
        self.equation = tk.StringVar()

        self.entry = tk.Entry(master, textvariable=self.equation, font=('Arial', 20), bd=10, insertwidth=2, width=20, borderwidth=4)
        self.entry.grid(row=0, column=0, columnspan=5)
        self.entry.bind("<KeyPress>", self.key_press)

        buttons = [
            '7', '8', '9', '/', 'C',
            '4', '5', '6', '*', 'x',
            '1', '2', '3', '-', 'Solve',
            '0', '.', '=', '+'
        ]

        row_val = 1
        col_val = 0
        for button in buttons:
            self.create_button(button, row_val, col_val)
            col_val += 1
            if col_val > 4:
                col_val = 0
                row_val += 1

    def create_button(self, text, row, col):
        if text == '=':
            btn = tk.Button(self.master, text=text, padx=20, pady=20, font=('Arial', 18), command=self.calculate)
        elif text == 'C':
            btn = tk.Button(self.master, text=text, padx=20, pady=20, font=('Arial', 18), command=self.clear)
        elif text == 'Solve':
            btn = tk.Button(self.master, text=text, padx=20, pady=20, font=('Arial', 18), command=self.solve_equation)
        else:
            btn = tk.Button(self.master, text=text, padx=20, pady=20, font=('Arial', 18), command=lambda t=text: self.click(t))
        
        btn.grid(row=row, column=col, sticky="nsew")

    def click(self, key):
        if self.result_displayed:
            self.clear()
            self.result_displayed = False
        
        current_text = self.equation.get()
        self.equation.set(current_text + str(key))

    def clear(self):
        self.equation.set("")

    def calculate(self):
        try:
            result = str(eval(self.equation.get()))
            self.equation.set(result)
            self.result_displayed = True
        except:
            self.equation.set("Error")
            self.result_displayed = True

    def solve_equation(self):
        try:
            expr_str = self.equation.get()
            x = sympy.symbols('x')
            # The expression is assumed to be equal to 0
            solution = sympy.solveset(expr_str, x)
            # FiniteSet returns a set, so we extract the elements
            solution_list = list(solution)
            if not solution_list:
                self.equation.set("No real solution")
            else:
                self.equation.set(f"x = {solution_list[0]}")
            self.result_displayed = True
        except Exception as e:
            self.equation.set("Invalid Equation")
            self.result_displayed = True

    def key_press(self, event):
        # Allow digits, operators, and 'x' for equations
        if event.char.isdigit() or event.char in ['+', '-', '*', '/', '.', 'x']:
            if self.result_displayed:
                self.clear()
                self.result_displayed = False
        elif event.keysym == "Return":
            # Decide whether to calculate or solve based on content
            if 'x' in self.equation.get():
                self.solve_equation()
            else:
                self.calculate()
        elif event.keysym == "Escape":
            self.clear()

if __name__ == '__main__':
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
