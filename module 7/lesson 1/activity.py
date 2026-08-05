from tkinter import *
from datetime import date

window = Tk()

window.title("My First GUI")

window.geometry("400x300")

label1 = Label(text = "Hey There!", fg = "white",bg = "blue",height = 1,width = 300)
label1.pack()

label2 = Label(text = "Enter your name: ")
label2.pack()
entry1 = Entry()
entry1.pack()

def display():
    name = entry1.get()
    global message
    message = "Welcome to tkinter Application!\nToday's date is:"
    greet = "Hello, "+ name + "!"
    text_box.insert(END,greet)
    text_box.insert(END,"\n" + message)
    text_box.insert(END, date.today())

text_box = Text(window, height = 5, width = 50)

button1 = Button(text = "Begin", command = display)
button1.pack()
text_box.pack()

window.mainloop()
