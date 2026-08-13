from tkinter import *

root = Tk()
root.title("ATM PIN Setup")
root.geometry("400x400")
root.configure(bg="lightblue")

# Title
title = Label(root, text="ATM PIN Setup", font=("Arial", 20, "bold"),
              bg="lightblue")
title.pack(pady=15)

# Frame for account details
frame1 = Frame(root, bd=2, relief="sunken", padx=10, pady=10)
frame1.pack(pady=10)

Label(frame1, text="Account Holder Name:").grid(row=0, column=0, padx=5, pady=5)
name_entry = Entry(frame1)
name_entry.grid(row=0, column=1, padx=5, pady=5)

Label(frame1, text="Account Number:").grid(row=1, column=0, padx=5, pady=5)
account_entry = Entry(frame1)
account_entry.grid(row=1, column=1, padx=5, pady=5)


# Frame for PIN
frame2 = Frame(root, bd=2, relief="sunken", padx=10, pady=10)
frame2.pack(pady=10)

Label(frame2, text="Set PIN:").grid(row=0, column=0, padx=5, pady=5)
pin_entry = Entry(frame2, show="*")
pin_entry.grid(row=0, column=1, padx=5, pady=5)

Label(frame2, text="Confirm PIN:").grid(row=1, column=0, padx=5, pady=5)
confirm_pin_entry = Entry(frame2, show="*")
confirm_pin_entry.grid(row=1, column=1, padx=5, pady=5)


# Function to display details
def show_details():
    name = name_entry.get()
    account = account_entry.get()
    pin = pin_entry.get()
    confirm_pin = confirm_pin_entry.get()

    if pin == confirm_pin:
        result.config(text=f"Name: {name}\nAccount No: {account}\nPIN Set Successfully!")
    else:
        result.config(text="PIN does not match!")


# Button
submit_button = Button(root, text="Submit", command=show_details)
submit_button.pack(pady=10)

# Result
result = Label(root, text="", bg="lightblue", font=("Arial", 11))
result.pack(pady=10)

root.mainloop()