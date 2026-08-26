from tkinter import *
from tkinter import messagebox

window = Tk()
window.title("Virus scanner")
window.geometry("300x200")

def msg():
    messagebox.showwarning("Alert","Stop! Virus detected!")

button = Button(window,text="Scan for virus", command=msg)
button.place(x=40,y=40)

window.mainloop()