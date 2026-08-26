from tkinter import *

window = Tk()
window.title("Event handler")
window.geometry("200x200")

def handle_keypress(event):
    print(event.char)

window.bind("<Key>", handle_keypress)

def handle_click(event):
    print("\nButton is clicked")

button = Button(text="Click Me")
button.pack()

button.bind("<Button-1>", handle_click)

window.mainloop()