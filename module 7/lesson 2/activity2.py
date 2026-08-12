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
    name = name_entr.get()
    greet = "Hello " +name+ "!"
    Message = "\nCongratulations! You have successfully signed up."
    textbox.insert(END,Message)

textbox = Text