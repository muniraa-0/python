import tkinter as tk
from tkinter import messagebox
import math
import random
import platform


# ============================================================
#                    CIVIC SHIELD
#          COMMUNITY IMPACT SYSTEM — GUI EDITION
# ============================================================


# -------------------- COLORS -------------------------------

BG = "#07111f"
PANEL = "#0c1b2a"
CARD = "#10263a"
CARD_HOVER = "#163653"
TEXT = "#e5edf5"
MUTED = "#7f96aa"
CYAN = "#35d6ff"
GREEN = "#35e08a"
RED = "#ff5c6c"
ORANGE = "#ffad42"
BLUE = "#4b8cff"


# -------------------- QUOTES -------------------------------

QUOTES = [
    '"Small actions can create big changes."',
    '"Technology becomes meaningful when it improves lives."',
    '"Together, we can solve problems that affect everyone."',
    '"Every community becomes stronger when people take action."',
    '"The future is built by the problems we choose to solve."',
]


# -------------------- MODULE DATA --------------------------

MODULES = [
    ("RAD", "ROAD SAFETY", "Speed Detection & Fine System", RED),
    ("SIG", "SMART TRAFFIC", "Adaptive Signal Management", ORANGE),
    ("MED", "BLOOD RESPONSE", "Emergency Donor Finder", "#e83e5b"),
    ("CLN", "CLEAN CITY", "Garbage Reporting System", GREEN),
    ("FOD", "FOOD RESCUE", "Food Redistribution Network", "#f57c36"),
    ("EDU", "EDUCATION", "Free Learning Resources", BLUE),
    ("WTR", "WATER PROTECTION", "Leak Detection System", CYAN),
]


# ============================================================
# SOUND
# ============================================================

def click_sound():
    try:
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(850, 40)
    except Exception:
        pass


def success_sound():
    try:
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(700, 60)
            winsound.Beep(1000, 80)
    except Exception:
        pass


def warning_sound():
    try:
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1000, 120)
            winsound.Beep(600, 150)
    except Exception:
        pass


# ============================================================
# MAIN APP
# ============================================================

