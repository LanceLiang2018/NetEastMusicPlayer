from tkinter import *
import time

root = Tk()
s = StringVar()
s.set(str(time.clock()))
Label(root, textvariable=s).grid()
def func():
    s.set(str(round(time.clock(), 2)))
    root.after(1, func)
root.after(1, func)
root.mainloop()
