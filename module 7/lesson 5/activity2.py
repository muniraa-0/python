from tkinter import * 
from tkinter import messagebox 

window = Tk() 
window.title("denomination calculator") 
window.geometry("600x400") 
window.configure(bg="lightblue") 

label1 = Label(window, text="hey user! welcome to the denomination calculator:", bg="lightblue", font=("Arial", 12, "bold")) 
label1.place(relx=0.5, rely=0.08, anchor=CENTER) 

def msg(): 
    msgbox = messagebox.showinfo("Alert", "do you want to open the denomination calculator?") 
    if msgbox == "ok": 
        topwin() 

button1 = Button(window, text="let's get started", command=msg, bg="green", fg="white") 
button1.place(x=250, y=360) 

def topwin(): 
    top = Toplevel() 
    top.title("denomination calculator") 
    top.configure(bg="light grey") 
    top.geometry("600x350+50+50") 
    
    # CRITICAL FIX: Added 'top' as the first argument to all widgets below
    label1 = Label(top, text="enter the total amount:", bg="light grey", font=("Arial", 12, "bold")) 
    entry = Entry(top) 
    
    lbl = Label(top, text="Here are number of the notes of each denomination:", bg="light grey", font=("Arial", 12, "bold")) 
    
    l1 = Label(top, text="1000:", bg="light grey", font=("Arial", 12, "bold")) 
    l2 = Label(top, text="500:", bg="light grey", font=("Arial", 12, "bold")) 
    l3 = Label(top, text="100:", bg="light grey", font=("Arial", 12, "bold")) 
    
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
            
            t1.delete(0, END) 
            t2.delete(0, END) 
            t3.delete(0, END) 
            
            t1.insert(0, str(note_1000)) 
            t2.insert(0, str(note_500)) 
            t2.insert(0, str(note_500)) 
            t3.insert(0, str(note_100)) 
        except ValueError: 
            messagebox.showerror("Invalid Input", "Please enter a valid integer amount.") 
            
    btn = Button(top, text="calculate", command=calculator, bg="blue", fg="white") 
    
    # Adjusted X coordinates to center everything beautifully inside the 600px width
    label1.place(x=210, y=30) 
    entry.place(x=235, y=60) 
    btn.place(x=260, y=100) 
    lbl.place(x=100, y=150) 
    
    l1.place(x=200, y=190) 
    l2.place(x=200, y=220) 
    l3.place(x=200, y=250) 
    
    t1.place(x=270, y=190) 
    t2.place(x=270, y=220) 
    t3.place(x=270, y=250) 

window.mainloop()