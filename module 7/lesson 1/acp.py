from tkinter import *

root = Tk()
root.title("Workshop Participant Greeting")
root.geometry("500x400")
root.configure(bg="lightblue")

# Title
Label(root, text="Workshop Participant Greeting",
      font=("Arial", 18, "bold"), bg="lightblue").pack(pady=15)

# Instructions
Label(root, text="Please enter your name below:",
      font=("Arial", 12), bg="lightblue").pack(pady=5)

# Name Entry
name_entry = Entry(root, width=30, font=("Arial", 12))
name_entry.pack(pady=10)


# Function for Check In button
def check_in():
    name = name_entry.get()

    output.delete("1.0", END)

    message = f"""Welcome to the Workshop, {name}!

We are happy to have you with us.

Workshop Date: August 12, 2026

Enjoy the workshop and have a great learning experience!"""

    output.insert(END, message)


# Check In Button
Button(root, text="Check In", font=("Arial", 12),
       command=check_in).pack(pady=10)


# Output Text Widget
output = Text(root, width=50, height=10,
              font=("Arial", 11))
output.pack(pady=10)

root.mainloop()