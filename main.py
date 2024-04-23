import os.path
import sys
import tkinter as tk
from time import sleep

txtFont = "Arial"
txtSize = 14
txtResSize = 24

LARGE_FONT_STYLE = (txtFont, 40, "bold")
SMALL_FONT_STYLE = (txtFont, 16)
DIGITS_FONT_STYLE = (txtFont, 24, "bold")
DEFAULT_FONT_STYLE = (txtFont, 20)

BACKGROUND_COLOR = "#171717"
PRESSED_BUTTON = "#272829"
TERTIARY_PRESSED = "#a40029"

SECONDARY_COLOR = "#1c1c1c"
TERTIARY_COLOR = "#DA0037"
TEXT_COLOR = "#EDEDED"
class Calculator:
    def __init__(self):
        self.expression = "0"

        self.digits = {
            7: (2, 0), 8: (2, 1), 9: (2, 2),
            4: (3, 0), 5: (3, 1), 6: (3, 2),
            1: (4, 0), 2: (4, 1), 3: (4, 2),
            0: (5, 1), '.': (5, 0),
            '-': (1, 3), '+': (2, 3), '×': (3, 3), '÷': (4, 3), '^': (1, 2),
            '(': (1, 0), ')': (1, 1)
        }
        self.operator_sym = "-+×÷^()."

        self.window = tk.Tk()
        self.window.geometry("320x420")
        self.window.resizable(0, 0)
        self.window.title("RED Calculator")
        self.iconPath = self.resource_path('Calculator_App.ico')
        self.window.iconbitmap(self.iconPath)

        for i in range(4):
            self.window.columnconfigure(i, weight=1)
        for i in range(5):
            self.window.rowconfigure(i, weight=1)

        self.label = self.create_display_labels()

        self.create_buttons()
        self.buttons_to_keyboard()

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def create_display_labels(self):
        '''
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')
        '''

        label = tk.Label(self.window, text=self.expression, anchor=tk.E, bg=BACKGROUND_COLOR,
                         fg=TEXT_COLOR, padx=15, font=LARGE_FONT_STYLE, width=320)
        #label.pack(expand=True, fill='both')
        label.grid(row=0, column=0, columnspan=4, sticky=tk.NSEW)

        return label

    def create_digits_and_operators(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.window, text=str(digit), bg=BACKGROUND_COLOR, activebackground=PRESSED_BUTTON, activeforeground=TEXT_COLOR, fg=TEXT_COLOR, font=DIGITS_FONT_STYLE,
                               borderwidth=0, command=lambda x=digit: self.add_to_expr(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

            if self.operator_sym.find(str(digit)) != -1:
                button = tk.Button(self.window, text=str(digit), bg=SECONDARY_COLOR, activebackground=PRESSED_BUTTON,
                                   activeforeground=TEXT_COLOR, fg=TEXT_COLOR, font=DIGITS_FONT_STYLE,
                                   borderwidth=0, command=lambda x=digit: self.add_to_expr(x))
                button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def create_clear_button(self):
        button = tk.Button(self.window, text="C", bg=SECONDARY_COLOR, activebackground=PRESSED_BUTTON, activeforeground=TEXT_COLOR, fg=TEXT_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=lambda: self.clear_txt())
        button.grid(row=5, column=2, sticky=tk.NSEW)

    def create_equals_button(self):
        button = tk.Button(self.window, text="=", bg=TERTIARY_COLOR, activebackground=TERTIARY_PRESSED, activeforeground=TEXT_COLOR, fg=TEXT_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=lambda: self.eval_expr())
        button.grid(row=5, column=3, sticky=tk.NSEW)

    def create_buttons(self):
        self.create_digits_and_operators()
        self.create_clear_button()
        self.create_equals_button()

    def buttons_to_keyboard(self):
        # Numbers
        self.window.bind('0', lambda event: self.press_btn('0'))
        self.window.bind('1', lambda event: self.press_btn('1'))
        self.window.bind('2', lambda event: self.press_btn('2'))
        self.window.bind('3', lambda event: self.press_btn('3'))
        self.window.bind('4', lambda event: self.press_btn('4'))
        self.window.bind('5', lambda event: self.press_btn('5'))
        self.window.bind('6', lambda event: self.press_btn('6'))
        self.window.bind('7', lambda event: self.press_btn('7'))
        self.window.bind('8', lambda event: self.press_btn('8'))
        self.window.bind('9', lambda event: self.press_btn('9'))

        #Operands
        self.window.bind('/', lambda event: self.press_btn('÷'))
        self.window.bind('*', lambda event: self.press_btn('×'))

        self.window.bind('-', lambda event: self.press_btn('-'))
        self.window.bind('+', lambda event: self.press_btn('+'))

        self.window.bind('^', lambda event: self.press_btn('^'))
        self.window.bind('.', lambda event: self.press_btn('.'))

        #Parantheses
        self.window.bind('(', lambda event: self.press_btn('('))
        self.window.bind(')', lambda event: self.press_btn(')'))

        #Others
        self.window.bind('=', lambda event: self.press_btn('='))
        self.window.bind('<Return>', lambda event: self.press_btn('='))
        self.window.bind('<BackSpace>', lambda event: self.press_btn('C'))

    def add_to_expr(self, symbol):
        operators = self.operator_sym + "^."
        digits = "0123456789"

        #Replace 0 with digits
        if(self.expression == '0' and digits.find(str(symbol)) != -1):
            self.expression = ""

        #Replace Error with digits and deactivate operators
        if(self.expression == 'Error' and digits.find(str(symbol)) != -1):
            self.expression = ""
        elif(self.expression == 'Error' and operators.find(str(symbol)) != -1):
            symbol = ''

        #Add to expression
        self.expression += str(symbol)

        #Check and fix extra parantheses
        if(self.expression.count(')') > self.expression.count('(')):
            self.expression = self.expression.replace(")", "", 1)

        if(self.expression.find("()") != -1):
            self.expression = self.expression.replace("()", "(0)")

        # Add a single operator of every kind
        for i in range(len(operators)):
            for j in range(len(operators)):
                self.expression = self.expression.replace(operators[i] + operators[j], operators[j])

        # Implicit multiplication
        for i in range(len(digits)):
            if(self.expression == "0("):
                self.expression = self.expression.replace("0(", "(")
            else:
                self.expression = self.expression.replace(digits[i] + "(", digits[i] + "×(")
        self.update_label()

    def update_label(self):
        self.label.config(text=self.expression[:10])

    def eval_expr(self):
        self.expression = self.expression.replace("^", "**")
        self.expression = self.expression.replace("÷", "/")
        self.expression = self.expression.replace("×", "*")
        try:
            self.expression = str(eval(self.expression))
        except:
            self.expression = "Error"
        self.update_label()

    def clear_txt(self):
        self.expression = "0"
        self.update_label()

    def press_btn(self, txt):
        for wgd in self.window.winfo_children():
            if wgd['text'] == txt and isinstance(wgd, tk.Label) == False:
                wgd.invoke()
                org_color = wgd.cget("background")
                wgd.config(relief="sunken")

                if org_color == TERTIARY_COLOR:
                    wgd.config(bg=TERTIARY_PRESSED)
                else:
                    wgd.config(bg=PRESSED_BUTTON)

                self.window.update_idletasks()
                sleep(0.1)
                wgd.config(relief="raised")
                wgd.config(bg=org_color)

    def run(self):
        self.window.mainloop()

if __name__ =="__main__":
    calc = Calculator()
    calc.run()