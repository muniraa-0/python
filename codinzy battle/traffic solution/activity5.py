import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import platform

# ============================================================
# CIVIC SHIELD
# Interactive Civic Problems & Solutions Platform
#
# PROJECT PURPOSE:
# Civic Shield is a prototype platform that demonstrates how
# technology can help communities identify problems and
# interact with practical solutions.
#
# The project focuses on seven areas:
#   1. Road Safety
#   2. Smart Traffic
#   3. Blood Response
#   4. Clean City
#   5. Food Rescue
#   6. Education Access
#   7. Water Protection
#
# IMPORTANT:
# This is an educational/prototype application. The simulated
# data and results demonstrate the concept and are not intended
# to replace real government, medical, emergency, or traffic
# systems.
#
# TECHNOLOGY:
# - Python
# - Tkinter for the graphical user interface
# - No external packages are required
# ============================================================


# ============================================================
# COLOR SYSTEM
# ============================================================
# Keeping the colors in one place makes the interface easier
# to maintain. If the visual theme needs to change, the colors
# can be modified here instead of throughout the program.
# ============================================================

BG = "#07111F"
PANEL = "#0B1B2B"
CARD = "#10263A"
CARD_HOVER = "#153650"
BORDER = "#1B405A"

TEXT = "#E8F1F8"
MUTED = "#7890A4"

CYAN = "#35D6FF"
GREEN = "#35E08A"
RED = "#FF5C6C"
ORANGE = "#FFAD42"
PURPLE = "#9B7BFF"
WHITE = "#FFFFFF"


# ============================================================
# BACKGROUND QUOTES
# ============================================================
# These quotes are displayed on the introduction and problem
# screens to communicate the project's main message:
# technology should be used to create positive social impact.
# ============================================================

QUOTES = [
    "Small actions can create big changes.",
    "Technology becomes meaningful when it improves lives.",
    "A safer community begins with one responsible action.",
    "The future is built by the problems we choose to solve.",
    "Every solved problem is a stronger community.",
]


# ============================================================
# CIVIC PROBLEM DATABASE
# ============================================================
# Each dictionary represents one problem module.
#
# This structure makes the application scalable. More problems
# can be added later simply by adding another dictionary rather
# than rewriting the entire interface.
#
# Each module contains:
#   key      -> internal identifier
#   code     -> short visual identifier
#   title    -> name shown to the user
#   short    -> short description
#   color    -> module's visual identity
#   problem  -> explanation of the social problem
#   solution -> proposed technological approach
#   benefit  -> expected community benefit
# ============================================================

MODULES = [

    {
        "key": "road",
        "code": "RAD",
        "title": "ROAD SAFETY",
        "short": "Reduce speeding and accident risks",
        "color": RED,

        "problem":
            "Speeding, dangerous driving and poor road awareness "
            "increase the chance and severity of crashes.",

        "solution":
            "Use a community safety center to analyze reported "
            "speeds, calculate risk, identify repeat hazards and "
            "provide targeted safety guidance.",

        "benefit":
            "Faster identification of dangerous behavior and "
            "better awareness around schools, crossings and busy "
            "intersections.",
    },

    {
        "key": "traffic",
        "code": "SIG",
        "title": "SMART TRAFFIC",
        "short": "Reduce congestion and waiting time",
        "color": ORANGE,

        "problem":
            "Fixed traffic timing can waste road capacity when "
            "one direction is crowded and another is nearly empty.",

        "solution":
            "Use live vehicle counts to create an adaptive signal "
            "plan that gives more green time to heavier queues.",

        "benefit":
            "Less unnecessary waiting, more balanced intersections "
            "and a clearer picture of where congestion is forming.",
    },

    {
        "key": "blood",
        "code": "MED",
        "title": "BLOOD RESPONSE",
        "short": "Connect urgent requests with donors",
        "color": RED,

        "problem":
            "During emergencies, families may lose valuable time "
            "searching for compatible blood donors.",

        "solution":
            "Match a request by blood group and urgency, show "
            "available sample donors and generate a clear "
            "emergency request.",

        "benefit":
            "A faster way to organize donor outreach when every "
            "minute matters.",
    },

    {
        "key": "clean",
        "code": "CLN",
        "title": "CLEAN CITY",
        "short": "Report and prioritize waste problems",
        "color": GREEN,

        "problem":
            "Overflowing bins, blocked drains and unmanaged waste "
            "can create health, safety and environmental problems.",

        "solution":
            "Submit a structured report, automatically classify "
            "its priority and track the response status.",

        "benefit":
            "More useful reports for city services and clearer "
            "visibility into unresolved problems.",
    },

    {
        "key": "food",
        "code": "FOD",
        "title": "FOOD RESCUE",
        "short": "Redirect safe surplus food",
        "color": "#F57C36",

        "problem":
            "Safe surplus food can be wasted while nearby people "
            "and organizations need food.",

        "solution":
            "Create a surplus listing with quantity, pickup time "
            "and safety information, then match it with a "
            "recipient organization.",

        "benefit":
            "Less avoidable waste and a more organized path from "
            "surplus food to people who can use it.",
    },

    {
        "key": "education",
        "code": "EDU",
        "title": "EDUCATION ACCESS",
        "short": "Find free learning resources",
        "color": "#4B8CFF",

        "problem":
            "Students may have motivation but lack access to "
            "organized, trustworthy learning resources.",

        "solution":
            "Choose a subject and level, then build a simple "
            "learning path with free resources and track progress.",

        "benefit":
            "A more structured starting point for students who "
            "need accessible learning materials.",
    },

    {
        "key": "water",
        "code": "WTR",
        "title": "WATER PROTECTION",
        "short": "Detect unusual water consumption",
        "color": CYAN,

        "problem":
            "Leaks can waste large amounts of water before "
            "anyone notices them.",

        "solution":
            "Compare meter readings over time, calculate "
            "consumption rate and flag unusual usage patterns.",

        "benefit":
            "Earlier investigation of possible leaks and better "
            "awareness of water consumption.",
    },
]


# ============================================================
# SOUND FEEDBACK
# ============================================================
# Small sounds provide immediate feedback when the user clicks
# buttons or when the application detects an important result.
#
# Windows users receive simple system beeps through winsound.
# On other operating systems the application simply continues
# without sound, so the program remains cross-platform.
# ============================================================

