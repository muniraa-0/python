import tkinter as tk
from tkinter import ttk, messagebox

class RestaurantOrderManagement:
    def __init__(self,root):
        self.root=root
        self.root.title("Restaurant Order Management System")

        self.menu_items = {
            "FRIES MEAL": 2,
            "LUNCH MEAL": 5,
            "BURGER MEAL": 3,
            "PIZZA MEAL": 4,
            "CHEESE BURGER": 2.5,
            "DRINKS": 1
        }

        self.exchange_rates = 82

        self.setup_background(root)

        self.setup_background(root)

        frame = ttk.Frame(root)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        ttk.Label(
            frame,
            text="Restaurant Order Management System",
            font=("Arial", 16, "bold")
        ).grid(row=0, columnspan=3, padx=10, pady=10)

        self.menu_labels = []
        self.menu_entries = []

        for i, (item, price) in enumerate(self.menu_items.items(),start=1) :
           label = ttk.Label(
               frame,
               text=f'{item} (${price})',
                font=("Arial", 12)
           )
           label.grid(row=i, column=0, padx=10, pady=5,)
           self.menu_labels[item] = label

           quantitiyy_entry = ttk.Entry(frame, width=5)
           quantitiyy_entry.grid(row=i, column=1, padx=10, pady=5)
           self.menu_entries.append(quantitiyy_entry)

           self.currency_var = tk.StringVar()
           ttk.Label(
               frame,
               text="Currency:",
                font=("Arial", 12)
           ).grid(
               row=len(self.menu_items)+1,
               column=0,
                padx=10,
                pady=5
           )

           currency_dropdown = ttk.Combobox(
               frame,
               textvariable=self.currency_var,
               values=["USD", "BDT"],
               state="readonly",
               width=10
           )
           currency_dropdown.grid(
                row=len(self.menu_items)+1,
                column=1,
                padx=10,
                pady=5
            )
           currency_dropdown.current(0)
           self.currency_var.trace("w", self.update_menu_prices)

           order_button = ttk.Button(
                frame,
                text="Place Order",
                command=self.place_order
            )
