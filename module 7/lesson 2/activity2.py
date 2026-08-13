from tkinter import *

root = Tk()
root.title("Login app")
root.geometry("400x400")

frame = Frame(master=root,height=200,width=360,bg="#d0efff")
label1 = Label(master=frame,text="Username",bg="#1C82B4",fg= "white",width=12)
label2 = Label(master=frame,text="Email ID",bg="#1C82B4",fg= "white",width=12)
label3 = Label(master=frame,text="password",bg="#1C82B4",fg= "white",width=12)

name_entry = Entry(master=frame)
email_entry = Entry(master=frame)
password_entry = Entry(master=frame,show="*")

def display():
    name = name_entry.get()
    greet = "Hello " +name+ "!"
    Message = "\nCongratulations! You have successfully signed up."
    textbox.insert(END,greet)
    textbox.insert(END,message)

textbox = Text(master=root,bg="grey",fg="white")
btn = Button(text = "Create Account", command=display,bg="#B41C1C")

frame.place(x=20, y=0)
label1.place(x=20,y=20)
label2.place(x=20,y=80)
email_entry.place(x=150, y=20)
label3.place(x=20,y=140)
password_entry.place(x=150, y=140)
btn.place(x=130, y=210)
textbox.place(y=250)

root.mainloop()