def beep(kind="click"):

    if platform.system() != "Windows":
        return

    try:

        import winsound

        if kind == "success":

            # Two rising tones communicate a successful action.
            winsound.Beep(700, 55)
            winsound.Beep(1000, 75)

        elif kind == "warning":

            # A different pattern communicates a warning.
            winsound.Beep(950, 100)
            winsound.Beep(600, 130)

        else:

            # Short click feedback.
            winsound.Beep(850, 35)

    except Exception:

        # Sound should never be allowed to crash the program.
        pass


# ============================================================
# MAIN APPLICATION CLASS
# ============================================================
# The entire application is organized inside one class.
#
# This keeps:
#   - user interface state
#   - selected module
#   - scores
#   - animations
#   - interactive tools
#
# organized in one central application object.
# ============================================================

class CivicShield:

    def __init__(self, root):

        # Store the main Tkinter window.
        self.root = root

        # Configure the application window.
        self.root.title(
            "CIVIC SHIELD // COMMUNITY IMPACT SYSTEM"
        )

        self.root.geometry("1240x780")
        self.root.minsize(980, 650)
        self.root.configure(bg=BG)


        # ----------------------------------------------------
        # APPLICATION STATE
        # ----------------------------------------------------
        # These variables remember what the user has done.
        # They allow the dashboard to show an evolving impact
        # score and achievements.
        # ----------------------------------------------------

        self.quote_index = 0

        self.radar_angle = 0

        self.screen = None

        # Index of the currently selected civic problem.
        self.selected = 0

        # Number of interactive actions completed.
        self.actions = 0

        # Demonstration impact score.
        self.impact = 0

        # Achievements earned by the user.
        self.achievements = set()

        # Stores references to the problem cards so their
        # appearance can be updated when selection changes.
        self.card_widgets = []


        # ----------------------------------------------------
        # TKINTER VISUAL STYLE
        # ----------------------------------------------------
        # ttk is used for the scrollbar because it gives us
        # a cleaner native-looking scrolling component.
        # ----------------------------------------------------

        self.style = ttk.Style()

        try:

            self.style.theme_use("clam")

        except tk.TclError:

            pass

        self.style.configure(
            "Vertical.TScrollbar",
            troughcolor="#091625",
            background="#24516D",
            bordercolor="#091625",
            arrowcolor="#9AB3C4",
        )


        # Start with the animated introduction screen.
        self.show_intro()


    # ========================================================
    # GENERAL UI HELPERS
    # ========================================================

    def clear(self):

        # Remove the previous screen before displaying a new one.
        #
        # This prevents old widgets from overlapping the new
        # screen and is important for keeping the animations and
        # navigation glitch-free.

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


    # ========================================================
    # IMPACT TRACKING
    # ========================================================
    # Every successful interaction contributes to the user's
    # demonstration impact score.
    #
    # This is a gamification feature. In a real application,
    # similar logic could be connected to verified community
    # activities rather than simulated actions.
    # ========================================================

    def add_action(self, points=50):

        # Increase the number of completed interactions.
        self.actions += 1

        # Increase the demonstration impact score.
        self.impact += points


        # ----------------------------------------------------
        # ACHIEVEMENT SYSTEM
        # ----------------------------------------------------
        # Users unlock badges as they interact with more
        # community solutions.
        # ----------------------------------------------------

        if self.actions >= 1:
            self.achievements.add("FIRST ACTION")

        if self.actions >= 5:
            self.achievements.add("COMMUNITY HELPER")

        if self.actions >= 10:
            self.achievements.add("CIVIC CHAMPION")


    # ========================================================
    # REUSABLE BUTTON CREATOR
    # ========================================================
    # A common button design is used throughout the program.
    # This keeps the user interface visually consistent.
    # ========================================================

    def button(
        self,
        parent,
        text,
        command,
        color=CYAN,
        width=20
    ):

        b = tk.Button(
            parent,

            text=text,

            # Run sound feedback before the selected action.
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

            padx=14,
            pady=9,
        )

        b.pack_propagate(False)

        return b


    # ========================================================
    # INTRODUCTION SCREEN
    # ========================================================
    # The intro is intentionally visual and simple.
    #
    # The goal is to immediately communicate:
    #   - this is a civic technology platform
    #   - the system is active
    #   - the project focuses on community impact
    #
    # The radar animation gives the interface a "live system"
    # feeling before the user enters the main dashboard.
    # ========================================================

    def show_intro(self):

        self.clear()

        tk.Label(
            self.screen,
            text="SECURE COMMUNITY NETWORK  //  CIVIC TECHNOLOGY",
            bg=BG,
            fg=MUTED,
            font=("Consolas", 11, "bold")
        ).pack(pady=(28, 5))


        # ----------------------------------------------------
        # ANIMATED RADAR / SHIELD
        # ----------------------------------------------------
        # This canvas contains the custom graphical animation.
        # Tkinter's Canvas allows us to draw shapes without
        # requiring external graphics libraries.
        # ----------------------------------------------------

        self.intro_canvas = tk.Canvas(
            self.screen,
            width=330,
            height=225,
            bg=BG,
            highlightthickness=0
        )

        self.intro_canvas.pack()

        self.radar_active = True

        # Start the continuous radar animation.
        self.animate_radar()


        # Main project title.
        tk.Label(
            self.screen,
            text="CIVIC SHIELD",
            bg=BG,
            fg=TEXT,
            font=("Arial", 42, "bold")
        ).pack()


        tk.Label(
            self.screen,
            text="COMMUNITY IMPACT CONTROL SYSTEM",
            bg=BG,
            fg=CYAN,
            font=("Consolas", 14, "bold")
        ).pack(pady=(3, 10))


        # ----------------------------------------------------
        # ROTATING SOCIAL-IMPACT QUOTE
        # ----------------------------------------------------
        # The quote changes automatically every few seconds.
        # This creates subtle motion without overwhelming the
        # user or interfering with navigation.
        # ----------------------------------------------------

        self.quote = tk.Label(
            self.screen,
            text=QUOTES[0],
            bg=BG,
            fg=MUTED,
            font=("Georgia", 14, "italic"),
            wraplength=850
        )

        self.quote.pack(pady=12)

        self.rotate_quote()


        tk.Label(
            self.screen,
            text="7 PROBLEMS  •  7 SOLUTIONS  •  ONE COMMUNITY",
            bg=BG,
            fg=GREEN,
            font=("Consolas", 11, "bold")
        ).pack(pady=12)


        # Main entry point into the application.
        self.button(
            self.screen,
            "ENTER CIVIC NETWORK  →",
            self.show_dashboard,
            CYAN,
            300
        ).pack(pady=8)


    # ========================================================
    # RADAR ANIMATION
    # ========================================================
    # The radar is drawn from scratch on a Canvas.
    #
    # Instead of using an animated image, the program
    # continuously changes the angle of a line. This demonstrates
    # that the interface itself is dynamically generated.
    # ========================================================

    def animate_radar(self):

        if not getattr(
            self,
            "radar_active",
            False
        ):
            return

        try:

            c = self.intro_canvas

            if not c.winfo_exists():
                return

            # Remove the previous animation frame.
            c.delete("all")

            cx = 165
            cy = 110


            # ------------------------------------------------
            # SHIELD OUTLINE
            # ------------------------------------------------
            # The shield visually represents protection,
            # responsibility and community safety.
            # ------------------------------------------------

            shield = [
                cx, 12,
                cx + 88, 48,
                cx + 72, 145,
                cx, 207,
                cx - 72, 145,
                cx - 88, 48
            ]

            c.create_polygon(
                shield,
                fill="#0B2030",
                outline=CYAN,
                width=3
            )


            # Radar rings.
            for r in (27, 52, 77):

                c.create_oval(
                    cx-r,
                    cy-r,
                    cx+r,
                    cy+r,
                    outline="#17465F"
                )


            # Convert the current angle to radians.
            angle = math.radians(
                self.radar_angle
            )


            # Calculate the radar endpoint.
            x = cx + math.cos(angle) * 77
            y = cy + math.sin(angle) * 77


            # Draw the rotating radar beam.
            c.create_line(
                cx,
                cy,
                x,
                y,
                fill=GREEN,
                width=3
            )


            # Crosshair lines.
            c.create_line(
                cx-77,
                cy,
                cx+77,
                cy,
                fill="#17465F"
            )

            c.create_line(
                cx,
                cy-77,
                cx,
                cy+77,
                fill="#17465F"
            )


            # Radar center point.
            c.create_oval(
                cx-5,
                cy-5,
                cx+5,
                cy+5,
                fill=CYAN,
                outline=""
            )


            # Advance the animation.
            self.radar_angle = (
                self.radar_angle + 6
            ) % 360


            # Schedule the next frame.
            #
            # Tkinter's after() method allows the animation to
            # run without blocking the rest of the interface.
            self.root.after(
                45,
                self.animate_radar
            )

        except tk.TclError:

            # If the window is closed while the animation is
            # running, quietly stop the animation.
            pass


    # ========================================================
    # QUOTE ROTATION
    # ========================================================
    # Automatically changes the motivational quote every
    # 4.5 seconds.
    # ========================================================

    def rotate_quote(self):

        try:

            if self.quote.winfo_exists():

                self.quote_index = (
                    self.quote_index + 1
                ) % len(QUOTES)

                self.quote.config(
                    text=QUOTES[
                        self.quote_index
                    ]
                )

                self.root.after(
                    4500,
                    self.rotate_quote
                )

        except tk.TclError:

            pass


    # ========================================================
    # MAIN DASHBOARD
    # ========================================================
    # This is the central navigation screen.
    #
    # LEFT SIDE:
    #   Scrollable list of civic problems.
    #
    # RIGHT SIDE:
    #   Detailed information and interactive solution button.
    #
    # This design means the user can browse many problems
    # without making the screen overcrowded.
    # ========================================================

    def show_dashboard(self):

        # Stop the intro radar when leaving the intro screen.
        self.radar_active = False

        self.clear()


        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = tk.Frame(
            self.screen,
            bg="#0A1A2A",
            height=76
        )

        header.pack(fill="x")
        header.pack_propagate(False)


        tk.Label(
            header,
            text="CIVIC SHIELD",
            bg="#0A1A2A",
            fg=TEXT,
            font=("Arial", 24, "bold")
        ).pack(
            side="left",
            padx=28
        )


        # Network indicator.
        tk.Label(
            header,
            text="● NETWORK ONLINE",
            bg="#0A1A2A",
            fg=GREEN,
            font=("Consolas", 10, "bold")
        ).pack(
            side="right",
            padx=28
        )


        body = tk.Frame(
            self.screen,
            bg=BG
        )

        body.pack(
            fill="both",
            expand=True
        )


        # ====================================================
        # LEFT SIDE: SCROLLABLE PROBLEM MENU
        # ====================================================
        # A Canvas + Scrollbar is used because Tkinter Frames
        # themselves do not provide scrolling.
        #
        # The result is a smooth, expandable problem list.
        # More modules can be added without redesigning the page.
        # ====================================================

        left = tk.Frame(
            body,
            bg=BG,
            width=470
        )

        left.pack(
            side="left",
            fill="y",
            padx=(22, 8),
            pady=18
        )

        left.pack_propagate(False)


        tk.Label(
            left,
            text="COMMUNITY PROBLEMS",
            bg=BG,
            fg=CYAN,
            font=("Consolas", 18, "bold")
        ).pack(anchor="w")


        tk.Label(
            left,
            text="Scroll through the problems and choose one.",
            bg=BG,
            fg=MUTED,
            font=("Arial", 10)
        ).pack(
            anchor="w",
            pady=(2, 10)
        )


        container = tk.Frame(
            left,
            bg="#081725"
        )

        container.pack(
            fill="both",
            expand=True
        )


        # Canvas is the scrolling surface.
        canvas = tk.Canvas(
            container,
            bg="#081725",
            highlightthickness=0,
            bd=0
        )


        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=canvas.yview,
            style="Vertical.TScrollbar"
        )


        # This Frame contains all of the problem cards.
        cards_frame = tk.Frame(
            canvas,
            bg="#081725"
        )


        # Insert the Frame inside the Canvas.
        window_id = canvas.create_window(
            (0, 0),
            window=cards_frame,
            anchor="nw"
        )


        # Update the scrolling area whenever the card list
        # changes size.
        def configure_frame(event):

            canvas.configure(
                scrollregion=canvas.bbox("all")
            )


        # Make the embedded Frame follow the Canvas width.
        def configure_canvas(event):

            canvas.itemconfigure(
                window_id,
                width=event.width
            )


        cards_frame.bind(
            "<Configure>",
            configure_frame
        )

        canvas.bind(
            "<Configure>",
            configure_canvas
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


        # ----------------------------------------------------
        # MOUSE WHEEL SUPPORT
        # ----------------------------------------------------
        # This lets users scroll naturally with their mouse
        # instead of needing to drag the scrollbar manually.
        # ----------------------------------------------------

        def wheel(event):

            canvas.yview_scroll(
                -1 if event.delta > 0 else 1,
                "units"
            )


        canvas.bind_all(
            "<MouseWheel>",
            wheel
        )


        # Create one interactive card for every civic problem.
        for i, module in enumerate(MODULES):

            self.make_problem_card(
                cards_frame,
                module,
                i
            )


        # ====================================================
        # RIGHT SIDE: DETAIL PANEL
        # ====================================================
        # This area changes whenever the user selects a problem.
        # It prevents the application from opening unnecessary
        # windows just to read basic information.
        # ====================================================

        self.detail = tk.Frame(
            body,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        self.detail.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(8, 22),
            pady=18
        )


        # Display the currently selected module.
        self.update_detail()


    # ========================================================
    # PROBLEM CARD CREATION
    # ========================================================
    # Each problem gets a custom card containing:
    #
    #   CODE
    #   TITLE
    #   SHORT DESCRIPTION
    #   ARROW
    #
    # The card responds to mouse hover and clicking.
    # ========================================================

    def make_problem_card(
        self,
        parent,
        module,
        index
    ):

        card = tk.Frame(
            parent,
            bg=CARD,
            height=105,
            cursor="hand2"
        )

        card.pack(
            fill="x",
            padx=10,
            pady=7
        )

        card.pack_propagate(False)


        # ----------------------------------------------------
        # VISUAL MODULE CODE
        # ----------------------------------------------------
        # Instead of emoji icons, each module uses a clean
        # technical code such as RAD, SIG, MED and WTR.
        # This gives the application a consistent professional
        # visual language.
        # ----------------------------------------------------

        icon = tk.Label(
            card,
            text=module["code"],
            bg=module["color"],
            fg=WHITE,
            font=("Consolas", 11, "bold"),
            width=6
        )

        icon.pack(
            side="left",
            fill="y",
            padx=(0, 12)
        )


        text = tk.Frame(
            card,
            bg=CARD
        )

        text.pack(
            side="left",
            fill="both",
            expand=True
        )


        title = tk.Label(
            text,
            text=module["title"],
            bg=CARD,
            fg=TEXT,
            font=("Consolas", 11, "bold"),
            anchor="w"
        )

        title.pack(
            fill="x",
            pady=(18, 2)
        )


        sub = tk.Label(
            text,
            text=module["short"],
            bg=CARD,
            fg=MUTED,
            font=("Arial", 9),
            anchor="w"
        )

        sub.pack(fill="x")


        arrow = tk.Label(
            card,
            text="›",
            bg=CARD,
            fg=module["color"],
            font=("Arial", 25)
        )

        arrow.pack(
            side="right",
            padx=15
        )


        widgets = [
            card,
            icon,
            text,
            title,
            sub,
            arrow
        ]


        # ----------------------------------------------------
        # HOVER ANIMATION
        # ----------------------------------------------------
        # The card changes background when the cursor moves
        # over it, giving the user a clear indication that the
        # card is interactive.
        # ----------------------------------------------------

        def enter(_=None):

            if index != self.selected:

                card.config(
                    bg=CARD_HOVER
                )

                text.config(
                    bg=CARD_HOVER
                )

                title.config(
                    bg=CARD_HOVER
                )

                sub.config(
                    bg=CARD_HOVER
                )

                arrow.config(
                    bg=CARD_HOVER
                )


        def leave(_=None):

            if index != self.selected:

                card.config(bg=CARD)
                text.config(bg=CARD)
                title.config(bg=CARD)
                sub.config(bg=CARD)
                arrow.config(bg=CARD)


        # ----------------------------------------------------
        # CARD SELECTION
        # ----------------------------------------------------
        # Clicking a card updates the selected problem and
        # refreshes the detail panel.
        # ----------------------------------------------------

        def select(_=None):

            beep()

            self.selected = index

            self.update_card_styles()

            self.update_detail()


        # Bind the same interaction to every visual element
        # inside the card, so the whole card feels clickable.
        for w in widgets:

            w.bind(
                "<Enter>",
                enter
            )

            w.bind(
                "<Leave>",
                leave
            )

            w.bind(
                "<Button-1>",
                select
            )


        self.card_widgets.append(
            (
                card,
                text,
                title,
                sub,
                arrow
            )
        )


    # ========================================================
    # UPDATE SELECTED CARD
    # ========================================================
    # The selected problem receives a different background,
    # making it easy to see which module is currently active.
    # ========================================================

    def update_card_styles(self):

        for i, widgets in enumerate(
            self.card_widgets
        ):

            card, text, title, sub, arrow = widgets

            bg = (
                "#163B52"
                if i == self.selected
                else CARD
            )

            card.config(bg=bg)
            text.config(bg=bg)
            title.config(bg=bg)
            sub.config(bg=bg)
            arrow.config(bg=bg)


    # ========================================================
    # DETAIL PANEL
    # ========================================================
    # Displays the selected problem's:
    #
    #   - title
    #   - problem
    #   - proposed solution
    #   - community benefit
    #   - user activity statistics
    #
    # This creates a simple "problem → solution → impact"
    # storytelling structure for the judges.
    # ========================================================

    def update_detail(self):

        # Remove previous content.
        for w in self.detail.winfo_children():
            w.destroy()


        m = MODULES[self.selected]


        top = tk.Frame(
            self.detail,
            bg=PANEL
        )

        top.pack(
            fill="x",
            padx=25,
            pady=25
        )


        # Module code.
        tk.Label(
            top,
            text=m["code"],
            bg=m["color"],
            fg=WHITE,
            font=("Consolas", 13, "bold"),
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

        title_box.pack(side="left")


        tk.Label(
            title_box,
            text=m["title"],
            bg=PANEL,
            fg=TEXT,
            font=("Arial", 22, "bold")
        ).pack(anchor="w")


        tk.Label(
            title_box,
            text=m["short"],
            bg=PANEL,
            fg=MUTED,
            font=("Arial", 10)
        ).pack(anchor="w")


        # Three major sections explain the civic problem.
        self.add_info_block(
            "WHY IT MATTERS",
            m["problem"],
            TEXT
        )

        self.add_info_block(
            "THE SOLUTION",
            m["solution"],
            CYAN
        )

        self.add_info_block(
            "COMMUNITY BENEFIT",
            m["benefit"],
            GREEN
        )


        # ----------------------------------------------------
        # USER IMPACT STATISTICS
        # ----------------------------------------------------
        # These demonstrate how a future civic platform could
        # track participation and engagement.
        # ----------------------------------------------------

        stats = tk.Frame(
            self.detail,
            bg="#081725"
        )

        stats.pack(
            fill="x",
            padx=25,
            pady=12
        )


        self.stat_label(
            stats,
            "ACTIONS",
            str(self.actions)
        ).pack(
            side="left",
            expand=True,
            pady=15
        )


        self.stat_label(
            stats,
            "IMPACT",
            str(self.impact)
        ).pack(
            side="left",
            expand=True
        )


        self.stat_label(
            stats,
            "BADGES",
            str(len(self.achievements))
        ).pack(
            side="left",
            expand=True
        )


        # Opens the interactive prototype for this problem.
        btn = self.button(
            self.detail,
            "OPEN INTERACTIVE SOLUTION  →",
            lambda: self.open_solution(m),
            m["color"],
            30
        )


        btn.config(height=45)

        btn.pack(pady=15)


        # Additional quote reinforces the project's message.
        tk.Label(
            self.detail,
            text=f'“{QUOTES[(self.selected + 2) % len(QUOTES)]}”',
            bg=PANEL,
            fg=MUTED,
            font=("Georgia", 11, "italic"),
            wraplength=600
        ).pack(pady=10)


    # ========================================================
    # INFORMATION BLOCK
    # ========================================================
    # Reusable component for the three explanatory sections
    # in the detail panel.
    # ========================================================

    def add_info_block(
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
            padx=25,
            pady=7
        )


        tk.Label(
            box,
            text=heading,
            bg=PANEL,
            fg=color,
            font=("Consolas", 10, "bold")
        ).pack(anchor="w")


        tk.Label(
            box,
            text=text,
            bg=PANEL,
            fg=MUTED,
            font=("Arial", 10),
            wraplength=650,
            justify="left",
            anchor="w"
        ).pack(
            anchor="w",
            pady=(3, 0)
        )


    # ========================================================
    # STATISTICS COMPONENT
    # ========================================================

    def stat_label(
        self,
        parent,
        title,
        value
    ):

        f = tk.Frame(
            parent,
            bg="#081725"
        )


        tk.Label(
            f,
            text=value,
            bg="#081725",
            fg=TEXT,
            font=("Consolas", 18, "bold")
        ).pack()


        tk.Label(
            f,
            text=title,
            bg="#081725",
            fg=MUTED,
            font=("Consolas", 8, "bold")
        ).pack()


        return f


    # ========================================================
    # SOLUTION ROUTER
    # ========================================================
    # Each problem has its own interactive demonstration.
    #
    # Instead of using one generic solution, this router sends
    # the user to a tool specifically designed around the
    # selected social problem.
    # ========================================================

    def open_solution(self, module):

        beep()


        if module["key"] == "road":

            self.road_solution(module)


        elif module["key"] == "traffic":

            self.traffic_solution(module)


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


    # ========================================================
    # REUSABLE SOLUTION WINDOW
    # ========================================================
    # Every interactive solution opens in a separate window.
    # This keeps the main dashboard stable while the user
    # experiments with a solution.
    # ========================================================

    def solution_window(self, module):

        w = tk.Toplevel(self.root)

        w.title(
            "CIVIC SHIELD // "
            + module["title"]
        )

        w.geometry("850x650")

        w.minsize(
            720,
            550
        )

        w.configure(
            bg=BG
        )


        header = tk.Frame(
            w,
            bg="#0A1A2A",
            height=75
        )

        header.pack(fill="x")
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
            pady=17
        )


        tk.Label(
            header,
            text=module["title"],
            bg="#0A1A2A",
            fg=TEXT,
            font=("Arial", 21, "bold")
        ).pack(
            side="left"
        )


        return w


    # ========================================================
    # ROAD SAFETY SOLUTION
    # ========================================================
    # Demonstrates how a road safety system could evaluate
    # vehicle speed against a configurable speed limit.
    #
    # A real deployment could receive this information from
    # sensors or legally authorized traffic systems.
    # ========================================================

    def road_solution(self, m):

        w = self.solution_window(m)


        content = tk.Frame(
            w,
            bg=BG
        )

        content.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=22
        )


        tk.Label(
            content,
            text="LIVE ROAD MONITOR",
            bg=BG,
            fg=CYAN,
            font=("Consolas", 15, "bold")
        ).pack(anchor="w")


        # ----------------------------------------------------
        # SIMULATED SENSOR DATA
        # ----------------------------------------------------
        # Random values are used only to make the prototype
        # feel dynamic. A real system would receive actual
        # sensor/camera data.
        # ----------------------------------------------------

        stats = tk.Frame(
            content,
            bg="#0B1B2B"
        )

        stats.pack(
            fill="x",
            pady=12
        )


        detected = random.randint(
            180,
            320
        )

        highrisk = random.randint(
            8,
            28
        )


        for label, value in [
            (
                "VEHICLES DETECTED",
                detected
            ),
            (
                "HIGH-RISK",
                highrisk
            ),
            (
                "AVG SPEED",
                "47 km/h"
            ),
        ]:

            f = tk.Frame(
                stats,
                bg="#0B1B2B"
            )

            f.pack(
                side="left",
                expand=True,
                pady=15
            )


            tk.Label(
                f,
                text=str(value),
                bg="#0B1B2B",
                fg=TEXT,
                font=("Consolas", 17, "bold")
            ).pack()


            tk.Label(
                f,
                text=label,
                bg="#0B1B2B",
                fg=MUTED,
                font=("Consolas", 8)
            ).pack()


        # ----------------------------------------------------
        # VEHICLE ANALYSIS INPUTS
        # ----------------------------------------------------

        form = tk.Frame(
            content,
            bg=BG
        )

        form.pack(
            fill="x",
            pady=5
        )


        entries = {}


        for label, default in [
            ("Vehicle plate", ""),
            ("Speed (km/h)", ""),
            ("Legal limit (km/h)", "50"),
        ]:

            tk.Label(
                form,
                text=label,
                bg=BG,
                fg=MUTED,
                font=("Arial", 9)
            ).pack(anchor="w")


            e = tk.Entry(
                form,
                bg="#10263A",
                fg=TEXT,
                insertbackground=TEXT,
                relief="flat",
                font=("Consolas", 11)
            )


            e.insert(
                0,
                default
            )


            e.pack(
                fill="x",
                pady=(2, 8)
            )


            entries[label] = e


        result = tk.Label(
            content,
            text="READY FOR VEHICLE ANALYSIS",
            bg=BG,
            fg=MUTED,
            font=("Consolas", 11),
            justify="left"
        )


        result.pack(
            anchor="w",
            pady=8
        )


        # ----------------------------------------------------
        # SPEED ANALYSIS ALGORITHM
        # ----------------------------------------------------
        # The program calculates:
        #
        #   excess speed
        #   risk score
        #   estimated example fine
        #
        # This demonstrates how raw input can be converted into
        # useful information for decision support.
        # ----------------------------------------------------

        def analyze():

            try:

                speed = float(
                    entries[
                        "Speed (km/h)"
                    ].get()
                )


                limit = float(
                    entries[
                        "Legal limit (km/h)"
                    ].get()
                )


                excess = speed - limit


                # Record this interaction.
                self.add_action(60)


                if excess <= 0:

                    result.config(
                        text=(
                            "✓ CLEAR\n"
                            "Vehicle is within "
                            "the configured speed limit."
                        ),
                        fg=GREEN
                    )


                    beep("success")


                else:

                    # Example risk formula for demonstration.
                    risk = min(
                        100,
                        35 + excess * 2
                    )


                    # Example value only; this is not a real
                    # legal fine calculation.
                    fine = (
                        500
                        + max(0, excess) * 100
                    )


                    result.config(
                        text=(
                            "⚠ VIOLATION DETECTED\n"
                            f"Excess speed: "
                            f"{excess:.1f} km/h\n"
                            f"Risk score: "
                            f"{risk:.0f}/100\n"
                            f"Estimated fine: "
                            f"{fine:.0f} BDT"
                        ),
                        fg=RED
                    )


                    beep("warning")


            except ValueError:

                result.config(
                    text="Enter valid numbers.",
                    fg=ORANGE
                )


        self.button(
            content,
            "ANALYZE VEHICLE",
            analyze,
            m["color"],
            25
        ).pack(
            anchor="w",
            pady=8
        )


        tk.Label(
            content,
            text=(
                "Safety guidance: slow down near schools, "
                "crossings and intersections; never use "
                "a phone while driving."
            ),
            bg=BG,
            fg=MUTED,
            font=("Arial", 9),
            wraplength=750,
            justify="left"
        ).pack(
            anchor="w",
            pady=10
        )


    # ========================================================
    # SMART TRAFFIC SOLUTION
    # ========================================================
    # Demonstrates proportional traffic signal allocation.
    #
    # The user enters the number of vehicles waiting in each
    # direction. The program gives larger queues more green
    # time.
    #
    # This demonstrates the basic concept behind adaptive
    # traffic management.
    # ========================================================

    def traffic_solution(self, m):

        w = self.solution_window(m)


        left = tk.Frame(
            w,
            bg=BG
        )

        left.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=20
        )


        tk.Label(
            left,
            text="ADAPTIVE INTERSECTION SIMULATOR",
            bg=BG,
            fg=CYAN,
            font=("Consolas", 15, "bold")
        ).pack(anchor="w")


        entries = {}


        # Create one input for each direction.
        for direction in (
            "North",
            "South",
            "East",
            "West"
        ):

            row = tk.Frame(
                left,
                bg=BG
            )

            row.pack(
                fill="x",
                pady=4
            )


            tk.Label(
                row,
                text=direction,
                width=10,
                bg=BG,
                fg=TEXT,
                font=("Consolas", 10)
            ).pack(
                side="left"
            )


            e = tk.Entry(
                row,
                bg="#10263A",
                fg=TEXT,
                insertbackground=TEXT,
                relief="flat"
            )


            # Random starting data makes the simulator ready
            # immediately when it opens.
            e.insert(
                0,
                str(random.randint(5, 50))
            )


            e.pack(
                side="left",
                fill="x",
                expand=True
            )


            entries[direction] = e


        result = tk.Text(
            left,
            height=9,
            bg="#081725",
            fg=TEXT,
            relief="flat",
            font=("Consolas", 10)
        )


        result.pack(
            fill="both",
            expand=True,
            pady=15
        )


        def optimize():

            try:

                # Convert user input into integer vehicle counts.
                counts = {
                    d: int(e.get())
                    for d, e in entries.items()
                }


                total = sum(
                    counts.values()
                )


                if total <= 0:
                    raise ValueError


                result.delete(
                    "1.0",
                    "end"
                )


                result.insert(
                    "end",
                    "ADAPTIVE SIGNAL PLAN\n"
                    "────────────────────────────\n"
                )


                # Give each direction a proportion of a
                # 90-second cycle according to queue size.
                for d, count in counts.items():

                    seconds = max(
                        8,
                        round(
                            count / total * 90
                        )
                    )


                    result.insert(
                        "end",
                        f"{d:<8} "
                        f"{count:>3} vehicles  "
                        f"→  {seconds:>2}s GREEN\n"
                    )


                result.insert(
                    "end",
                    "\nRecommendation: prioritize "
                    "the direction with the longest queue."
                )


                self.add_action(75)

                beep("success")


            except ValueError:

                messagebox.showwarning(
                    "Invalid traffic data",
                    "Enter whole numbers "
                    "for vehicle counts.",
                    parent=w
                )


        self.button(
            left,
            "OPTIMIZE SIGNAL TIMING",
            optimize,
            m["color"],
            28
        ).pack(anchor="w")


    # ========================================================
    # BLOOD RESPONSE SOLUTION
    # ========================================================
    # Demonstrates a simplified blood-group matching concept.
    #
    # NOTE:
    # The displayed names are demonstration data, not a real
    # donor database. Real medical matching must be handled by
    # qualified professionals and verified medical systems.
    # ========================================================

    def blood_solution(self, m):

        w = self.solution_window(m)


        frame = tk.Frame(
            w,
            bg=BG
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )


        donors = {

            "O-": [
                "Ayesha Rahman"
            ],

            "O+": [
                "Nusrat Jahan",
                "Imran Ali"
            ],

            "A-": [
                "Community Donor Network"
            ],

            "A+": [
                "Tanvir Alam",
                "Sadia Noor"
            ],

            "B-": [
                "Emergency Donor Network"
            ],

            "B+": [
                "Farhana Kabir"
            ],

            "AB-": [
                "Regional Donor Network"
            ],

            "AB+": [
                "Rafiq Islam"
            ],
        }


        tk.Label(
            frame,
            text="EMERGENCY BLOOD MATCH",
            bg=BG,
            fg=CYAN,
            font=("Consolas", 15, "bold")
        ).pack(anchor="w")


        row = tk.Frame(
            frame,
            bg=BG
        )

        row.pack(
            fill="x",
            pady=20
        )


        blood = tk.StringVar(
            value="O+"
        )


        urgency = tk.StringVar(
            value="URGENT"
        )


        tk.Label(
            row,
            text="Blood group",
            bg=BG,
            fg=MUTED
        ).pack(
            side="left"
        )


        tk.OptionMenu(
            row,
            blood,
            *donors.keys()
        ).pack(
            side="left",
            padx=10
        )


        tk.Label(
            row,
            text="Urgency",
            bg=BG,
            fg=MUTED
        ).pack(
            side="left",
            padx=(25, 0)
        )


        tk.OptionMenu(
            row,
            urgency,
            "CRITICAL",
            "URGENT",
            "NORMAL"
        ).pack(
            side="left",
            padx=10
        )


        result = tk.Label(
            frame,
            text="No request active.",
            bg=BG,
            fg=MUTED,
            font=("Consolas", 11),
            justify="left"
        )


        result.pack(
            anchor="w",
            pady=20
        )


        def match():

            group = blood.get()

            names = donors.get(
                group,
                []
            )


            # Record a successful interaction.
            self.add_action(100)


            result.config(
                text=(
                    f"REQUEST: "
                    f"{urgency.get()}\n"
                    f"REQUIRED GROUP: "
                    f"{group}\n\n"
                    "Potential matches:\n"
                    + "\n".join(
                        "• " + n
                        for n in names
                    )
                    + "\n\nNext step: contact "
                    "the donor/network and verify eligibility."
                ),
                fg=GREEN
            )


            beep("success")


        self.button(
            frame,
            "FIND COMPATIBLE DONORS",
            match,
            m["color"],
            30
        ).pack(
            anchor="w"
        )


    # ========================================================
    # CLEAN CITY SOLUTION
    # ========================================================
    # Allows a user to submit a simulated city-service report.
    #
    # The application analyzes keywords to assign an example
    # priority level.
    #
    # In a real system this could be expanded using:
    #   - GPS coordinates
    #   - photographs
    #   - municipal databases
    #   - duplicate-report detection
    #   - status tracking
    # ========================================================

    def clean_solution(self, m):

        w = self.solution_window(m)


        frame = tk.Frame(
            w,
            bg=BG
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=20
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
            bg="#10263A",
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
            pady=10
        )


        desc = tk.Text(
            frame,
            height=7,
            bg="#10263A",
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat"
        )


        desc.pack(
            fill="both",
            expand=True
        )


        result = tk.Label(
            frame,
            text="Report ready.",
            bg=BG,
            fg=MUTED,
            font=("Consolas", 10),
            justify="left"
        )


        result.pack(
            anchor="w",
            pady=12
        )


        def report():

            text = desc.get(
                "1.0",
                "end"
            ).lower()


            if not location.get().strip():
                return


            # ------------------------------------------------
            # SIMPLE PRIORITY CLASSIFICATION
            # ------------------------------------------------
            # This is a rule-based prototype. A production
            # version could use a trained classification model
            # or a municipal workflow engine.
            # ------------------------------------------------

            if any(
                x in text
                for x in (
                    "medical",
                    "hazard",
                    "overflow",
                    "blocked drain"
                )
            ):

                priority = "CRITICAL"


            elif any(
                x in text
                for x in (
                    "smell",
                    "garbage",
                    "blocked",
                    "waste"
                )
            ):

                priority = "HIGH"


            else:

                priority = "NORMAL"


            self.add_action(70)


            # Generate a demonstration tracking number.
            ticket = (
                f"CS-{random.randint(10000, 99999)}"
            )


            result.config(
                text=(
                    "REPORT SUBMITTED\n"
                    f"Ticket: {ticket}\n"
                    f"Priority: {priority}\n"
                    "Status: QUEUED FOR REVIEW"
                ),
                fg=GREEN
            )


            beep("success")


        self.button(
            frame,
            "SUBMIT CITY REPORT",
            report,
            m["color"],
            28
        ).pack(
            anchor="w"
        )


    # ========================================================
    # FOOD RESCUE SOLUTION
    # ========================================================
    # Demonstrates how surplus food could be listed and
    # connected with a potential community organization.
    #
    # The goal is to reduce unnecessary waste while creating
    # an organized process for redistribution.
    # ========================================================

    def food_solution(self, m):

        w = self.solution_window(m)


        frame = tk.Frame(
            w,
            bg=BG
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=20
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

            (
                "Food item",
                "Cooked rice / meals"
            ),

            (
                "Quantity",
                "25 portions"
            ),

            (
                "Pickup time",
                "Within 2 hours"
            ),

        ]:

            tk.Label(
                frame,
                text=label,
                bg=BG,
                fg=MUTED
            ).pack(
                anchor="w",
                pady=(10, 2)
            )


            e = tk.Entry(
                frame,
                bg="#10263A",
                fg=TEXT,
                insertbackground=TEXT,
                relief="flat"
            )


            e.insert(
                0,
                default
            )


            e.pack(
                fill="x"
            )


            fields[label] = e


        result = tk.Label(
            frame,
            text="No listing created.",
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

            # Simulate finding a nearby organization.
            recipient = random.choice(
                [
                    "Community Kitchen",
                    "Local Food Support Group",
                    "Neighborhood Relief Center"
                ]
            )


            self.add_action(80)


            result.config(
                text=(
                    "LISTING CREATED\n"
                    f"Item: "
                    f"{fields['Food item'].get()}\n"
                    f"Quantity: "
                    f"{fields['Quantity'].get()}\n"
                    f"Pickup: "
                    f"{fields['Pickup time'].get()}\n"
                    f"Suggested recipient: "
                    f"{recipient}\n\n"
                    "Reminder: only redistribute food "
                    "that is safe and legally appropriate to donate."
                ),
                fg=GREEN
            )


            beep("success")


        self.button(
            frame,
            "MATCH WITH RECIPIENT",
            match,
            m["color"],
            28
        ).pack(
            anchor="w"
        )


    # ========================================================
    # EDUCATION ACCESS SOLUTION
    # ========================================================
    # Creates a simple personalized learning path.
    #
    # The user selects a subject and can mark topics complete.
    # This demonstrates how a civic platform can move beyond
    # simply displaying information and actually involve users.
    # ========================================================

    def education_solution(self, m):

        w = self.solution_window(m)


        frame = tk.Frame(
            w,
            bg=BG
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=20
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


        # Example learning paths.
        subjects = {

            "Programming": [
                "Python fundamentals",
                "Problem solving",
                "Data structures",
                "Build a small project"
            ],

            "Mathematics": [
                "Algebra foundations",
                "Functions",
                "Geometry",
                "Practice problems"
            ],

            "Science": [
                "Core concepts",
                "Experiments",
                "Data interpretation",
                "Revision quiz"
            ],

            "English": [
                "Vocabulary",
                "Grammar",
                "Listening",
                "Speaking practice"
            ]

        }


        subject = tk.StringVar(
            value="Programming"
        )


        tk.OptionMenu(
            frame,
            subject,
            *subjects.keys()
        ).pack(
            anchor="w",
            pady=15
        )


        listbox = tk.Listbox(
            frame,
            bg="#10263A",
            fg=TEXT,
            selectbackground="#24516D",
            relief="flat",
            font=("Consolas", 11)
        )


        listbox.pack(
            fill="both",
            expand=True
        )


        progress = tk.IntVar(
            value=0
        )


        # ----------------------------------------------------
        # REFRESH LEARNING PATH
        # ----------------------------------------------------

        def refresh():

            listbox.delete(
                0,
                "end"
            )


            for item in subjects[
                subject.get()
            ]:

                listbox.insert(
                    "end",
                    "□ " + item
                )


        # ----------------------------------------------------
        # COMPLETE TOPIC
        # ----------------------------------------------------
        # A completed topic contributes to progress and
        # demonstrates user engagement.
        # ----------------------------------------------------

        def complete():

            selection = listbox.curselection()


            if not selection:
                return


            idx = selection[0]


            old = listbox.get(idx)


            if old.startswith("□"):

                listbox.delete(idx)


                listbox.insert(
                    idx,
                    "✓ " + old[2:]
                )


                # Four topics = approximately 25% each.
                progress.set(
                    min(
                        100,
                        progress.get() + 25
                    )
                )


                self.add_action(45)


                beep("success")


            result.config(
                text=(
                    f"LEARNING PATH PROGRESS: "
                    f"{progress.get()}%"
                ),
                fg=GREEN
            )


        # Automatically rebuild the list when the subject
        # selection changes.
        subject.trace_add(
            "write",
            lambda *_: refresh()
        )


        refresh()


        result = tk.Label(
            frame,
            text="LEARNING PATH PROGRESS: 0%",
            bg=BG,
            fg=MUTED,
            font=("Consolas", 10)
        )


        result.pack(
            anchor="w",
            pady=10
        )


        self.button(
            frame,
            "MARK SELECTED TOPIC COMPLETE",
            complete,
            m["color"],
            32
        ).pack(
            anchor="w"
        )


    # ========================================================
    # WATER PROTECTION SOLUTION
    # ========================================================
    # Calculates water consumption rate and flags unusually
    # high usage.
    #
    # This demonstrates how simple measurements can be turned
    # into an early-warning system.
    #
    # A production system could connect this concept to smart
    # water meters and historical consumption databases.
    # ========================================================

    def water_solution(self, m):

        w = self.solution_window(m)


        frame = tk.Frame(
            w,
            bg=BG
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=20
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


        for label, default in [

            (
                "Previous meter reading (L)",
                "1000"
            ),

            (
                "Current meter reading (L)",
                "1080"
            ),

            (
                "Hours elapsed",
                "24"
            ),

        ]:

            tk.Label(
                frame,
                text=label,
                bg=BG,
                fg=MUTED
            ).pack(
                anchor="w",
                pady=(9, 2)
            )


            e = tk.Entry(
                frame,
                bg="#10263A",
                fg=TEXT,
                insertbackground=TEXT,
                relief="flat"
            )


            e.insert(
                0,
                default
            )


            e.pack(
                fill="x"
            )


            entries[label] = e


        result = tk.Label(
            frame,
            text="Scanner ready.",
            bg=BG,
            fg=MUTED,
            font=("Consolas", 11),
            justify="left"
        )


        result.pack(
            anchor="w",
            pady=20
        )


        def scan():

            try:

                old = float(
                    entries[
                        "Previous meter reading (L)"
                    ].get()
                )


                new = float(
                    entries[
                        "Current meter reading (L)"
                    ].get()
                )


                hours = float(
                    entries[
                        "Hours elapsed"
                    ].get()
                )


                # Prevent impossible readings.
                if hours <= 0 or new < old:

                    raise ValueError


                # Calculate consumption rate.
                rate = (
                    (new - old)
                    / hours
                )


                self.add_action(65)


                # ------------------------------------------------
                # SIMPLE LEAK DETECTION RULE
                # ------------------------------------------------
                # This threshold is a prototype value, not a
                # universal definition of a water leak.
                # ------------------------------------------------

                if rate > 5:

                    result.config(
                        text=(
                            "⚠ POSSIBLE LEAK DETECTED\n"
                            f"Consumption: "
                            f"{new-old:.1f} L\n"
                            f"Rate: "
                            f"{rate:.2f} L/hour\n\n"
                            "Recommendation: inspect taps, "
                            "toilets, pipes and outdoor lines."
                        ),
                        fg=RED
                    )


                    beep("warning")


                else:

                    result.config(
                        text=(
                            "✓ USAGE APPEARS NORMAL\n"
                            f"Consumption: "
                            f"{new-old:.1f} L\n"
                            f"Rate: "
                            f"{rate:.2f} L/hour\n\n"
                            "Continue monitoring for sudden changes."
                        ),
                        fg=GREEN
                    )


                    beep("success")


            except ValueError:

                result.config(
                    text=(
                        "Enter valid positive readings "
                        "and elapsed hours."
                    ),
                    fg=ORANGE
                )


        self.button(
            frame,
            "RUN LEAK ANALYSIS",
            scan,
            m["color"],
            28
        ).pack(
            anchor="w"
        )


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================
# Python starts executing here.
#
# Tk() creates the main application window.
# CivicShield(root) creates our application.
# mainloop() keeps the interface running and listens for
# user interactions such as clicks, scrolling and typing.
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = CivicShield(root)

    root.mainloop()