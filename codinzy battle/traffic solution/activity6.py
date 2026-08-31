# ==============================================================
# CIVIC SHIELD
# COMMUNITY PROBLEM -> SMART RESPONSE -> COMMUNITY IMPACT
# ==============================================================
#
# A polished Python/Tkinter prototype for demonstrating how
# technology can help solve practical community problems.
#
# MAIN FEATURES
# --------------------------------------------------------------
# 1. Beautiful animated introduction screen
# 2. Animated civic particles
# 3. Scrollable community-problem menu
# 4. Interactive solution modules
# 5. Realistic Traffic Response System for police officers
# 6. Incident priority calculation
# 7. Adaptive traffic-signal recommendation
# 8. Emergency vehicle priority mode
# 9. Traffic officer action checklist
# 10. Blood-response demonstration
# 11. Clean-city reporting system
# 12. Food-rescue matching
# 13. Education learning path
# 14. Water-leak analysis
# 15. Animated flower planter at the bottom
# 16. Judge-friendly explanations throughout the code
#
# IMPORTANT:
# --------------------------------------------------------------
# This is a demonstration/prototype.
# Traffic recommendations are simulated and should NOT be used
# as real-world law-enforcement or emergency-control commands.
# A real system would require certified hardware, legal approval,
# verified traffic data, cybersecurity, human supervision and
# integration with authorized government systems.
# ==============================================================


import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
import platform
import time


# ==============================================================
# COLOR PALETTE
# ==============================================================
# A centralized color palette makes the design easier to change.
# ==============================================================

BG = "#06111D"
BG2 = "#081A2A"
PANEL = "#0B1F30"
CARD = "#102B40"
CARD_HOVER = "#163A52"

WHITE = "#F4F8FB"
TEXT = "#E5F0F6"
MUTED = "#7F98AA"

CYAN = "#38D7FF"
GREEN = "#36E18A"
RED = "#FF6475"
ORANGE = "#FFB24A"
PURPLE = "#A887FF"
BLUE = "#4D91FF"

LINE = "#1C4057"


# ==============================================================
# BACKGROUND QUOTES
# ==============================================================
# These quotes reinforce the project's social-impact theme.
# ==============================================================

QUOTES = [
    "Technology is powerful when it makes everyday life safer.",
    "A better community begins with better solutions.",
    "The best technology solves problems people actually face.",
    "Small actions can create measurable community impact.",
    "Identify the problem. Understand the cause. Build the solution.",
    "Smart cities are built around people, not just technology."
]


# ==============================================================
# COMMUNITY PROBLEM DATABASE
# ==============================================================
# Each dictionary represents a complete civic problem module.
#
# The modular structure allows the project to grow later.
# ==============================================================

MODULES = [

    {
        "key": "traffic",
        "code": "TRF",
        "title": "SMART TRAFFIC",
        "short": "Assist officers in managing congestion",
        "color": ORANGE,
        "problem":
            "Traffic officers often have to make quick decisions "
            "while dealing with changing vehicle queues, crashes, "
            "road blocks and emergency vehicles.",
        "solution":
            "A decision-support dashboard can combine manually "
            "reported queue sizes, incidents and emergency status "
            "to suggest a practical traffic-control plan.",
        "benefit":
            "Officers receive a clear summary instead of manually "
            "calculating every lane and priority."
    },

    {
        "key": "road",
        "code": "RAD",
        "title": "ROAD SAFETY",
        "short": "Identify dangerous driving patterns",
        "color": RED,
        "problem":
            "Speeding and unsafe driving can increase crash risk, "
            "especially around schools, crossings and busy roads.",
        "solution":
            "A safety-analysis tool can compare observed speed "
            "against the configured road limit and produce a "
            "risk indicator.",
        "benefit":
            "Faster identification of potentially dangerous "
            "situations."
    },

    {
        "key": "blood",
        "code": "MED",
        "title": "BLOOD RESPONSE",
        "short": "Organize emergency donor requests",
        "color": RED,
        "problem":
            "Families can lose valuable time when searching for "
            "compatible blood donors during emergencies.",
        "solution":
            "A structured request system can organize blood group, "
            "urgency and donor-network information.",
        "benefit":
            "A clearer process for coordinating donor outreach."
    },

    {
        "key": "clean",
        "code": "CLN",
        "title": "CLEAN CITY",
        "short": "Report waste and drainage problems",
        "color": GREEN,
        "problem":
            "Overflowing waste bins and blocked drains can create "
            "environmental and public-health problems.",
        "solution":
            "Citizens can submit structured reports that are "
            "classified by urgency and given a tracking number.",
        "benefit":
            "More organized communication between citizens and "
            "city-service teams."
    },

    {
        "key": "food",
        "code": "FOD",
        "title": "FOOD RESCUE",
        "short": "Connect safe surplus food with organizations",
        "color": ORANGE,
        "problem":
            "Safe surplus food can be wasted while nearby "
            "organizations may need food.",
        "solution":
            "A food-rescue listing can record quantity, pickup "
            "time and basic safety information.",
        "benefit":
            "Less avoidable waste and better coordination."
    },

    {
        "key": "education",
        "code": "EDU",
        "title": "EDUCATION ACCESS",
        "short": "Create simple learning pathways",
        "color": BLUE,
        "problem":
            "Students may have motivation but lack an organized "
            "starting point for learning.",
        "solution":
            "The platform can generate a simple subject-based "
            "learning path and track completed topics.",
        "benefit":
            "A more structured and accessible learning experience."
    },

    {
        "key": "water",
        "code": "WTR",
        "title": "WATER PROTECTION",
        "short": "Detect unusual water consumption",
        "color": CYAN,
        "problem":
            "Leaks can waste significant amounts of water before "
            "they are discovered.",
        "solution":
            "A usage analyzer can compare meter readings and "
            "highlight unusual consumption rates.",
        "benefit":
            "Earlier investigation of possible leaks."
    }
]


# ==============================================================
# SIMPLE SOUND FEEDBACK
# ==============================================================
# Sound is optional. On Windows we use winsound.
# On other systems the program continues normally.
# ==============================================================

def beep(kind="click"):

    if platform.system() != "Windows":
        return

    try:

        import winsound

        if kind == "success":
            winsound.Beep(700, 50)
            winsound.Beep(950, 70)

        elif kind == "warning":
            winsound.Beep(900, 90)
            winsound.Beep(550, 120)

        else:
            winsound.Beep(850, 35)

    except Exception:
        pass


# ==============================================================
# MAIN APPLICATION
# ==============================================================

