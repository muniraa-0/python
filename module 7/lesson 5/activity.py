from tkinter import *
from tkinter import messagebox

window = Tk()
window.title("denomination calculator")
window.geometry("600x400")
window.configure(bg="lightblue")

label1 = Label(window, text="hey user! welcome to the denomination calculator:", bg="lightblue", font=("Arial", 12, "bold"))
label1.place(relx=0.5, rely=0.08, anchor=CENTER)

def msg():
    msgbox = messagebox.showinfo(
        "Alert",
        "do you want to open the denomination calculator?"
    )

    if msgbox == "ok":
        topwin()

button1 = Button(window, text="let's get started", command=msg, bg="green", fg="white")
button1.place(x=250, y=360)

def topwin():
    top = Toplevel()
    top.title("denomination calculator")
    top.configure(bg="light grey")
    top.geometry("600x350+50+50")

    label1 = Label(top, text="enter the total amount:", bg="light grey", font=("Arial", 12, "bold"))
    entry = Entry(top)

    lbl = Label(
        top,
        text="Here are number of the notes of each denomination:",
        bg="light grey",
        font=("Arial", 12, "bold")
    )

    l1 = Label(top, text="1000:", bg="light grey", font=("Arial", 12, "bold"))
    l2 = Label(top, text = "500", bg="light grey", font=("Arial", 12, "bold"))
    l3 = Label(top, text="100", bg="light grey", font=("Arial", 12, "bold"))

    t1 = Entry(top)
    t2 = Entry(top)
    t3 = Entry(top)

    def calculator():
        try:
            amount = int(entry.get())

            note_1000 = amount // 1000
            amount %= 1000

            note_500 = amount // 500
            amount %= 500

            note_100 = amount // 100
            amount %= 100

            t1.delete(0, END)
            t2.delete(0, END)
            t3.delete(0, END)

            t1.insert(0, str(note_1000))
            t2.insert(0, str(note_500))
            t3.insert(0, str(note_100))

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer amount.")

    btn = Button(
        top,
        text="calculate",
        command=calculator, 
        bg="blue",
        fg="white"
    )

    label1.place(x=230, y=50)
    entry.place(x=200, y=80)
    btn.place(x=240, y=120)

    lbl.place(x=140, y=170)

    l1.place(x=180, y=200)
    l2.place(x=180, y=230)
    l3.place(x=180, y=260)

    t1.place(x=270, y=200)
    t2.place(x=270, y=230)  
    t3.place(x=270, y=260)

    window.mainloop()