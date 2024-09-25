from tkinter import *
from ctypes import windll

window = Tk()
bg = "#ffffff"
title_window = "Calculator"


class app:
    def __init__(self, main):
        self.main = main
        self.main.configure(bg=bg)
        self.main.overrideredirect(True)
        self.main.geometry('320x420+500+200')
        self.main.resizable(width=False, height=False)

        self.top_bar = Frame(main,bg=bg)
        self.top_bar.pack(fill=X)

        self.iconImg = PhotoImage(file='Calculator_App_1.png')
        self.iconImg = self.iconImg.subsample(2, 2)

        self.icon_space = Label(self.top_bar, image=self.iconImg, bg=bg)
        self.icon_space.pack(side="left", padx=1)

        self.title_txt = Label(self.top_bar, text=title_window, bg=bg)
        self.title_txt.pack(side="left", padx=1)

        self.close_btn = Button(self.top_bar,text=" × ", cursor="arrow", bg=bg, padx=8, pady=4, fg="black", highlightthickness=0, activebackground="red", activeforeground="white", bd=0, command=self.main.quit, font=('calibri', 13))
        self.close_btn.pack(side="right")

        #bottom_bar = Frame(main, bg=bg)
        #bottom_bar.pack()

        self.close_btn.bind('<Enter>', self.changex_on_hovering)
        self.close_btn.bind('<Leave>', self.returnx_to_normalstate)

        self.minim_btn = Button(self.top_bar, text=' 🗕 ', command=self.minimize_me,  bg='white', padx=6, pady=4, bd=0, fg='black', font=("calibri", 13), highlightthickness=0)
        self.minim_btn.pack(side="right")

        self.minim_btn.bind('<Enter>', self.changeminim_on_hovering)
        self.minim_btn.bind('<Leave>', self.returnminim_to_normalstate)

        self.top_bar.bind('<Button-1>', self.get_pos)
        self.title_txt.bind('<Button-1>', self.get_pos)

        self.main.bind("<FocusIn>", self.deminimize)
        self.main.after(10, self.set_appwindow)

    def minimize_me(self):
        self.main.attributes("-alpha", 0)  # so you can't see the window when is minimized

    def deminimize(self, event):
        self.main.focus()
        self.main.attributes("-alpha", 1)  # so you can see the window when is not minimized

    def changex_on_hovering(self, event):
        self.close_btn['bg'] = 'red'
        self.close_btn['fg'] = 'white'

    def returnx_to_normalstate(self, event):
        self.close_btn['bg'] = 'white'
        self.close_btn['fg'] = 'black'

    def changeminim_on_hovering(self, event):
        self.minim_btn['bg'] = 'gray'
        self.minim_btn['fg'] = 'white'

    def returnminim_to_normalstate(self, event):
        self.minim_btn['bg'] = 'white'
        self.minim_btn['fg'] = 'black'

    def get_pos(self, event):
        xwin = self.main.winfo_x()
        ywin = self.main.winfo_y()
        startx = event.x_root
        starty = event.y_root

        ywin = ywin - starty
        xwin = xwin - startx

        def move_window(event):
            self.main.geometry('+{0}+{1}'.format(event.x_root + xwin, event.y_root + ywin))

        #startx = event.x_root
        #starty = event.y_root

        self.top_bar.bind('<B1-Motion>', move_window)
        self.title_txt.bind('<B1-Motion>', move_window)

    def set_appwindow(self):  # to display the window icon on the taskbar,
        # even when using root.overrideredirect(True
        # Some WindowsOS styles, required for task bar integration
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080
        # Magic
        hwnd = windll.user32.GetParent(self.main.winfo_id())
        stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        stylew = stylew & ~WS_EX_TOOLWINDOW
        stylew = stylew | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)

        self.main.wm_withdraw()
        self.main.after(10, lambda: self.main.wm_deiconify())

execution = app(window)
#execution.top_bar.bind('<B1-Motion>', move_window)
#execution.title_txt.bind('<B1-Motion>', move_window)
window.mainloop()