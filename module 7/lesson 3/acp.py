import tkinter as tk
from tkinter import messagebox

class AfterSchoolRoutineChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("After-School Routine Checker")
        self.root.geometry("520x420")
        self.root.configure(bg="#f0f4f8")
        self.root.resizable(False, False)

        # Sample after-school routine
        self.routine = [
            "Do homework",
            "Have a snack",
            "Practice coding",
            "Read a book",
            "Help with chores",
            "Free time / play"
        ]
        self.current_index = 0

        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="After-School Routine Checker",
            font=("Arial", 18, "bold"),
            bg="#f0f4f8",
            fg="#1a365d"
        )
        title.pack(pady=(20, 10))

        # Instruction
        instruction = tk.Label(
            self.root,
            text="Type a task below, then press Enter or click the button",
            font=("Arial", 10),
            bg="#f0f4f8",
            fg="#4a5568"
        )
        instruction.pack()

        # Task Entry
        self.task_entry = tk.Entry(
            self.root,
            font=("Arial", 12),
            width=35,
            relief="solid",
            bd=1
        )
        self.task_entry.pack(pady=12)
        self.task_entry.focus()

        # Bind key press → show last character typed
        self.task_entry.bind("<KeyRelease>", self.show_last_character)

        # Button to check task
        check_btn = tk.Button(
            self.root,
            text="Check Task",
            font=("Arial", 11, "bold"),
            bg="#3182ce",
            fg="white",
            activebackground="#2b6cb0",
            relief="flat",
            padx=20,
            pady=6,
            cursor="hand2",
            command=self.check_task
        )
        check_btn.pack(pady=5)

        # Also allow pressing Enter
        self.task_entry.bind("<Return>", lambda e: self.check_task())

        # Last character display
        self.last_char_label = tk.Label(
            self.root,
            text="Last character typed: -",
            font=("Arial", 10),
            bg="#f0f4f8",
            fg="#2d3748"
        )
        self.last_char_label.pack(pady=(15, 5))

        # Routine display area (clickable)
        self.routine_frame = tk.Frame(
            self.root,
            bg="#e2e8f0",
            relief="solid",
            bd=1,
            cursor="hand2"
        )
        self.routine_frame.pack(pady=15, padx=30, fill="x")

        self.routine_label = tk.Label(
            self.routine_frame,
            text=f"Current Task: {self.routine[self.current_index]}",
            font=("Arial", 12, "bold"),
            bg="#e2e8f0",
            fg="#2b6cb0",
            pady=15
        )
        self.routine_label.pack()

        # Bind mouse click on the routine area
        self.routine_frame.bind("<Button-1>", self.on_routine_click)
        self.routine_label.bind("<Button-1>", self.on_routine_click)

        # Status / next task message
        self.status_label = tk.Label(
            self.root,
            text="Click the routine box to see the next task",
            font=("Arial", 10),
            bg="#f0f4f8",
            fg="#718096"
        )
        self.status_label.pack(pady=5)

    def show_last_character(self, event):
        """Display the last character the user typed"""
        text = self.task_entry.get()
        if text:
            last_char = text[-1]
            self.last_char_label.config(text=f"Last character typed: '{last_char}'")
        else:
            self.last_char_label.config(text="Last character typed: -")

    def check_task(self):
        """Check if a task was entered. Show warning if empty."""
        task = self.task_entry.get().strip()

        if not task:
            messagebox.showwarning("Warning", "No task entered!\nPlease type a task first.")
            return

        messagebox.showinfo("Task Received", f"You entered:\n\n{task}")
        self.task_entry.delete(0, tk.END)
        self.last_char_label.config(text="Last character typed: -")

    def on_routine_click(self, event):
        """React to mouse click on the routine area → show next task"""
        self.current_index = (self.current_index + 1) % len(self.routine)
        next_task = self.routine[self.current_index]

        self.routine_label.config(text=f"Current Task: {next_task}")
        self.status_label.config(
            text=f"Next task loaded! ({self.current_index + 1}/{len(self.routine)})",
            fg="#38a169"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = AfterSchoolRoutineChecker(root)
    root.mainloop()