class CivicShieldApp:

    def __init__(self, root):

        self.root = root

        self.root.title("CIVIC SHIELD")
        self.root.geometry("1200x760")
        self.root.minsize(950, 650)
        self.root.configure(bg=BG)

        self.quote_index = 0
        self.radar_angle = 0
        self.radar_running = True

        self.show_intro()


    # ========================================================
    # CLEAR SCREEN
    # ========================================================

    def clear_screen(self):

        self.radar_running = False

        for widget in self.root.winfo_children():
            widget.destroy()


    # ========================================================
    # INTRO SCREEN
    # ========================================================

    def show_intro(self):

        self.clear_screen()

        self.radar_running = True

        frame = tk.Frame(
            self.root,
            bg=BG
        )

        frame.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            frame,
            text="SECURE COMMUNITY SYSTEM // VERSION 2.0",
            font=("Consolas", 11, "bold"),
            bg=BG,
            fg=MUTED
        ).pack(pady=(30, 10))

        # Radar Canvas

        self.radar_canvas = tk.Canvas(
            frame,
            width=300,
            height=220,
            bg=BG,
            highlightthickness=0
        )

        self.radar_canvas.pack(pady=5)

        self.animate_radar()

        # Title

        tk.Label(
            frame,
            text="CIVIC SHIELD",
            font=("Arial", 38, "bold"),
            bg=BG,
            fg=TEXT
        ).pack()

        tk.Label(
            frame,
            text="COMMUNITY IMPACT CONTROL SYSTEM",
            font=("Consolas", 14, "bold"),
            bg=BG,
            fg=CYAN
        ).pack(pady=(5, 15))

        # Quote

        self.quote_label = tk.Label(
            frame,
            text=QUOTES[0],
            font=("Georgia", 14, "italic"),
            bg=BG,
            fg=MUTED,
            wraplength=750
        )

        self.quote_label.pack(pady=15)

        self.rotate_quotes()

        # Status

        tk.Label(
            frame,
            text="● 7 MODULES READY",
            font=("Consolas", 12, "bold"),
            bg=BG,
            fg=GREEN
        ).pack(pady=15)

        # Enter button

        button = tk.Button(
            frame,
            text="ENTER CIVIC NETWORK",
            font=("Consolas", 13, "bold"),
            bg="#126d98",
            fg="white",
            activebackground="#1b8ec4",
            activeforeground="white",
            bd=0,
            padx=40,
            pady=15,
            cursor="hand2",
            command=self.enter_dashboard
        )

        button.pack(pady=10)


    # ========================================================
    # RADAR ANIMATION
    # ========================================================

    def animate_radar(self):

        if not self.radar_running:
            return

        if not hasattr(self, "radar_canvas"):
            return

        try:

            c = self.radar_canvas

            if not c.winfo_exists():
                return

            c.delete("all")

            cx = 150
            cy = 105

            # Shield

            points = [
                cx, 10,
                cx + 85, 45,
                cx + 70, 140,
                cx, 200,
                cx - 70, 140,
                cx - 85, 45
            ]

            c.create_polygon(
                points,
                outline=CYAN,
                fill="#0b2030",
                width=3
            )

            # Radar circles

            for radius in (25, 50, 75):

                c.create_oval(
                    cx - radius,
                    cy - radius,
                    cx + radius,
                    cy + radius,
                    outline="#16445c"
                )

            # Cross lines

            c.create_line(
                cx - 75,
                cy,
                cx + 75,
                cy,
                fill="#16445c"
            )

            c.create_line(
                cx,
                cy - 75,
                cx,
                cy + 75,
                fill="#16445c"
            )

            # Rotating radar

            angle = math.radians(self.radar_angle)

            x = cx + math.cos(angle) * 75
            y = cy + math.sin(angle) * 75

            c.create_line(
                cx,
                cy,
                x,
                y,
                fill=GREEN,
                width=3
            )

            # Center point

            c.create_oval(
                cx - 5,
                cy - 5,
                cx + 5,
                cy + 5,
                fill=CYAN,
                outline=""
            )

            # Random radar dots

            for _ in range(3):

                a = random.uniform(0, math.pi * 2)
                r = random.uniform(20, 70)

                dx = cx + math.cos(a) * r
                dy = cy + math.sin(a) * r

                c.create_oval(
                    dx - 2,
                    dy - 2,
                    dx + 2,
                    dy + 2,
                    fill=GREEN,
                    outline=""
                )

            self.radar_angle += 7

            if self.radar_angle >= 360:
                self.radar_angle = 0

            self.root.after(
                50,
                self.animate_radar
            )

        except tk.TclError:
            return


    # ========================================================
    # QUOTE ROTATION
    # ========================================================

    def rotate_quotes(self):

        try:

            if not self.quote_label.winfo_exists():
                return

            self.quote_index += 1

            if self.quote_index >= len(QUOTES):
                self.quote_index = 0

            self.quote_label.config(
                text=QUOTES[self.quote_index]
            )

            self.root.after(
                4000,
                self.rotate_quotes
            )

        except tk.TclError:
            pass


    # ========================================================
    # ENTER DASHBOARD
    # ========================================================

    def enter_dashboard(self):

        click_sound()

        self.show_loading()


    # ========================================================
    # LOADING
    # ========================================================

    def show_loading(self):

        self.clear_screen()

        frame = tk.Frame(
            self.root,
            bg=BG
        )

        frame.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            frame,
            text="INITIALIZING CIVIC MODULES",
            font=("Consolas", 25, "bold"),
            bg=BG,
            fg=CYAN
        ).pack(pady=(250, 30))

        self.load_label = tk.Label(
            frame,
            text="LOADING 0%",
            font=("Consolas", 13),
            bg=BG,
            fg=MUTED
        )

        self.load_label.pack()

        self.progress_canvas = tk.Canvas(
            frame,
            width=500,
            height=25,
            bg=BG,
            highlightthickness=0
        )

        self.progress_canvas.pack(pady=20)

        self.load_value = 0

        self.loading_animation()


    def loading_animation(self):

        self.load_value += 2

        c = self.progress_canvas

        c.delete("all")

        c.create_rectangle(
            0,
            0,
            500,
            20,
            fill="#13293d",
            outline=""
        )

        width = 500 * self.load_value / 100

        c.create_rectangle(
            0,
            0,
            width,
            20,
            fill=GREEN,
            outline=""
        )

        self.load_label.config(
            text=f"LOADING {self.load_value}%"
        )

        if self.load_value < 100:

            self.root.after(
                25,
                self.loading_animation
            )

        else:

            success_sound()

            self.root.after(
                300,
                self.show_dashboard
            )


    # ========================================================
    # DASHBOARD
    # ========================================================

    def show_dashboard(self):

        self.clear_screen()

        main = tk.Frame(
            self.root,
            bg=BG
        )

        main.pack(
            fill="both",
            expand=True
        )

        # Header

        header = tk.Frame(
            main,
            bg="#0b1d2e",
            height=80
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        tk.Label(
            header,
            text="CIVIC SHIELD",
            font=("Arial", 25, "bold"),
            bg="#0b1d2e",
            fg=TEXT
        ).pack(
            side="left",
            padx=30,
            pady=20
        )

        tk.Label(
            header,
            text="● ALL SYSTEMS ONLINE",
            font=("Consolas", 11, "bold"),
            bg="#0b1d2e",
            fg=GREEN
        ).pack(
            side="right",
            padx=30
        )

        # Heading

        tk.Label(
            main,
            text="COMMUNITY PROTECTION MODULES",
            font=("Consolas", 19, "bold"),
            bg=BG,
            fg=CYAN
        ).pack(pady=(20, 3))

        tk.Label(
            main,
            text="Select a system to begin",
            font=("Arial", 12),
            bg=BG,
            fg=MUTED
        ).pack(pady=(0, 15))

        # Grid

        grid = tk.Frame(
            main,
            bg=BG
        )

        grid.pack(
            expand=True
        )

        for col in range(4):
            grid.grid_columnconfigure(
                col,
                weight=1
            )

        for i, module in enumerate(MODULES):

            row = i // 4
            col = i % 4

            self.create_card(
                grid,
                module,
                row,
                col
            )


    # ========================================================
    # MODULE CARD
    # ========================================================

    def create_card(
        self,
        parent,
        module,
        row,
        col
    ):

        icon, title, subtitle, color = module

        card = tk.Frame(
            parent,
            bg=CARD,
            width=220,
            height=175,
            cursor="hand2"
        )

        card.grid(
            row=row,
            column=col,
            padx=12,
            pady=12
        )

        card.grid_propagate(False)

        # Icon

        icon_label = tk.Label(
            card,
            text=icon,
            font=("Consolas", 16, "bold"),
            bg=color,
            fg="white",
            width=7,
            height=2
        )

        icon_label.pack(pady=(20, 10))

        title_label = tk.Label(
            card,
            text=title,
            font=("Consolas", 12, "bold"),
            bg=CARD,
            fg=TEXT
        )

        title_label.pack()

        sub_label = tk.Label(
            card,
            text=subtitle,
            font=("Arial", 10),
            bg=CARD,
            fg=MUTED
        )

        sub_label.pack(pady=5)

        open_label = tk.Label(
            card,
            text="OPEN MODULE  →",
            font=("Consolas", 9, "bold"),
            bg=CARD,
            fg=color
        )

        open_label.pack(pady=5)

        widgets = [
            card,
            icon_label,
            title_label,
            sub_label,
            open_label
        ]

        # Hover

        def enter(event):

            card.config(
                bg=CARD_HOVER
            )

            title_label.config(
                bg=CARD_HOVER
            )

            sub_label.config(
                bg=CARD_HOVER
            )

            open_label.config(
                bg=CARD_HOVER
            )


        def leave(event):

            card.config(
                bg=CARD
            )

            title_label.config(
                bg=CARD
            )

            sub_label.config(
                bg=CARD
            )

            open_label.config(
                bg=CARD
            )


        def open_card(event=None):

            click_sound()

            self.open_module(
                module
            )


        for widget in widgets:

            widget.bind(
                "<Enter>",
                enter
            )

            widget.bind(
                "<Leave>",
                leave
            )

            widget.bind(
                "<Button-1>",
                open_card
            )


    # ========================================================
    # OPEN MODULE
    # ========================================================

    def open_module(self, module):

        icon, title, subtitle, color = module

        if title == "ROAD SAFETY":
            self.speeding_module(title, color)

        elif title == "SMART TRAFFIC":
            self.traffic_module(title, color)

        elif title == "BLOOD RESPONSE":
            self.blood_module(title, color)

        elif title == "CLEAN CITY":
            self.garbage_module(title, color)

        elif title == "FOOD RESCUE":
            self.food_module(title, color)

        elif title == "EDUCATION":
            self.education_module(title, color)

        elif title == "WATER PROTECTION":
            self.water_module(title, color)


    # ========================================================
    # CREATE MODULE WINDOW
    # ========================================================

    def module_window(self, title, color):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            title
        )

        window.geometry(
            "650x550"
        )

        window.configure(
            bg=BG
        )

        tk.Label(
            window,
            text=title,
            font=("Consolas", 22, "bold"),
            bg=BG,
            fg=color
        ).pack(
            pady=25
        )

        return window


    # ========================================================
    # ROAD SAFETY
    # ========================================================

    def speeding_module(self, title, color):

        w = self.module_window(
            title,
            color
        )

        plate = tk.Entry(
            w,
            width=40,
            font=("Arial", 12)
        )

        plate.insert(
            0,
            "Vehicle plate"
        )

        plate.pack(
            pady=10
        )

        speed = tk.Entry(
            w,
            width=40,
            font=("Arial", 12)
        )

        speed.insert(
            0,
            "Vehicle speed"
        )

        speed.pack(
            pady=10
        )

        limit = tk.Entry(
            w,
            width=40,
            font=("Arial", 12)
        )

        limit.insert(
            0,
            "Speed limit"
        )

        limit.pack(
            pady=10
        )

        result = tk.Label(
            w,
            text="READY FOR SCAN",
            bg=BG,
            fg=MUTED,
            font=("Consolas", 12)
        )

        result.pack(
            pady=20
        )

        def scan():

            try:

                v = float(speed.get())
                l = float(limit.get())

                excess = v - l

                if excess <= 0:

                    result.config(
                        text="✓ VEHICLE CLEAR — WITHIN LIMIT",
                        fg=GREEN
                    )

                    success_sound()

                else:

                    fine = 500 + excess * 100

                    result.config(
                        text=(
                            f"⚠ SPEED VIOLATION\n"
                            f"EXCESS: {excess:.1f} km/h\n"
                            f"FINE: {fine:.0f} BDT"
                        ),
                        fg=RED
                    )

                    warning_sound()

            except ValueError:

                result.config(
                    text="ENTER VALID NUMBERS",
                    fg=ORANGE
                )

        tk.Button(
            w,
            text="SCAN VEHICLE",
            bg=color,
            fg="white",
            font=("Consolas", 11, "bold"),
            bd=0,
            padx=25,
            pady=10,
            command=scan
        ).pack()


    # ========================================================
    # SMART TRAFFIC
    # ========================================================

    def traffic_module(self, title, color):

        w = self.module_window(
            title,
            color
        )

        entries = {}

        for direction in [
            "North",
            "South",
            "East",
            "West"
        ]:

            tk.Label(
                w,
                text=f"{direction} vehicles:",
                bg=BG,
                fg=TEXT
            ).pack()

            entry = tk.Entry(
                w,
                width=25
            )

            entry.pack(
                pady=3
            )

            entries[direction] = entry

        result = tk.Label(
            w,
            text="",
            bg=BG,
            fg=TEXT,
            font=("Consolas", 11)
        )

        result.pack(
            pady=15
        )

        def optimize():

            try:

                data = {
                    d: int(e.get())
                    for d, e in entries.items()
                }

                total = sum(
                    data.values()
                )

                if total == 0:

                    result.config(
                        text="NO TRAFFIC DETECTED",
                        fg=GREEN
                    )

                    return

                output = ""

                for d, count in data.items():

                    seconds = max(
                        8,
                        round(count / total * 90)
                    )

                    output += (
                        f"{d}: {seconds}s GREEN\n"
                    )

                result.config(
                    text=output,
                    fg=GREEN
                )

                success_sound()

            except ValueError:

                result.config(
                    text="ENTER VALID NUMBERS",
                    fg=RED
                )

        tk.Button(
            w,
            text="OPTIMIZE SIGNAL",
            bg=color,
            fg="white",
            command=optimize
        ).pack()


    # ========================================================
    # BLOOD RESPONSE
    # ========================================================

    def blood_module(self, title, color):

        w = self.module_window(
            title,
            color
        )

        donors = {
            "O-": ["Ayesha Rahman"],
            "O+": ["Nusrat Jahan", "Imran Ali"],
            "A+": ["Tanvir Alam"],
            "B+": ["Farhana Kabir"],
            "AB+": ["Rafiq Islam"]
        }

        selected = tk.StringVar(
            value="O+"
        )

        tk.OptionMenu(
            w,
            selected,
            *[
                "O-", "O+",
                "A-", "A+",
                "B-", "B+",
                "AB-", "AB+"
            ]
        ).pack(
            pady=15
        )

        result = tk.Label(
            w,
            text="SELECT BLOOD TYPE",
            bg=BG,
            fg=MUTED,
            font=("Consolas", 12)
        )

        result.pack(
            pady=20
        )

        def search():

            blood = selected.get()

            found = donors.get(
                blood,
                []
            )

            if found:

                result.config(
                    text=(
                        f"DONORS FOUND\n\n"
                        + "\n".join(found)
                    ),
                    fg=GREEN
                )

                success_sound()

            else:

                result.config(
                    text="NO DONORS FOUND",
                    fg=ORANGE
                )

        tk.Button(
            w,
            text="SEARCH DONORS",
            bg=color,
            fg="white",
            command=search
        ).pack()


    # ========================================================
    # CLEAN CITY
    # ========================================================

    def garbage_module(self, title, color):

        w = self.module_window(
            title,
            color
        )

        tk.Label(
            w,
            text="Location:",
            bg=BG,
            fg=TEXT
        ).pack()

        location = tk.Entry(
            w,
            width=45
        )

        location.pack(
            pady=8
        )

        tk.Label(
            w,
            text="Problem description:",
            bg=BG,
            fg=TEXT
        ).pack()

        description = tk.Text(
            w,
            width=45,
            height=7
        )

        description.pack(
            pady=8
        )

        result = tk.Label(
            w,
            text="",
            bg=BG,
            fg=TEXT
        )

        result.pack(
            pady=15
        )

        def report():

            if not location.get().strip():

                result.config(
                    text="LOCATION REQUIRED",
                    fg=RED
                )

                return

            text = description.get(
                "1.0",
                "end"
            ).lower()

            priority = "LOW"

            if any(
                word in text
                for word in [
                    "hazard",
                    "medical",
                    "overflow"
                ]
            ):

                priority = "HIGH"

            elif any(
                word in text
                for word in [
                    "smell",
                    "blocked"
                ]
            ):

                priority = "MEDIUM"

            result.config(
                text=(
                    f"REPORT SENT\n"
                    f"PRIORITY: {priority}"
                ),
                fg=GREEN
            )

            success_sound()

        tk.Button(
            w,
            text="SEND REPORT",
            bg=color,
            fg="white",
            command=report
        ).pack()


    # ========================================================
    # FOOD RESCUE
    # ========================================================

    def food_module(self, title, color):

        w = self.module_window(
            title,
            color
        )

        fields = {}

        for label in [
            "Food item",
            "Donor name",
            "Hours remaining"
        ]:

            tk.Label(
                w,
                text=label,
                bg=BG,
                fg=TEXT
            ).pack()

            entry = tk.Entry(
                w,
                width=40
            )

            entry.pack(
                pady=5
            )

            fields[label] = entry

        result = tk.Label(
            w,
            text="",
            bg=BG,
            fg=TEXT
        )

        result.pack(
            pady=20
        )

        def publish():

            result.config(
                text=(
                    "✓ FOOD LISTING PUBLISHED\n"
                    "Available for community organizations."
                ),
                fg=GREEN
            )

            success_sound()

        tk.Button(
            w,
            text="PUBLISH LISTING",
            bg=color,
            fg="white",
            command=publish
        ).pack()


    # ========================================================
    # EDUCATION
    # ========================================================

    def education_module(self, title, color):

        w = self.module_window(
            title,
            color
        )

        resources = {
            "Programming": [
                "freeCodeCamp",
                "CS50"
            ],

            "Mathematics": [
                "Khan Academy",
                "OpenStax"
            ],

            "Science": [
                "MIT OpenCourseWare"
            ],

            "English": [
                "BBC Learning English",
                "British Council"
            ]
        }

        selected = tk.StringVar(
            value="Programming"
        )

        tk.OptionMenu(
            w,
            selected,
            *resources.keys()
        ).pack(
            pady=20
        )

        result = tk.Label(
            w,
            text="",
            bg=BG,
            fg=TEXT,
            font=("Consolas", 12)
        )

        result.pack(
            pady=20
        )

        def find():

            subject = selected.get()

            output = (
                f"FREE {subject.upper()} RESOURCES\n\n"
            )

            output += "\n".join(
                f"• {x}"
                for x in resources[subject]
            )

            result.config(
                text=output,
                fg=CYAN
            )

            success_sound()

        tk.Button(
            w,
            text="FIND RESOURCES",
            bg=color,
            fg="white",
            command=find
        ).pack()


    # ========================================================
    # WATER PROTECTION
    # ========================================================

    def water_module(self, title, color):

        w = self.module_window(
            title,
            color
        )

        fields = {}

        for label in [
            "Zone name",
            "Previous reading",
            "Current reading",
            "Hours elapsed"
        ]:

            tk.Label(
                w,
                text=label,
                bg=BG,
                fg=TEXT
            ).pack()

            entry = tk.Entry(
                w,
                width=40
            )

            entry.pack(
                pady=4
            )

            fields[label] = entry

        result = tk.Label(
            w,
            text="",
            bg=BG,
            fg=TEXT
        )

        result.pack(
            pady=15
        )

        def analyze():

            try:

                old = float(
                    fields["Previous reading"].get()
                )

                new = float(
                    fields["Current reading"].get()
                )

                hours = float(
                    fields["Hours elapsed"].get()
                )

                if new < old:

                    result.config(
                        text="INVALID METER READINGS",
                        fg=RED
                    )

                    return

                rate = (
                    new - old
                ) / hours

                if rate > 5:

                    result.config(
                        text=(
                            f"⚠ POSSIBLE LEAK\n"
                            f"FLOW: {rate:.2f} L/hour"
                        ),
                        fg=RED
                    )

                    warning_sound()

                else:

                    result.config(
                        text=(
                            f"✓ NORMAL FLOW\n"
                            f"FLOW: {rate:.2f} L/hour"
                        ),
                        fg=GREEN
                    )

                    success_sound()

            except ValueError:

                result.config(
                    text="ENTER VALID NUMBERS",
                    fg=ORANGE
                )

        tk.Button(
            w,
            text="RUN LEAK SCAN",
            bg=color,
            fg="white",
            command=analyze
        ).pack()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = CivicShieldApp(root)

    root.mainloop()