class CivicShield:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "CIVIC SHIELD // COMMUNITY IMPACT SYSTEM"
        )

        self.root.geometry("1280x820")
        self.root.minsize(1000, 680)

        self.root.configure(bg=BG)


        # ------------------------------------------------------
        # APPLICATION STATE
        # ------------------------------------------------------

        self.screen = None

        self.selected = 0

        self.actions = 0

        self.impact = 0

        self.achievements = set()

        self.quote_index = 0

        self.card_widgets = []

        self.intro_running = False

        self.particle_angle = 0


        # ------------------------------------------------------
        # STYLE FOR SCROLLBAR
        # ------------------------------------------------------

        self.style = ttk.Style()

        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.style.configure(
            "Vertical.TScrollbar",
            troughcolor="#071421",
            background="#27516A",
            bordercolor="#071421",
            arrowcolor="#9BB5C5"
        )


        # Start the application with the animated introduction.
        self.show_intro()


    # ==========================================================
    # CLEAR CURRENT SCREEN
    # ==========================================================

    def clear(self):

        if self.screen is not None:
            self.screen.destroy()

        self.screen = tk.Frame(
            self.root,
            bg=BG
        )

        self.screen.pack(
            fill="both",
            expand=True
        )


    # ==========================================================
    # RECORD USER ACTION
    # ==========================================================
    # The project uses gamification to show how engagement could
    # be measured in a future civic platform.
    # ==============================================================

    def add_action(self, points=50):

        self.actions += 1

        self.impact += points

        if self.actions >= 1:
            self.achievements.add("FIRST ACTION")

        if self.actions >= 5:
            self.achievements.add("COMMUNITY HELPER")

        if self.actions >= 10:
            self.achievements.add("CIVIC CHAMPION")


    # ==========================================================
    # REUSABLE BUTTON
    # ==========================================================

    def make_button(
        self,
        parent,
        text,
        command,
        color=CYAN,
        width=250
    ):

        button = tk.Button(
            parent,
            text=text,
            command=lambda: (
                beep(),
                command()
            ),
            bg=color,
            fg=WHITE,
            activebackground=color,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            font=("Consolas", 10, "bold"),
            cursor="hand2",
            padx=15,
            pady=9
        )

        button.config(width=max(10, width // 10))

        return button


    # ==========================================================
    # INTRO SCREEN
    # ==========================================================
    # The introduction is intentionally visual.
    #
    # The animation communicates that the system is "alive"
    # before the user enters the dashboard.
    # ==============================================================

    def show_intro(self):

        self.clear()

        self.intro_running = True

        # ------------------------------------------------------
        # TOP STATUS BAR
        # ------------------------------------------------------

        status = tk.Frame(
            self.screen,
            bg="#081A2A",
            height=42
        )

        status.pack(
            fill="x"
        )

        status.pack_propagate(False)


        tk.Label(
            status,
            text="● SYSTEM ONLINE",
            bg="#081A2A",
            fg=GREEN,
            font=("Consolas", 9, "bold")
        ).pack(
            side="left",
            padx=20
        )


        tk.Label(
            status,
            text="CIVIC TECHNOLOGY DEMONSTRATION",
            bg="#081A2A",
            fg=MUTED,
            font=("Consolas", 9)
        ).pack(
            side="right",
            padx=20
        )


        # ------------------------------------------------------
        # MAIN INTRO CANVAS
        # ------------------------------------------------------

        self.intro_canvas = tk.Canvas(
            self.screen,
            width=620,
            height=340,
            bg=BG,
            highlightthickness=0
        )

        self.intro_canvas.pack(
            pady=(15, 0)
        )


        # Start the animated shield.
        self.animate_intro()


        # ------------------------------------------------------
        # PROJECT TITLE
        # ------------------------------------------------------

        tk.Label(
            self.screen,
            text="CIVIC SHIELD",
            bg=BG,
            fg=TEXT,
            font=("Arial", 42, "bold")
        ).pack(
            pady=(0, 2)
        )


        tk.Label(
            self.screen,
            text="COMMUNITY PROBLEM → SMART RESPONSE → IMPACT",
            bg=BG,
            fg=CYAN,
            font=("Consolas", 11, "bold")
        ).pack()


        # ------------------------------------------------------
        # ROTATING QUOTE
        # ------------------------------------------------------

        self.quote_label = tk.Label(
            self.screen,
            text=QUOTES[0],
            bg=BG,
            fg=MUTED,
            font=("Georgia", 13, "italic"),
            wraplength=800
        )

        self.quote_label.pack(
            pady=18
        )


        # ------------------------------------------------------
        # FEATURE STRIP
        # ------------------------------------------------------

        feature = tk.Frame(
            self.screen,
            bg=BG
        )

        feature.pack(
            pady=5
        )


        features = [
            ("07", "CIVIC MODULES"),
            ("01", "SMART DASHBOARD"),
            ("∞", "COMMUNITY IMPACT")
        ]


        for number, title in features:

            f = tk.Frame(
                feature,
                bg=PANEL,
                width=190,
                height=70
            )

            f.pack(
                side="left",
                padx=6
            )

            f.pack_propagate(False)


            tk.Label(
                f,
                text=number,
                bg=PANEL,
                fg=CYAN,
                font=("Consolas", 18, "bold")
            ).pack(
                pady=(9, 0)
            )


            tk.Label(
                f,
                text=title,
                bg=PANEL,
                fg=MUTED,
                font=("Consolas", 7, "bold")
            ).pack()


        # ------------------------------------------------------
        # ENTER BUTTON
        # ------------------------------------------------------

        self.make_button(
            self.screen,
            "ENTER CIVIC NETWORK  →",
            self.show_dashboard,
            CYAN,
            300
        ).pack(
            pady=18
        )


        self.rotate_quote()


    # ==========================================================
    # ANIMATED INTRO SHIELD
    # ==========================================================
    # Canvas animation creates a shield without external images.
    # Small particles orbit the shield to represent information
    # flowing through a civic network.
    # ==============================================================

    def animate_intro(self):

        if not self.intro_running:
            return

        try:

            if not self.intro_canvas.winfo_exists():
                return

            canvas = self.intro_canvas

            canvas.delete("all")


            cx = 310
            cy = 170


            # --------------------------------------------------
            # SOFT RADAR CIRCLES
            # --------------------------------------------------

            for radius in (70, 105, 140):

                canvas.create_oval(
                    cx - radius,
                    cy - radius,
                    cx + radius,
                    cy + radius,
                    outline="#12364B"
                )


            # --------------------------------------------------
            # SHIELD SHAPE
            # --------------------------------------------------

            shield = [
                cx, 45,
                cx + 110, 90,
                cx + 88, 205,
                cx, 275,
                cx - 88, 205,
                cx - 110, 90
            ]


            canvas.create_polygon(
                shield,
                fill="#0A2233",
                outline=CYAN,
                width=3
            )


            # Inner shield.
            inner = [
                cx, 70,
                cx + 78, 103,
                cx + 61, 190,
                cx, 240,
                cx - 61, 190,
                cx - 78, 103
            ]


            canvas.create_polygon(
                inner,
                fill="#0C2A3D",
                outline="#23627D"
            )


            # --------------------------------------------------
            # SHIELD LETTERING
            # --------------------------------------------------

            canvas.create_text(
                cx,
                cy - 10,
                text="CS",
                fill=WHITE,
                font=("Arial", 38, "bold")
            )


            canvas.create_text(
                cx,
                cy + 35,
                text="COMMUNITY",
                fill=CYAN,
                font=("Consolas", 9, "bold")
            )


            # --------------------------------------------------
            # ORBITING PARTICLES
            # --------------------------------------------------

            for i in range(18):

                angle = (
                    self.particle_angle
                    + i * 20
                )

                radians = math.radians(angle)

                radius = 155 + (
                    i % 3
                ) * 12

                x = (
                    cx
                    + math.cos(radians)
                    * radius
                )

                y = (
                    cy
                    + math.sin(radians)
                    * radius
                    * 0.65
                )

                size = 3 if i % 2 else 5

                canvas.create_oval(
                    x - size,
                    y - size,
                    x + size,
                    y + size,
                    fill=CYAN if i % 2 else GREEN,
                    outline=""
                )


            self.particle_angle = (
                self.particle_angle + 2
            ) % 360


            self.root.after(
                35,
                self.animate_intro
            )

        except tk.TclError:
            pass


    # ==========================================================
    # ROTATING QUOTE
    # ==========================================================

    def rotate_quote(self):

        try:

            if (
                hasattr(self, "quote_label")
                and self.quote_label.winfo_exists()
            ):

                self.quote_index = (
                    self.quote_index + 1
                ) % len(QUOTES)


                self.quote_label.config(
                    text=QUOTES[
                        self.quote_index
                    ]
                )


                self.root.after(
                    4200,
                    self.rotate_quote
                )

        except tk.TclError:
            pass


    # ==========================================================
    # MAIN DASHBOARD
    # ==========================================================

    def show_dashboard(self):

        self.intro_running = False

        self.clear()

        self.card_widgets = []


        # ------------------------------------------------------
        # HEADER
        # ------------------------------------------------------

        header = tk.Frame(
            self.screen,
            bg="#081A2A",
            height=72
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)


        tk.Label(
            header,
            text="CIVIC SHIELD",
            bg="#081A2A",
            fg=TEXT,
            font=("Arial", 23, "bold")
        ).pack(
            side="left",
            padx=25
        )


        tk.Label(
            header,
            text="COMMUNITY COMMAND CENTER",
            bg="#081A2A",
            fg=CYAN,
            font=("Consolas", 9, "bold")
        ).pack(
            side="left"
        )


        # ------------------------------------------------------
        # LIVE SYSTEM STATUS
        # ------------------------------------------------------

        right_header = tk.Frame(
            header,
            bg="#081A2A"
        )

        right_header.pack(
            side="right",
            padx=25
        )


        tk.Label(
            right_header,
            text="●",
            bg="#081A2A",
            fg=GREEN,
            font=("Arial", 12)
        ).pack(
            side="left"
        )


        tk.Label(
            right_header,
            text="NETWORK ACTIVE",
            bg="#081A2A",
            fg=GREEN,
            font=("Consolas", 9, "bold")
        ).pack(
            side="left",
            padx=5
        )


        # ------------------------------------------------------
        # BODY
        # ------------------------------------------------------

        body = tk.Frame(
            self.screen,
            bg=BG
        )

        body.pack(
            fill="both",
            expand=True
        )


        # ======================================================
        # LEFT: SCROLLABLE PROBLEM MENU
        # ======================================================

        left = tk.Frame(
            body,
            bg=BG,
            width=425
        )

        left.pack(
            side="left",
            fill="y",
            padx=(20, 8),
            pady=18
        )

        left.pack_propagate(False)


        tk.Label(
            left,
            text="COMMUNITY PROBLEMS",
            bg=BG,
            fg=CYAN,
            font=("Consolas", 17, "bold")
        ).pack(
            anchor="w"
        )


        tk.Label(
            left,
            text="Scroll and choose a problem to explore.",
            bg=BG,
            fg=MUTED,
            font=("Arial", 9)
        ).pack(
            anchor="w",
            pady=(3, 10)
        )


        menu_container = tk.Frame(
            left,
            bg="#071522"
        )

        menu_container.pack(
            fill="both",
            expand=True
        )


        canvas = tk.Canvas(
            menu_container,
            bg="#071522",
            highlightthickness=0
        )


        scrollbar = ttk.Scrollbar(
            menu_container,
            orient="vertical",
            command=canvas.yview
        )


        cards_frame = tk.Frame(
            canvas,
            bg="#071522"
        )


        window_id = canvas.create_window(
            (0, 0),
            window=cards_frame,
            anchor="nw"
        )


        def update_scroll_region(event=None):

            canvas.configure(
                scrollregion=canvas.bbox("all")
            )


        def resize_cards(event):

            canvas.itemconfigure(
                window_id,
                width=event.width
            )


        cards_frame.bind(
            "<Configure>",
            update_scroll_region
        )

        canvas.bind(
            "<Configure>",
            resize_cards
        )


        canvas.configure(
            yscrollcommand=scrollbar.set
        )


        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )


        # ------------------------------------------------------
        # MOUSE-WHEEL SCROLLING
        # ------------------------------------------------------

        def wheel(event):

            canvas.yview_scroll(
                -1 if event.delta > 0 else 1,
                "units"
            )


        canvas.bind(
            "<MouseWheel>",
            wheel
        )


        # ------------------------------------------------------
        # CREATE PROBLEM CARDS
        # ------------------------------------------------------

        for index, module in enumerate(MODULES):

            self.create_problem_card(
                cards_frame,
                module,
                index
            )


        # ======================================================
        # RIGHT: DETAIL AREA
        # ======================================================

        self.detail = tk.Frame(
            body,
            bg=PANEL,
            highlightbackground=LINE,
            highlightthickness=1
        )

        self.detail.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(8, 20),
            pady=18
        )


        # Show first problem.
        self.update_detail()


        # ------------------------------------------------------
        # FLOWER PLANTER
        # ------------------------------------------------------
        # The planter is intentionally decorative.
        #
        # It gives the interface a warmer "community" feeling
        # instead of making the entire application look like
        # a cold technical dashboard.
        # ------------------------------------------------------

        self.create_flower_planter(
            self.screen
        )


    # ==========================================================
    # PROBLEM CARD
    # ==========================================================

    def create_problem_card(
        self,
        parent,
        module,
        index
    ):

        card = tk.Frame(
            parent,
            bg=CARD,
            height=98,
            cursor="hand2"
        )

        card.pack(
            fill="x",
            padx=8,
            pady=6
        )

        card.pack_propagate(False)


        # ------------------------------------------------------
        # PROFESSIONAL TEXT ICON
        # ------------------------------------------------------
        # Instead of emoji, every module gets a short technical
        # code such as TRF, MED, WTR and EDU.
        # ------------------------------------------------------

        icon = tk.Label(
            card,
            text=module["code"],
            bg=module["color"],
            fg=WHITE,
            font=("Consolas", 10, "bold"),
            width=6
        )

        icon.pack(
            side="left",
            fill="y"
        )


        content = tk.Frame(
            card,
            bg=CARD
        )

        content.pack(
            side="left",
            fill="both",
            expand=True,
            padx=12
        )


        title = tk.Label(
            content,
            text=module["title"],
            bg=CARD,
            fg=TEXT,
            font=("Consolas", 10, "bold"),
            anchor="w"
        )

        title.pack(
            fill="x",
            pady=(17, 2)
        )


        subtitle = tk.Label(
            content,
            text=module["short"],
            bg=CARD,
            fg=MUTED,
            font=("Arial", 8),
            anchor="w"
        )

        subtitle.pack(
            fill="x"
        )


        arrow = tk.Label(
            card,
            text="›",
            bg=CARD,
            fg=module["color"],
            font=("Arial", 24)
        )

        arrow.pack(
            side="right",
            padx=10
        )


        widgets = [
            card,
            content,
            title,
            subtitle,
            arrow
        ]


        # ------------------------------------------------------
        # HOVER EFFECT
        # ------------------------------------------------------

        def enter(event=None):

            if index != self.selected:

                for widget in widgets:

                    try:
                        widget.config(
                            bg=CARD_HOVER
                        )
                    except:
                        pass


        def leave(event=None):

            if index != self.selected:

                for widget in widgets:

                    try:
                        widget.config(
                            bg=CARD
                        )
                    except:
                        pass


        # ------------------------------------------------------
        # SELECTION
        # ------------------------------------------------------

        def select(event=None):

            beep()

            self.selected = index

            self.update_card_styles()

            self.update_detail()


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
                select
            )


        self.card_widgets.append(
            (
                card,
                content,
                title,
                subtitle,
                arrow
            )
        )


    # ==========================================================
    # UPDATE CARD COLORS
    # ==========================================================

    def update_card_styles(self):

        for index, widgets in enumerate(
            self.card_widgets
        ):

            card, content, title, subtitle, arrow = widgets

            if index == self.selected:

                bg = "#173B52"

            else:

                bg = CARD


            for widget in widgets:

                try:
                    widget.config(bg=bg)
                except:
                    pass


    # ==========================================================
    # DETAIL PANEL
    # ==========================================================

    def update_detail(self):

        for widget in self.detail.winfo_children():

            widget.destroy()


        module = MODULES[
            self.selected
        ]


        # ------------------------------------------------------
        # TOP TITLE AREA
        # ------------------------------------------------------

        top = tk.Frame(
            self.detail,
            bg=PANEL
        )

        top.pack(
            fill="x",
            padx=28,
            pady=25
        )


        tk.Label(
            top,
            text=module["code"],
            bg=module["color"],
            fg=WHITE,
            font=("Consolas", 12, "bold"),
            width=7,
            height=2
        ).pack(
            side="left",
            padx=(0, 15)
        )


        title_box = tk.Frame(
            top,
            bg=PANEL
        )

        title_box.pack(
            side="left"
        )


        tk.Label(
            title_box,
            text=module["title"],
            bg=PANEL,
            fg=TEXT,
            font=("Arial", 22, "bold")
        ).pack(
            anchor="w"
        )


        tk.Label(
            title_box,
            text=module["short"],
            bg=PANEL,
            fg=MUTED,
            font=("Arial", 9)
        ).pack(
            anchor="w"
        )


        # ------------------------------------------------------
        # THREE-STEP STORY
        # ------------------------------------------------------

        self.info_section(
            "01  THE PROBLEM",
            module["problem"],
            RED
        )


        self.info_section(
            "02  PROPOSED SOLUTION",
            module["solution"],
            CYAN
        )


        self.info_section(
            "03  COMMUNITY BENEFIT",
            module["benefit"],
            GREEN
        )


        # ------------------------------------------------------
        # USER STATISTICS
        # ------------------------------------------------------

        stats = tk.Frame(
            self.detail,
            bg="#071724"
        )

        stats.pack(
            fill="x",
            padx=28,
            pady=15
        )


        values = [
            ("ACTIONS", self.actions),
            ("IMPACT", self.impact),
            ("BADGES", len(self.achievements))
        ]


        for label, value in values:

            box = tk.Frame(
                stats,
                bg="#071724"
            )

            box.pack(
                side="left",
                expand=True,
                pady=13
            )


            tk.Label(
                box,
                text=str(value),
                bg="#071724",
                fg=TEXT,
                font=("Consolas", 17, "bold")
            ).pack()


            tk.Label(
                box,
                text=label,
                bg="#071724",
                fg=MUTED,
                font=("Consolas", 7, "bold")
            ).pack()


        # ------------------------------------------------------
        # OPEN SOLUTION
        # ------------------------------------------------------

        button = self.make_button(
            self.detail,
            "OPEN INTERACTIVE SOLUTION  →",
            lambda: self.open_solution(module),
            module["color"],
            300
        )

        button.pack(
            pady=12
        )


        # ------------------------------------------------------
        # QUOTE
        # ------------------------------------------------------

        tk.Label(
            self.detail,
            text=(
                "“"
                + QUOTES[
                    (self.selected + 2)
                    % len(QUOTES)
                ]
                + "”"
            ),
            bg=PANEL,
            fg=MUTED,
            font=("Georgia", 10, "italic"),
            wraplength=650
        ).pack(
            pady=5
        )


    # ==========================================================
    # INFO SECTION
    # ==========================================================

    def info_section(
        self,
        heading,
        text,
        color
    ):

        box = tk.Frame(
            self.detail,
            bg=PANEL
        )

        box.pack(
            fill="x",
            padx=28,
            pady=6
        )


        tk.Label(
            box,
            text=heading,
            bg=PANEL,
            fg=color,
            font=("Consolas", 9, "bold")
        ).pack(
            anchor="w"
        )


        tk.Label(
            box,
            text=text,
            bg=PANEL,
            fg=MUTED,
            font=("Arial", 9),
            wraplength=680,
            justify="left"
        ).pack(
            anchor="w",
            pady=(3, 0)
        )


    # ==========================================================
    # FLOWER PLANTER
    # ==========================================================
    # This is the decorative element requested for the bottom.
    #
    # It is drawn directly using Canvas shapes:
    #   - pot
    #   - stems
    #   - leaves
    #   - flowers
    #
    # A gentle flower animation makes the dashboard feel alive.
    # ==============================================================

    def create_flower_planter(self, parent):

        self.flower_canvas = tk.Canvas(
            parent,
            height=92,
            bg=BG,
            highlightthickness=0
        )

        self.flower_canvas.pack(
            fill="x",
            side="bottom"
        )


        self.flower_phase = 0

        self.animate_flowers()


    # ==========================================================
    # FLOWER ANIMATION
    # ==========================================================

    def animate_flowers(self):

        try:

            if not self.flower_canvas.winfo_exists():
                return


            canvas = self.flower_canvas

            canvas.delete("all")


            width = canvas.winfo_width()

            if width < 300:
                width = 1000


            # --------------------------------------------------
            # GROUND LINE
            # --------------------------------------------------

            canvas.create_line(
                0,
                80,
                width,
                80,
                fill="#173A2B",
                width=2
            )


            # --------------------------------------------------
            # FLOWERS
            # --------------------------------------------------

            flower_positions = [
                int(width * 0.12),
                int(width * 0.24),
                int(width * 0.36),
                int(width * 0.50),
                int(width * 0.64),
                int(width * 0.77),
                int(width * 0.89)
            ]


            flower_colors = [
                RED,
                PURPLE,
                CYAN,
                ORANGE,
                RED,
                PURPLE,
                CYAN
            ]


            for i, x in enumerate(
                flower_positions
            ):

                # Gentle movement gives each flower a slightly
                # different animation phase.
                sway = math.sin(
                    self.flower_phase
                    + i * 0.7
                ) * 2


                stem_top = 38 + (
                    i % 3
                ) * 5


                # Stem.
                canvas.create_line(
                    x,
                    80,
                    x + sway,
                    stem_top,
                    fill=GREEN,
                    width=2
                )


                # Left leaf.
                canvas.create_oval(
                    x - 13 + sway,
                    58,
                    x + sway,
                    68,
                    fill="#238252",
                    outline=""
                )


                # Right leaf.
                canvas.create_oval(
                    x + sway,
                    51,
                    x + 14 + sway,
                    61,
                    fill="#238252",
                    outline=""
                )


                # Flower center.
                fx = x + sway
                fy = stem_top


                # Petals.
                for petal_angle in range(
                    0,
                    360,
                    72
                ):

                    radians = math.radians(
                        petal_angle
                    )


                    px = (
                        fx
                        + math.cos(radians)
                        * 8
                    )


                    py = (
                        fy
                        + math.sin(radians)
                        * 8
                    )


                    canvas.create_oval(
                        px - 5,
                        py - 5,
                        px + 5,
                        py + 5,
                        fill=flower_colors[i],
                        outline=""
                    )


                # Flower center.
                canvas.create_oval(
                    fx - 3,
                    fy - 3,
                    fx + 3,
                    fy + 3,
                    fill=ORANGE,
                    outline=""
                )


            # --------------------------------------------------
            # PLANTER
            # --------------------------------------------------
            # The planter is drawn in the center to visually
            # anchor the flower arrangement.
            # --------------------------------------------------

            pot_x = width // 2


            canvas.create_polygon(
                pot_x - 70,
                57,
                pot_x + 70,
                57,
                pot_x + 53,
                86,
                pot_x - 53,
                86,
                fill="#7A4A35",
                outline=""
            )


            canvas.create_rectangle(
                pot_x - 76,
                52,
                pot_x + 76,
                61,
                fill="#935B3F",
                outline=""
            )


            # Update animation phase.
            self.flower_phase += 0.08


            self.root.after(
                70,
                self.animate_flowers
            )


        except tk.TclError:
            pass


    # ==========================================================
    # SOLUTION ROUTER
    # ==========================================================

    def open_solution(self, module):

        beep()


        if module["key"] == "traffic":
            self.traffic_solution(module)

        elif module["key"] == "road":
            self.road_solution(module)

        elif module["key"] == "blood":
            self.blood_solution(module)

        elif module["key"] == "clean":
            self.clean_solution(module)

        elif module["key"] == "food":
            self.food_solution(module)

        elif module["key"] == "education":
            self.education_solution(module)

        elif module["key"] == "water":
            self.water_solution(module)


    # ==========================================================
    # COMMON SOLUTION WINDOW
    # ==========================================================

    def solution_window(self, module):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "CIVIC SHIELD // "
            + module["title"]
        )

        window.geometry(
            "900x700"
        )

        window.minsize(
            760,
            600
        )

        window.configure(
            bg=BG
        )


        header = tk.Frame(
            window,
            bg="#081A2A",
            height=72
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)


        tk.Label(
            header,
            text=module["code"],
            bg=module["color"],
            fg=WHITE,
            font=("Consolas", 11, "bold"),
            width=7
        ).pack(
            side="left",
            padx=20,
            pady=16
        )


        tk.Label(
            header,
            text=module["title"],
            bg="#081A2A",
            fg=TEXT,
            font=("Arial", 21, "bold")
        ).pack(
            side="left"
        )


        return window


    # ==========================================================
    # ==========================================================
    # SMART TRAFFIC RESPONSE SYSTEM
    # ==========================================================
    # THIS IS THE MOST IMPORTANT INTERACTIVE MODULE.
    #
    # DESIGN GOAL:
    # ----------------------------------------------------------
    # Instead of making an officer manually calculate everything,
    # the system asks for a few easy observations:
    #
    #   - intersection
    #   - vehicles in each direction
    #   - incident type
    #   - weather
    #   - emergency vehicle status
    #
    # It then creates:
    #
    #   1. Congestion score
    #   2. Priority direction
    #   3. Suggested signal allocation
    #   4. Officer action checklist
    #   5. Incident summary
    #
    # This is decision SUPPORT, not automatic policing.
    # A human officer remains responsible for the decision.
    # ==============================================================

    def traffic_solution(self, module):

        window = self.solution_window(
            module
        )


        # ------------------------------------------------------
        # MAIN CONTENT
        # ------------------------------------------------------

        main = tk.Frame(
            window,
            bg=BG
        )

        main.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=18
        )


        # ------------------------------------------------------
        # TITLE
        # ------------------------------------------------------

        tk.Label(
            main,
            text="OFFICER TRAFFIC RESPONSE CENTER",
            bg=BG,
            fg=CYAN,
            font=("Consolas", 15, "bold")
        ).pack(
            anchor="w"
        )


        tk.Label(
            main,
            text=(
                "Enter quick field observations. "
                "The system converts them into a clear "
                "decision-support summary."
            ),
            bg=BG,
            fg=MUTED,
            font=("Arial", 9)
        ).pack(
            anchor="w",
            pady=(2, 12)
        )


        # ------------------------------------------------------
        # TWO-COLUMN LAYOUT
        # ------------------------------------------------------

        columns = tk.Frame(
            main,
            bg=BG
        )

        columns.pack(
            fill="both",
            expand=True
        )


        left = tk.Frame(
            columns,
            bg="#0B1F30",
            width=370
        )

        left.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )

        left.pack_propagate(False)


        right = tk.Frame(
            columns,
            bg="#081724"
        )

        right.pack(
            side="left",
            fill="both",
            expand=True
        )


        # ======================================================
        # LEFT: FIELD INPUT
        # ======================================================

        tk.Label(
            left,
            text="FIELD OBSERVATIONS",
            bg="#0B1F30",
            fg=CYAN,
            font=("Consolas", 11, "bold")
        ).pack(
            anchor="w",
            padx=18,
            pady=(18, 8)
        )


        # ------------------------------------------------------
        # INTERSECTION
        # ------------------------------------------------------

        tk.Label(
            left,
            text="Intersection / location",
            bg="#0B1F30",
            fg=MUTED,
            font=("Arial", 8)
        ).pack(
            anchor="w",
            padx=18
        )


        location = tk.Entry(
            left,
            bg="#102B40",
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            font=("Consolas", 10)
        )

        location.insert(
            0,
            "Main Junction"
        )

        location.pack(
            fill="x",
            padx=18,
            pady=(3, 10)
        )


        # ------------------------------------------------------
        # INCIDENT TYPE
        # ------------------------------------------------------

        tk.Label(
            left,
            text="Current incident",
            bg="#0B1F30",
            fg=MUTED,
            font=("Arial", 8)
        ).pack(
            anchor="w",
            padx=18
        )


        incident = tk.StringVar(
            value="Normal congestion"
        )


        incident_menu = ttk.Combobox(
            left,
            textvariable=incident,
            state="readonly",
            values=[
                "Normal congestion",
                "Minor collision",
                "Major collision",
                "Road blockage",
                "Pedestrian crowd",
                "Road construction"
            ]
        )


        incident_menu.pack(
            fill="x",
            padx=18,
            pady=(3, 10)
        )


        # ------------------------------------------------------
        # WEATHER
        # ------------------------------------------------------

        tk.Label(
            left,
            text="Weather / road condition",
            bg="#0B1F30",
            fg=MUTED,
            font=("Arial", 8)
        ).pack(
            anchor="w",
            padx=18
        )


        weather = tk.StringVar(
            value="Clear"
        )


        ttk.Combobox(
            left,
            textvariable=weather,
            state="readonly",
            values=[
                "Clear",
                "Rain",
                "Heavy rain",
                "Fog",
                "Poor visibility"
            ]
        ).pack(
            fill="x",
            padx=18,
            pady=(3, 10)
        )


        # ------------------------------------------------------
        # EMERGENCY MODE
        # ------------------------------------------------------
        # This checkbox simulates an emergency vehicle needing
        # priority through the intersection.
        # ==============================================================

        emergency = tk.BooleanVar(
            value=False
        )


        tk.Checkbutton(
            left,
            text="Emergency vehicle approaching",
            variable=emergency,
            bg="#0B1F30",
            fg=TEXT,
            activebackground="#0B1F30",
            activeforeground=TEXT,
            selectcolor="#163A52",
            font=("Arial", 9)
        ).pack(
            anchor="w",
            padx=18,
            pady=8
        )


        # ------------------------------------------------------
        # QUEUE INPUTS
        # ------------------------------------------------------
        # Officers only need to estimate how many vehicles are
        # waiting in each direction.
        # ==============================================================

        tk.Label(
            left,
            text="ESTIMATED VEHICLE QUEUES",
            bg="#0B1F30",
            fg=ORANGE,
            font=("Consolas", 9, "bold")
        ).pack(
            anchor="w",
            padx=18,
            pady=(10, 4)
        )


        queue_entries = {}


        directions = [
            "North",
            "South",
            "East",
            "West"
        ]


        defaults = [
            35,
            28,
            62,
            18
        ]


        for direction, default in zip(
            directions,
            defaults
        ):

            row = tk.Frame(
                left,
                bg="#0B1F30"
            )

            row.pack(
                fill="x",
                padx=18,
                pady=3
            )


            tk.Label(
                row,
                text=direction,
                bg="#0B1F30",
                fg=TEXT,
                width=8,
                anchor="w",
                font=("Consolas", 9)
            ).pack(
                side="left"
            )


            entry = tk.Entry(
                row,
                bg="#102B40",
                fg=TEXT,
                insertbackground=TEXT,
                relief="flat",
                justify="center",
                font=("Consolas", 9)
            )


            entry.insert(
                0,
                str(default)
            )


            entry.pack(
                side="left",
                fill="x",
                expand=True
            )


            queue_entries[
                direction
            ] = entry


        # ======================================================
        # RIGHT: RESULT AREA
        # ======================================================

        tk.Label(
            right,
            text="SYSTEM RECOMMENDATION",
            bg="#081724",
            fg=CYAN,
            font=("Consolas", 11, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )


        result = tk.Text(
            right,
            bg="#071522",
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            bd=0,
            font=("Consolas", 9),
            wrap="word"
        )


        result.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=8
        )


        # ------------------------------------------------------
        # DEFAULT SYSTEM MESSAGE
        # ------------------------------------------------------

        result.insert(
            "end",
            "READY.\n\n"
            "Enter current field conditions and press\n"
            "\"GENERATE RESPONSE PLAN\".\n\n"
            "The system will produce:\n"
            "• congestion level\n"
            "• priority direction\n"
            "• signal timing suggestion\n"
            "• officer checklist\n"
            "• incident summary\n"
        )


        # ======================================================
        # TRAFFIC CALCULATION ENGINE
        # ======================================================
        # This function converts the observations into a
        # transparent, understandable recommendation.
        #
        # It deliberately uses simple formulas so a judge can
        # understand exactly how the prototype works.
        # ==============================================================

        def generate_plan():

            try:

                queues = {}

                for direction, entry in queue_entries.items():

                    value = int(
                        entry.get()
                    )

                    if value < 0:
                        raise ValueError

                    queues[
                        direction
                    ] = value


                total = sum(
                    queues.values()
                )


                if total == 0:

                    messagebox.showwarning(
                        "No traffic data",
                        "Enter at least one vehicle "
                        "in the intersection.",
                        parent=window
                    )

                    return


                # ------------------------------------------------
                # FIND THE MOST CONGESTED DIRECTION
                # ------------------------------------------------

                priority_direction = max(
                    queues,
                    key=queues.get
                )


                largest_queue = queues[
                    priority_direction
                ]


                # ------------------------------------------------
                # CALCULATE CONGESTION SCORE
                # ------------------------------------------------
                # The score is a prototype indicator based on
                # queue size. It is NOT a real traffic standard.
                # ------------------------------------------------

                congestion_score = min(
                    100,
                    round(
                        total / 3
                    )
                )


                if congestion_score >= 75:
                    congestion_level = "CRITICAL"

                elif congestion_score >= 50:
                    congestion_level = "HIGH"

                elif congestion_score >= 25:
                    congestion_level = "MODERATE"

                else:
                    congestion_level = "LOW"


                # ------------------------------------------------
                # INCIDENT ADJUSTMENT
                # ------------------------------------------------

                incident_adjustment = {
                    "Normal congestion": 0,
                    "Minor collision": 10,
                    "Major collision": 25,
                    "Road blockage": 25,
                    "Pedestrian crowd": 15,
                    "Road construction": 10
                }


                congestion_score = min(
                    100,
                    congestion_score
                    + incident_adjustment[
                        incident.get()
                    ]
                )


                # ------------------------------------------------
                # WEATHER ADJUSTMENT
                # ------------------------------------------------

                if weather.get() in (
                    "Heavy rain",
                    "Fog",
                    "Poor visibility"
                ):

                    congestion_score = min(
                        100,
                        congestion_score + 10
                    )


                # ------------------------------------------------
                # SIGNAL TIMING
                # ------------------------------------------------
                # A 120-second demonstration cycle is divided
                # proportionally between the directions.
                #
                # Minimum green time prevents a direction from
                # being completely ignored.
                # ------------------------------------------------

                cycle = 120

                minimum_green = 12

                raw_times = {}


                for direction, queue in queues.items():

                    raw_times[
                        direction
                    ] = max(
                        minimum_green,
                        round(
                            (
                                queue
                                / total
                            )
                            * cycle
                        )
                    )


                # Adjust total so the cycle remains close to
                # the configured 120 seconds.
                calculated_total = sum(
                    raw_times.values()
                )


                if calculated_total > cycle:

                    excess = (
                        calculated_total
                        - cycle
                    )


                    raw_times[
                        priority_direction
                    ] = max(
                        minimum_green,
                        raw_times[
                            priority_direction
                        ] - excess
                    )


                # ------------------------------------------------
                # EMERGENCY VEHICLE MODE
                # ------------------------------------------------

                emergency_text = (
                    "NO emergency priority requested."
                )


                if emergency.get():

                    emergency_text = (
                        "EMERGENCY VEHICLE MODE ACTIVE.\n"
                        "Officer should follow authorized "
                        "emergency-traffic procedures and "
                        "visually confirm the route is safe."
                    )


                # ------------------------------------------------
                # OFFICER CHECKLIST
                # ------------------------------------------------

                checklist = []


                if incident.get() in (
                    "Major collision",
                    "Road blockage"
                ):

                    checklist.append(
                        "Establish a safe perimeter."
                    )

                    checklist.append(
                        "Identify blocked lanes."
                    )


                if weather.get() != "Clear":

                    checklist.append(
                        "Increase caution due to road conditions."
                    )


                if largest_queue >= 50:

                    checklist.append(
                        f"Monitor the {priority_direction} queue."
                    )


                checklist.append(
                    "Keep pedestrian movement visible and safe."
                )


                checklist.append(
                    "Reassess traffic conditions after intervention."
                )


                # ------------------------------------------------
                # DISPLAY RESULT
                # ------------------------------------------------

                result.delete(
                    "1.0",
                    "end"
                )


                result.insert(
                    "end",
                    "TRAFFIC RESPONSE PLAN\n"
                    "══════════════════════════════════════\n\n"
                )


                result.insert(
                    "end",
                    f"LOCATION\n"
                    f"  {location.get()}\n\n"
                )


                result.insert(
                    "end",
                    f"INCIDENT\n"
                    f"  {incident.get()}\n\n"
                )


                result.insert(
                    "end",
                    f"TRAFFIC STATUS\n"
                    f"  {congestion_level}\n"
                    f"  Score: {congestion_score}/100\n"
                    f"  Total queued vehicles: {total}\n\n"
                )


                result.insert(
                    "end",
                    "PRIORITY DIRECTION\n"
                    "──────────────────────────────────────\n"
                )


                result.insert(
                    "end",
                    f"  {priority_direction} "
                    f"→ {largest_queue} vehicles\n\n"
                )


                result.insert(
                    "end",
                    "SUGGESTED SIGNAL ALLOCATION\n"
                    "──────────────────────────────────────\n"
                )


                for direction in directions:

                    result.insert(
                        "end",
                        f"  {direction:<8} "
                        f"{queues[direction]:>3} vehicles"
                        f"  →  "
                        f"{raw_times[direction]:>3}s green\n"
                    )


                result.insert(
                    "end",
                    "\n"
                )


                result.insert(
                    "end",
                    "OFFICER ACTION CHECKLIST\n"
                    "──────────────────────────────────────\n"
                )


                for item in checklist:

                    result.insert(
                        "end",
                        "  □ " + item + "\n"
                    )


                result.insert(
                    "end",
                    "\n"
                )


                result.insert(
                    "end",
                    emergency_text
                    + "\n\n"
                )


                result.insert(
                    "end",
                    "DECISION NOTE\n"
                    "──────────────────────────────────────\n"
                    "This recommendation is decision support only.\n"
                    "The officer must verify actual road conditions,\n"
                    "follow local traffic rules and use human judgment.\n"
                )


                self.add_action(
                    120
                )


                beep("success")


                # Update dashboard statistics when the
                # solution window is closed.
                # The dashboard itself will reflect the new
                # values the next time it is refreshed.


            except ValueError:

                beep("warning")

                messagebox.showerror(
                    "Invalid traffic data",
                    "Vehicle queues must be whole numbers "
                    "greater than or equal to zero.",
                    parent=window
                )


        # ======================================================
        # GENERATE PLAN BUTTON
        # ======================================================

        self.make_button(
            left,
            "GENERATE RESPONSE PLAN",
            generate_plan,
            ORANGE,
            300
        ).pack(
            pady=16,
            padx=18
        )


        # ------------------------------------------------------
        # REALISTIC DESIGN NOTE
        # ------------------------------------------------------

        tk.Label(
            left,
            text=(
                "DESIGNED FOR HUMAN DECISION SUPPORT\n"
                "The officer remains in control."
            ),
            bg="#0B1F30",
            fg=MUTED,
            font=("Consolas", 7),
            justify="left"
        ).pack(
            anchor="w",
            padx=18,
            pady=5
        )


    # ==========================================================
    # ROAD SAFETY
    # ==========================================================

    def road_solution(self, module):

        window = self.solution_window(
            module
        )


        frame = tk.Frame(
            window,
            bg=BG
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )


        tk.Label(
            frame,
            text="ROAD SAFETY ANALYZER",
            bg=BG,
            fg=CYAN,
            font=("Consolas", 15, "bold")
        ).pack(
            anchor="w"
        )


        entries = {}


        for label, default in [
            ("Observed speed (km/h)", "68"),
            ("Road limit (km/h)", "50"),
            ("Location", "School zone")
        ]:

            tk.Label(
                frame,
                text=label,
                bg=BG,
                fg=MUTED,
                font=("Arial", 9)
            ).pack(
                anchor="w",
                pady=(12, 2)
            )


            entry = tk.Entry(
                frame,
                bg="#102B40",
                fg=TEXT,
                insertbackground=TEXT,
                relief="flat"
            )


            entry.insert(
                0,
                default
            )


            entry.pack(
                fill="x"
            )


            entries[
                label
            ] = entry


        result = tk.Label(
            frame,
            text="READY FOR ANALYSIS",
            bg=BG,
            fg=MUTED,
            font=("Consolas", 10),
            justify="left"
        )


        result.pack(
            anchor="w",
            pady=20
        )


        def analyze():

            try:

                speed = float(
                    entries[
                        "Observed speed (km/h)"
                    ].get()
                )


                limit = float(
                    entries[
                        "Road limit (km/h)"
                    ].get()
                )


                excess = speed - limit


                self.add_action(
                    60
                )


                if excess <= 0:

                    result.config(
                        text=(
                            "✓ WITHIN CONFIGURED LIMIT\n\n"
                            f"Observed: {speed:.1f} km/h\n"
                            f"Limit: {limit:.1f} km/h\n\n"
                            "Continue normal monitoring."
                        ),
                        fg=GREEN
                    )


                    beep("success")


                else:

                    risk = min(
                        100,
                        round(
                            30 + excess * 2
                        )
                    )


                    result.config(
                        text=(
                            "⚠ SPEED RISK FLAG\n\n"
                            f"Observed: {speed:.1f} km/h\n"
                            f"Limit: {limit:.1f} km/h\n"
                            f"Excess: {excess:.1f} km/h\n"
                            f"Risk indicator: {risk}/100\n\n"
                            "Suggested response:\n"
                            "Increase observation and apply "
                            "authorized procedures."
                        ),
                        fg=RED
                    )


                    beep("warning")


            except ValueError:

                result.config(
                    text="Please enter valid numbers.",
                    fg=ORANGE
                )


        self.make_button(
            frame,
            "ANALYZE ROAD RISK",
            analyze,
            module["color"],
            260
        ).pack(
            anchor="w"
        )


    # ==========================================================
    # BLOOD RESPONSE
    # ==========================================================

    def blood_solution(self, module):

        window = self.solution_window(
            module
        )


        frame = tk.Frame(
            window,
            bg=BG
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )


        tk.Label(
            frame,
            text="EMERGENCY DONOR COORDINATION",
            bg=BG,
            fg=CYAN,
            font=("Consolas", 15, "bold")
        ).pack(
            anchor="w"
        )


        tk.Label(
            frame,
            text=(
                "Demonstration interface — actual blood matching "
                "must be verified by qualified medical services."
            ),
            bg=BG,
            fg=MUTED,
            font=("Arial", 9)
        ).pack(
            anchor="w",
            pady=5
        )


        blood = tk.StringVar(
            value="O+"
        )


        urgency = tk.StringVar(
            value="URGENT"
        )


        tk.Label(
            frame,
            text="Blood group",
            bg=BG,
            fg=MUTED
        ).pack(
            anchor="w",
            pady=(15, 2)
        )


        ttk.Combobox(
            frame,
            textvariable=blood,
            state="readonly",
            values=[
                "O-",
                "O+",
                "A-",
                "A+",
                "B-",
                "B+",
                "AB-",
                "AB+"
            ]
        ).pack(
            fill="x"
        )


        tk.Label(
            frame,
            text="Urgency",
            bg=BG,
            fg=MUTED
        ).pack(
            anchor="w",
            pady=(12, 2)
        )


        ttk.Combobox(
            frame,
            textvariable=urgency,
            state="readonly",
            values=[
                "CRITICAL",
                "URGENT",
                "NORMAL"
            ]
        ).pack(
            fill="x"
        )


        result = tk.Label(
            frame,
            text="No request created.",
            bg=BG,
            fg=MUTED,
            font=("Consolas", 10),
            justify="left"
        )


        result.pack(
            anchor="w",
            pady=20
        )


        def create_request():

            self.add_action(
                100
            )


            request_id = (
                "MED-"
                + str(
                    random.randint(
                        10000,
                        99999
                    )
                )
            )


            result.config(
                text=(
                    "REQUEST CREATED\n\n"
                    f"Request ID: {request_id}\n"
                    f"Blood group: {blood.get()}\n"
                    f"Urgency: {urgency.get()}\n\n"
                    "Next step:\n"
                    "Contact an authorized blood bank or "
                    "medical service for verified matching."
                ),
                fg=GREEN
            )


            beep("success")


        self.make_button(
            frame,
            "CREATE DONOR REQUEST",
            create_request,
            module["color"],
            280
        ).pack(
            anchor="w"
        )


    # ==========================================================
    # CLEAN CITY
    # ==========================================================

    def clean_solution(self, module):

        window = self.solution_window(
            module
        )


        frame = tk.Frame(
            window,
            bg=BG
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )


        tk.Label(
            frame,
            text="CITY SERVICE REPORT CENTER",
            bg=BG,
            fg=CYAN,
            font=("Consolas", 15, "bold")
        ).pack(
            anchor="w"
        )


        location = tk.Entry(
            frame,
            bg="#102B40",
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat"
        )


        location.insert(
            0,
            "Location / landmark"
        )


        location.pack(
            fill="x",
            pady=12
        )


        description = tk.Text(
            frame,
            height=9,
            bg="#102B40",
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat"
        )


        description.pack(
            fill="both",
            expand=True
        )


        result = tk.Label(
            frame,
            text="REPORT READY",
            bg=BG,
            fg=MUTED,
            font=("Consolas", 10),
            justify="left"
        )


        result.pack(
            anchor="w",
            pady=12
        )


        def submit():

            text = description.get(
                "1.0",
                "end"
            ).lower()


            if not text.strip():

                messagebox.showwarning(
                    "Empty report",
                    "Describe the problem first.",
                    parent=window
                )

                return


            if any(
                word in text
                for word in [
                    "danger",
                    "blocked drain",
                    "overflow",
                    "hazard"
                ]
            ):

                priority = "CRITICAL"

            elif any(
                word in text
                for word in [
                    "garbage",
                    "waste",
                    "smell",
                    "blocked"
                ]
            ):

                priority = "HIGH"

            else:

                priority = "NORMAL"


            ticket = (
                "CITY-"
                + str(
                    random.randint(
                        10000,
                        99999
                    )
                )
            )


            self.add_action(
                70
            )


            result.config(
                text=(
                    "REPORT SUBMITTED\n\n"
                    f"Ticket: {ticket}\n"
                    f"Priority: {priority}\n"
                    "Status: QUEUED FOR REVIEW"
                ),
                fg=GREEN
            )


            beep("success")


        self.make_button(
            frame,
            "SUBMIT CITY REPORT",
            submit,
            module["color"],
            260
        ).pack(
            anchor="w"
        )


    # ==========================================================
    # FOOD RESCUE
    # ==========================================================

    def food_solution(self, module):

        window = self.solution_window(
            module
        )


        frame = tk.Frame(
            window,
            bg=BG
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )


        tk.Label(
            frame,
            text="SURPLUS FOOD MATCHING",
            bg=BG,
            fg=CYAN,
            font=("Consolas", 15, "bold")
        ).pack(
            anchor="w"
        )


        fields = {}


        for label, default in [
            ("Food", "Prepared meals"),
            ("Quantity", "30 portions"),
            ("Pickup", "Within 2 hours")
        ]:

            tk.Label(
                frame,
                text=label,
                bg=BG,
                fg=MUTED
            ).pack(
                anchor="w",
                pady=(12, 2)
            )


            entry = tk.Entry(
                frame,
                bg="#102B40",
                fg=TEXT,
                insertbackground=TEXT,
                relief="flat"
            )


            entry.insert(
                0,
                default
            )


            entry.pack(
                fill="x"
            )


            fields[
                label
            ] = entry


        result = tk.Label(
            frame,
            text="NO MATCH CREATED",
            bg=BG,
            fg=MUTED,
            font=("Consolas", 10),
            justify="left"
        )


        result.pack(
            anchor="w",
            pady=20
        )


        def match():

            organizations = [
                "Community Kitchen",
                "Local Relief Center",
                "Neighborhood Food Bank"
            ]


            recipient = random.choice(
                organizations
            )


            self.add_action(
                80
            )


            result.config(
                text=(
                    "SURPLUS LISTING CREATED\n\n"
                    f"Food: {fields['Food'].get()}\n"
                    f"Quantity: {fields['Quantity'].get()}\n"
                    f"Pickup: {fields['Pickup'].get()}\n\n"
                    f"Suggested recipient:\n"
                    f"{recipient}\n\n"
                    "Food safety and local regulations "
                    "must be verified before transfer."
                ),
                fg=GREEN
            )


            beep("success")


        self.make_button(
            frame,
            "FIND COMMUNITY RECIPIENT",
            match,
            module["color"],
            280
        ).pack(
            anchor="w"
        )


    # ==========================================================
    # EDUCATION ACCESS
    # ==========================================================

    def education_solution(self, module):

        window = self.solution_window(
            module
        )


        frame = tk.Frame(
            window,
            bg=BG
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )


        tk.Label(
            frame,
            text="PERSONAL LEARNING PATH",
            bg=BG,
            fg=CYAN,
            font=("Consolas", 15, "bold")
        ).pack(
            anchor="w"
        )


        paths = {

            "Programming": [
                "Python fundamentals",
                "Problem solving",
                "Data structures",
                "Build a project"
            ],

            "Mathematics": [
                "Algebra",
                "Functions",
                "Geometry",
                "Practice problems"
            ],

            "Science": [
                "Core concepts",
                "Experiments",
                "Data interpretation",
                "Revision"
            ],

            "English": [
                "Vocabulary",
                "Grammar",
                "Listening",
                "Speaking"
            ]
        }


        subject = tk.StringVar(
            value="Programming"
        )


        ttk.Combobox(
            frame,
            textvariable=subject,
            state="readonly",
            values=list(
                paths.keys()
            )
        ).pack(
            anchor="w",
            pady=15
        )


        listbox = tk.Listbox(
            frame,
            bg="#102B40",
            fg=TEXT,
            selectbackground="#28546D",
            relief="flat",
            font=("Consolas", 10)
        )


        listbox.pack(
            fill="both",
            expand=True
        )


        progress = 0


        progress_label = tk.Label(
            frame,
            text="PROGRESS: 0%",
            bg=BG,
            fg=MUTED,
            font=("Consolas", 10)
        )


        progress_label.pack(
            anchor="w",
            pady=10
        )


        def refresh():

            listbox.delete(
                0,
                "end"
            )


            for item in paths[
                subject.get()
            ]:

                listbox.insert(
                    "end",
                    "□ " + item
                )


        def complete():

            nonlocal progress


            selection = listbox.curselection()


            if not selection:
                return


            index = selection[0]

            current = listbox.get(
                index
            )


            if current.startswith("□"):

                listbox.delete(
                    index
                )

                listbox.insert(
                    index,
                    "✓ "
                    + current[2:]
                )


                progress = min(
                    100,
                    progress + 25
                )


                progress_label.config(
                    text=(
                        f"PROGRESS: {progress}%"
                    ),
                    fg=GREEN
                )


                self.add_action(
                    40
                )


                beep("success")


        subject.trace_add(
            "write",
            lambda *_: refresh()
        )


        refresh()


        self.make_button(
            frame,
            "MARK TOPIC COMPLETE",
            complete,
            module["color"],
            260
        ).pack(
            anchor="w"
        )


    # ==========================================================
    # WATER PROTECTION
    # ==========================================================

    def water_solution(self, module):

        window = self.solution_window(
            module
        )


        frame = tk.Frame(
            window,
            bg=BG
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )


        tk.Label(
            frame,
            text="WATER USAGE ANALYZER",
            bg=BG,
            fg=CYAN,
            font=("Consolas", 15, "bold")
        ).pack(
            anchor="w"
        )


        entries = {}


        fields = [
            (
                "Previous reading (L)",
                "1000"
            ),
            (
                "Current reading (L)",
                "1120"
            ),
            (
                "Hours elapsed",
                "24"
            )
        ]


        for label, default in fields:

            tk.Label(
                frame,
                text=label,
                bg=BG,
                fg=MUTED
            ).pack(
                anchor="w",
                pady=(12, 2)
            )


            entry = tk.Entry(
                frame,
                bg="#102B40",
                fg=TEXT,
                insertbackground=TEXT,
                relief="flat"
            )


            entry.insert(
                0,
                default
            )


            entry.pack(
                fill="x"
            )


            entries[
                label
            ] = entry


        result = tk.Label(
            frame,
            text="ANALYZER READY",
            bg=BG,
            fg=MUTED,
            font=("Consolas", 10),
            justify="left"
        )


        result.pack(
            anchor="w",
            pady=20
        )


        def analyze():

            try:

                old = float(
                    entries[
                        "Previous reading (L)"
                    ].get()
                )


                current = float(
                    entries[
                        "Current reading (L)"
                    ].get()
                )


                hours = float(
                    entries[
                        "Hours elapsed"
                    ].get()
                )


                if hours <= 0 or current < old:
                    raise ValueError


                consumed = (
                    current - old
                )


                rate = (
                    consumed / hours
                )


                self.add_action(
                    65
                )


                if rate > 5:

                    result.config(
                        text=(
                            "⚠ POSSIBLE UNUSUAL USAGE\n\n"
                            f"Consumption: {consumed:.1f} L\n"
                            f"Rate: {rate:.2f} L/hour\n\n"
                            "Recommendation:\n"
                            "Inspect taps, toilets, pipes and "
                            "outdoor water lines."
                        ),
                        fg=RED
                    )


                    beep("warning")


                else:

                    result.config(
                        text=(
                            "✓ USAGE APPEARS STABLE\n\n"
                            f"Consumption: {consumed:.1f} L\n"
                            f"Rate: {rate:.2f} L/hour\n\n"
                            "Continue monitoring for sudden changes."
                        ),
                        fg=GREEN
                    )


                    beep("success")


            except ValueError:

                result.config(
                    text=(
                        "Enter valid meter readings "
                        "and elapsed hours."
                    ),
                    fg=ORANGE
                )


        self.make_button(
            frame,
            "RUN WATER ANALYSIS",
            analyze,
            module["color"],
            260
        ).pack(
            anchor="w"
        )


# ==============================================================
# PROGRAM ENTRY POINT
# ==============================================================
#
# Python starts the graphical application here.
#
# Tk() creates the main window.
# CivicShield(root) creates our application.
# mainloop() keeps listening for clicks, scrolling, typing,
# animations and other user interactions.
# ==============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = CivicShield(
        root
    )

    root.mainloop()