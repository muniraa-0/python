import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import platform
import time
from datetime import datetime

# ============================================================
# CIVIC SHIELD
# Interactive Civic Problems & Solutions Platform
#
# Built with the Python standard library only (tkinter) so it
# runs anywhere without extra installs - handy for a quick demo
# on competition day.
#
# Note to self: the traffic module got a big rework so it plays
# nicer for an actual officer standing at an intersection - a
# manual override matters more in real life than a perfect
# algorithm, since a human on the ground always outranks the
# math. Also added a little decorative flower planter at the
# bottom of the home screen, just because a bit of warmth never
# hurts a "civic" project.
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

QUOTES = [
    "Small actions can create big changes.",
    "Technology becomes meaningful when it improves lives.",
    "A safer community begins with one responsible action.",
    "The future is built by the problems we choose to solve.",
    "Every solved problem is a stronger community.",
]

MODULES = [
    {
        "key": "road",
        "code": "RAD",
        "title": "ROAD SAFETY",
        "short": "Reduce speeding and accident risks",
        "color": RED,
        "problem": "Speeding, dangerous driving and poor road awareness increase the chance and severity of crashes.",
        "solution": "Use a community safety center to analyze reported speeds, calculate risk, identify repeat hazards and provide targeted safety guidance.",
        "benefit": "Faster identification of dangerous behavior and better awareness around schools, crossings and busy intersections.",
    },
    {
        "key": "traffic",
        "code": "SIG",
        "title": "SMART TRAFFIC",
        "short": "Reduce congestion and waiting time",
        "color": ORANGE,
        "problem": "Fixed traffic timing can waste road capacity when one direction is crowded and another is nearly empty.",
        "solution": "Use live vehicle counts to create an adaptive signal plan that gives more green time to heavier queues.",
        "benefit": "Less unnecessary waiting, more balanced intersections and a clearer picture of where congestion is forming.",
    },
    {
        "key": "blood",
        "code": "MED",
        "title": "BLOOD RESPONSE",
        "short": "Connect urgent requests with donors",
        "color": RED,
        "problem": "During emergencies, families may lose valuable time searching for compatible blood donors.",
        "solution": "Match a request by blood group and urgency, show available sample donors and generate a clear emergency request.",
        "benefit": "A faster way to organize donor outreach when every minute matters.",
    },
    {
        "key": "clean",
        "code": "CLN",
        "title": "CLEAN CITY",
        "short": "Report and prioritize waste problems",
        "color": GREEN,
        "problem": "Overflowing bins, blocked drains and unmanaged waste can create health, safety and environmental problems.",
        "solution": "Submit a structured report, automatically classify its priority and track the response status.",
        "benefit": "More useful reports for city services and clearer visibility into unresolved problems.",
    },
    {
        "key": "food",
        "code": "FOD",
        "title": "FOOD RESCUE",
        "short": "Redirect safe surplus food",
        "color": "#F57C36",
        "problem": "Safe surplus food can be wasted while nearby people and organizations need food.",
        "solution": "Create a surplus listing with quantity, pickup time and safety information, then match it with a recipient organization.",
        "benefit": "Less avoidable waste and a more organized path from surplus food to people who can use it.",
    },
    {
        "key": "education",
        "code": "EDU",
        "title": "EDUCATION ACCESS",
        "short": "Find free learning resources",
        "color": "#4B8CFF",  # a calmer sky blue for the education card
        "problem": "Students may have motivation but lack access to organized, trustworthy learning resources.",
        "solution": "Choose a subject and level, then build a simple learning path with free resources and track progress.",
        "benefit": "A more structured starting point for students who need accessible learning materials.",
    },
    {
        "key": "water",
        "code": "WTR",
        "title": "WATER PROTECTION",
        "short": "Detect unusual water consumption",
        "color": CYAN,
        "problem": "Leaks can waste large amounts of water before anyone notices them.",
        "solution": "Compare meter readings over time, calculate consumption rate and flag unusual usage patterns.",
        "benefit": "Earlier investigation of possible leaks and better awareness of water consumption.",
    },
]


def beep(kind="click"):
    if platform.system() != "Windows":
        return
    try:
        import winsound
        if kind == "success":
            winsound.Beep(700, 55)
            winsound.Beep(1000, 75)
        elif kind == "warning":
            winsound.Beep(950, 100)
            winsound.Beep(600, 130)
        else:
            winsound.Beep(850, 35)
    except Exception:
        pass


class CivicShield:
    def __init__(self, root):
        self.root = root
        self.root.title("CIVIC SHIELD // COMMUNITY IMPACT SYSTEM")
        self.root.geometry("1240x780")
        self.root.minsize(980, 650)
        self.root.configure(bg=BG)

        self.quote_index = 0
        self.radar_angle = 0
        self.screen = None
        self.selected = 0
        self.actions = 0
        self.impact = 0
        self.achievements = set()
        self.status_text = "SYSTEM READY"
        self.card_widgets = []

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

        self.show_intro()

    # --------------------------------------------------------
    # Utility
    # --------------------------------------------------------

    def clear(self):
        if self.screen is not None:
            self.screen.destroy()
        self.screen = tk.Frame(self.root, bg=BG)
        self.screen.pack(fill="both", expand=True)

    def add_action(self, points=50):
        self.actions += 1
        self.impact += points
        if self.actions >= 1:
            self.achievements.add("FIRST ACTION")
        if self.actions >= 5:
            self.achievements.add("COMMUNITY HELPER")
        if self.actions >= 10:
            self.achievements.add("CIVIC CHAMPION")

    def button(self, parent, text, command, color=CYAN, width=20):
        b = tk.Button(
            parent,
            text=text,
            command=lambda: (beep(), command()),
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

    def dark_dropdown(self, parent, variable, options):
        """A tk.OptionMenu re-skinned to match the dark theme.

        The stock OptionMenu is grey and sticks out like a sore
        thumb against everything else in this app, so we push a
        few colors into it after it's built.
        """
        menu = tk.OptionMenu(parent, variable, *options)
        menu.config(
            bg=CARD, fg=TEXT,
            activebackground=CARD_HOVER, activeforeground=TEXT,
            highlightthickness=0, relief="flat",
            font=("Consolas", 10, "bold"),
            padx=10, pady=4,
            cursor="hand2",
        )
        menu["menu"].config(
            bg=CARD, fg=TEXT,
            activebackground=CARD_HOVER, activeforeground=WHITE,
            font=("Consolas", 10),
        )
        return menu

    def draw_flower_planter(self, parent, width=760, height=110):
        """Purely decorative - a little row of flowers in a planter box.

        Nothing functional here, it's just a nicer way to end the
        screen than dead empty space. Petals are simple ovals
        around a center dot, drawn a few times with different
        colors and positions so it doesn't look copy-pasted.
        """
        c = tk.Canvas(parent, width=width, height=height, bg=BG, highlightthickness=0)

        petal_colors = [RED, ORANGE, "#FF8FB8", PURPLE, CYAN, GREEN]
        stem_y = height - 26
        box_top = height - 26
        box_bottom = height - 4

        # the planter box itself
        c.create_rectangle(
            width * 0.10, box_top, width * 0.90, box_bottom,
            fill="#3B2A1E", outline="#5C4531", width=2
        )
        c.create_rectangle(
            width * 0.08, box_top - 4, width * 0.92, box_top,
            fill="#4A3625", outline="#5C4531"
        )

        flower_count = 9
        span_left = width * 0.14
        span_right = width * 0.86
        for i in range(flower_count):
            fx = span_left + (span_right - span_left) * (i / (flower_count - 1))
            fx += random.uniform(-6, 6)
            fy = stem_y - random.randint(34, 58)
            color = petal_colors[i % len(petal_colors)]

            # a slightly wavy stem instead of a dead straight line
            mid_x = fx + random.uniform(-5, 5)
            c.create_line(
                fx, stem_y, mid_x, (fy + stem_y) / 2, fx, fy,
                fill="#3F9C5B", width=3, smooth=True
            )
            # a couple of little leaves
            c.create_oval(fx - 12, stem_y - 18, fx - 2, stem_y - 10, fill="#3F9C5B", outline="")
            c.create_oval(fx + 2, stem_y - 26, fx + 12, stem_y - 18, fill="#4CB56B", outline="")

            # petals around a center
            petal_r = random.randint(7, 9)
            for angle in range(0, 360, 60):
                rad = math.radians(angle)
                px = fx + math.cos(rad) * petal_r
                py = fy + math.sin(rad) * petal_r
                c.create_oval(
                    px - 6, py - 6, px + 6, py + 6,
                    fill=color, outline=""
                )
            c.create_oval(fx - 5, fy - 5, fx + 5, fy + 5, fill=ORANGE, outline="")

        return c

    # --------------------------------------------------------
    # Intro
    # --------------------------------------------------------

    def show_intro(self):
        self.clear()

        top = tk.Label(
            self.screen,
            text="SECURE COMMUNITY NETWORK  //  CIVIC TECHNOLOGY",
            bg=BG, fg=MUTED, font=("Consolas", 11, "bold")
        )
        top.pack(pady=(28, 5))

        self.intro_canvas = tk.Canvas(
            self.screen, width=330, height=225,
            bg=BG, highlightthickness=0
        )
        self.intro_canvas.pack()

        self.radar_active = True
        self.animate_radar()

        tk.Label(
            self.screen, text="CIVIC SHIELD",
            bg=BG, fg=TEXT, font=("Arial", 42, "bold")
        ).pack()

        tk.Label(
            self.screen, text="COMMUNITY IMPACT CONTROL SYSTEM",
            bg=BG, fg=CYAN, font=("Consolas", 14, "bold")
        ).pack(pady=(3, 10))

        self.quote = tk.Label(
            self.screen, text=QUOTES[0],
            bg=BG, fg=MUTED,
            font=("Georgia", 14, "italic"),
            wraplength=850
        )
        self.quote.pack(pady=12)
        self.rotate_quote()

        tk.Label(
            self.screen,
            text="7 PROBLEMS  •  7 SOLUTIONS  •  ONE COMMUNITY",
            bg=BG, fg=GREEN,
            font=("Consolas", 11, "bold")
        ).pack(pady=12)

        self.button(
            self.screen,
            "ENTER CIVIC NETWORK  →",
            self.show_dashboard,
            CYAN,
            300
        ).pack(pady=8)

        # a small decorative touch so the welcome screen doesn't
        # end so abruptly
        self.draw_flower_planter(self.screen, width=520, height=90).pack(pady=(14, 6))

    def animate_radar(self):
        if not getattr(self, "radar_active", False):
            return
        try:
            c = self.intro_canvas
            if not c.winfo_exists():
                return
            c.delete("all")
            cx, cy = 165, 110

            shield = [
                cx, 12, cx + 88, 48, cx + 72, 145,
                cx, 207, cx - 72, 145, cx - 88, 48
            ]
            c.create_polygon(
                shield, fill="#0B2030", outline=CYAN, width=3
            )

            for r in (27, 52, 77):
                c.create_oval(
                    cx-r, cy-r, cx+r, cy+r,
                    outline="#17465F"
                )

            angle = math.radians(self.radar_angle)
            x = cx + math.cos(angle) * 77
            y = cy + math.sin(angle) * 77

            c.create_line(cx, cy, x, y, fill=GREEN, width=3)
            c.create_line(cx-77, cy, cx+77, cy, fill="#17465F")
            c.create_line(cx, cy-77, cx, cy+77, fill="#17465F")
            c.create_oval(cx-5, cy-5, cx+5, cy+5, fill=CYAN, outline="")

            self.radar_angle = (self.radar_angle + 6) % 360
            self.root.after(45, self.animate_radar)
        except tk.TclError:
            pass

    def rotate_quote(self):
        try:
            if self.quote.winfo_exists():
                self.quote_index = (self.quote_index + 1) % len(QUOTES)
                self.quote.config(text=QUOTES[self.quote_index])
                self.root.after(4500, self.rotate_quote)
        except tk.TclError:
            pass

    # --------------------------------------------------------
    # Dashboard
    # --------------------------------------------------------

    def show_dashboard(self):
        self.radar_active = False
        self.clear()

        header = tk.Frame(self.screen, bg="#0A1A2A", height=76)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="CIVIC SHIELD",
            bg="#0A1A2A", fg=TEXT,
            font=("Arial", 24, "bold")
        ).pack(side="left", padx=28)

        tk.Label(
            header, text="● NETWORK ONLINE",
            bg="#0A1A2A", fg=GREEN,
            font=("Consolas", 10, "bold")
        ).pack(side="right", padx=28)

        body = tk.Frame(self.screen, bg=BG)
        body.pack(fill="both", expand=True)

        # Left: stable scroll area
        left = tk.Frame(body, bg=BG, width=470)
        left.pack(side="left", fill="y", padx=(22, 8), pady=18)
        left.pack_propagate(False)

        tk.Label(
            left, text="COMMUNITY PROBLEMS",
            bg=BG, fg=CYAN,
            font=("Consolas", 18, "bold")
        ).pack(anchor="w")

        tk.Label(
            left, text="Scroll through the problems and choose one.",
            bg=BG, fg=MUTED,
            font=("Arial", 10)
        ).pack(anchor="w", pady=(2, 10))

        container = tk.Frame(left, bg="#081725")
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            container, bg="#081725",
            highlightthickness=0, bd=0
        )
        scrollbar = ttk.Scrollbar(
            container, orient="vertical",
            command=canvas.yview,
            style="Vertical.TScrollbar"
        )

        cards_frame = tk.Frame(canvas, bg="#081725")

        window_id = canvas.create_window(
            (0, 0), window=cards_frame, anchor="nw"
        )

        def configure_frame(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def configure_canvas(event):
            canvas.itemconfigure(
                window_id, width=event.width
            )

        cards_frame.bind("<Configure>", configure_frame)
        canvas.bind("<Configure>", configure_canvas)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def wheel(event):
            canvas.yview_scroll(
                -1 if event.delta > 0 else 1,
                "units"
            )

        canvas.bind_all("<MouseWheel>", wheel)

        for i, module in enumerate(MODULES):
            self.make_problem_card(
                cards_frame, module, i
            )

        # Right detail panel
        self.detail = tk.Frame(
            body, bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        self.detail.pack(
            side="left", fill="both", expand=True,
            padx=(8, 22), pady=18
        )

        self.update_detail()

        footer = tk.Frame(self.screen, bg=BG)
        footer.pack(fill="x", side="bottom")
        self.draw_flower_planter(footer, width=1240, height=70).pack()

    def make_problem_card(self, parent, module, index):
        card = tk.Frame(
            parent,
            bg=CARD,
            height=105,
            cursor="hand2"
        )
        card.pack(fill="x", padx=10, pady=7)
        card.pack_propagate(False)

        icon = tk.Label(
            card,
            text=module["code"],
            bg=module["color"],
            fg=WHITE,
            font=("Consolas", 11, "bold"),
            width=6
        )
        icon.pack(side="left", fill="y", padx=(0, 12))

        text = tk.Frame(card, bg=CARD)
        text.pack(side="left", fill="both", expand=True)

        title = tk.Label(
            text, text=module["title"],
            bg=CARD, fg=TEXT,
            font=("Consolas", 11, "bold"),
            anchor="w"
        )
        title.pack(fill="x", pady=(18, 2))

        sub = tk.Label(
            text, text=module["short"],
            bg=CARD, fg=MUTED,
            font=("Arial", 9),
            anchor="w"
        )
        sub.pack(fill="x")

        arrow = tk.Label(
            card, text="›",
            bg=CARD, fg=module["color"],
            font=("Arial", 25)
        )
        arrow.pack(side="right", padx=15)

        widgets = [card, icon, text, title, sub, arrow]

        def enter(_=None):
            if index != self.selected:
                card.config(bg=CARD_HOVER)
                text.config(bg=CARD_HOVER)
                title.config(bg=CARD_HOVER)
                sub.config(bg=CARD_HOVER)
                arrow.config(bg=CARD_HOVER)

        def leave(_=None):
            if index != self.selected:
                card.config(bg=CARD)
                text.config(bg=CARD)
                title.config(bg=CARD)
                sub.config(bg=CARD)
                arrow.config(bg=CARD)

        def select(_=None):
            beep()
            self.selected = index
            self.update_card_styles()
            self.update_detail()

        for w in widgets:
            w.bind("<Enter>", enter)
            w.bind("<Leave>", leave)
            w.bind("<Button-1>", select)

        self.card_widgets.append((card, text, title, sub, arrow))

    def update_card_styles(self):
        for i, widgets in enumerate(self.card_widgets):
            card, text, title, sub, arrow = widgets
            bg = "#163B52" if i == self.selected else CARD
            card.config(bg=bg)
            text.config(bg=bg)
            title.config(bg=bg)
            sub.config(bg=bg)
            arrow.config(bg=bg)

    # --------------------------------------------------------
    # Detail panel
    # --------------------------------------------------------

    def update_detail(self):
        for w in self.detail.winfo_children():
            w.destroy()

        m = MODULES[self.selected]

        top = tk.Frame(self.detail, bg=PANEL)
        top.pack(fill="x", padx=25, pady=25)

        tk.Label(
            top, text=m["code"],
            bg=m["color"], fg=WHITE,
            font=("Consolas", 13, "bold"),
            width=7, height=2
        ).pack(side="left", padx=(0, 15))

        title_box = tk.Frame(top, bg=PANEL)
        title_box.pack(side="left")

        tk.Label(
            title_box, text=m["title"],
            bg=PANEL, fg=TEXT,
            font=("Arial", 22, "bold")
        ).pack(anchor="w")

        tk.Label(
            title_box, text=m["short"],
            bg=PANEL, fg=MUTED,
            font=("Arial", 10)
        ).pack(anchor="w")

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

        # live stats
        stats = tk.Frame(
            self.detail, bg="#081725"
        )
        stats.pack(fill="x", padx=25, pady=12)

        self.stat_label(
            stats, "ACTIONS", str(self.actions)
        ).pack(side="left", expand=True, pady=15)

        self.stat_label(
            stats, "IMPACT", str(self.impact)
        ).pack(side="left", expand=True)

        self.stat_label(
            stats, "BADGES", str(len(self.achievements))
        ).pack(side="left", expand=True)

        btn = self.button(
            self.detail,
            "OPEN INTERACTIVE SOLUTION  →",
            lambda: self.open_solution(m),
            m["color"],
            30
        )
        # (this used to be "height=45", which sizes a tk.Button in
        # TEXT LINES, not pixels - it was turning the button into an
        # enormous square. ipady gives a normal, comfortable button.)
        btn.pack(pady=15, ipady=6)

        tk.Label(
            self.detail,
            text=f'“{QUOTES[(self.selected + 2) % len(QUOTES)]}”',
            bg=PANEL, fg=MUTED,
            font=("Georgia", 11, "italic"),
            wraplength=600
        ).pack(pady=10)

    def add_info_block(self, heading, text, color):
        box = tk.Frame(self.detail, bg=PANEL)
        box.pack(fill="x", padx=25, pady=7)

        tk.Label(
            box, text=heading,
            bg=PANEL, fg=color,
            font=("Consolas", 10, "bold")
        ).pack(anchor="w")

        tk.Label(
            box, text=text,
            bg=PANEL, fg=MUTED,
            font=("Arial", 10),
            wraplength=650,
            justify="left",
            anchor="w"
        ).pack(anchor="w", pady=(3, 0))

    def stat_label(self, parent, title, value):
        f = tk.Frame(parent, bg="#081725")
        tk.Label(
            f, text=value,
            bg="#081725", fg=TEXT,
            font=("Consolas", 18, "bold")
        ).pack()
        tk.Label(
            f, text=title,
            bg="#081725", fg=MUTED,
            font=("Consolas", 8, "bold")
        ).pack()
        return f

    # --------------------------------------------------------
    # Solution window
    # --------------------------------------------------------

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

    def solution_window(self, module):
        w = tk.Toplevel(self.root)
        w.title("CIVIC SHIELD // " + module["title"])
        w.geometry("850x650")
        w.minsize(720, 550)
        w.configure(bg=BG)

        header = tk.Frame(w, bg="#0A1A2A", height=75)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text=module["code"],
            bg=module["color"], fg=WHITE,
            font=("Consolas", 11, "bold"),
            width=7
        ).pack(side="left", padx=20, pady=17)

        tk.Label(
            header, text=module["title"],
            bg="#0A1A2A", fg=TEXT,
            font=("Arial", 21, "bold")
        ).pack(side="left")

        return w

    # --------------------------------------------------------
    # Road Safety
    # --------------------------------------------------------

    def road_solution(self, m):
        w = self.solution_window(m)

        content = tk.Frame(w, bg=BG)
        content.pack(fill="both", expand=True, padx=28, pady=22)

        tk.Label(
            content, text="LIVE ROAD MONITOR",
            bg=BG, fg=CYAN,
            font=("Consolas", 15, "bold")
        ).pack(anchor="w")

        stats = tk.Frame(content, bg="#0B1B2B")
        stats.pack(fill="x", pady=12)

        detected = random.randint(180, 320)
        highrisk = random.randint(8, 28)

        for label, value in [
            ("VEHICLES DETECTED", detected),
            ("HIGH-RISK", highrisk),
            ("AVG SPEED", "47 km/h"),
        ]:
            f = tk.Frame(stats, bg="#0B1B2B")
            f.pack(side="left", expand=True, pady=15)
            tk.Label(
                f, text=str(value),
                bg="#0B1B2B", fg=TEXT,
                font=("Consolas", 17, "bold")
            ).pack()
            tk.Label(
                f, text=label,
                bg="#0B1B2B", fg=MUTED,
                font=("Consolas", 8)
            ).pack()

        form = tk.Frame(content, bg=BG)
        form.pack(fill="x", pady=5)

        entries = {}
        for label, default in [
            ("Vehicle plate", ""),
            ("Speed (km/h)", ""),
            ("Legal limit (km/h)", "50"),
        ]:
            tk.Label(
                form, text=label,
                bg=BG, fg=MUTED,
                font=("Arial", 9)
            ).pack(anchor="w")
            e = tk.Entry(
                form, bg="#10263A", fg=TEXT,
                insertbackground=TEXT,
                relief="flat", font=("Consolas", 11)
            )
            e.insert(0, default)
            e.pack(fill="x", pady=(2, 8))
            entries[label] = e

        result = tk.Label(
            content, text="READY FOR VEHICLE ANALYSIS",
            bg=BG, fg=MUTED,
            font=("Consolas", 11),
            justify="left"
        )
        result.pack(anchor="w", pady=8)

        def analyze():
            try:
                speed = float(entries["Speed (km/h)"].get())
                limit = float(entries["Legal limit (km/h)"].get())
                excess = speed - limit
                self.add_action(60)

                if excess <= 0:
                    result.config(
                        text="✓ CLEAR\nVehicle is within the configured speed limit.",
                        fg=GREEN
                    )
                    beep("success")
                else:
                    risk = min(100, 35 + excess * 2)
                    fine = 500 + max(0, excess) * 100
                    result.config(
                        text=(
                            f"⚠ VIOLATION DETECTED\n"
                            f"Excess speed: {excess:.1f} km/h\n"
                            f"Risk score: {risk:.0f}/100\n"
                            f"Estimated fine: {fine:.0f} BDT"
                        ),
                        fg=RED
                    )
                    beep("warning")
            except ValueError:
                result.config(text="Enter valid numbers.", fg=ORANGE)

        self.button(
            content, "ANALYZE VEHICLE",
            analyze, m["color"], 25
        ).pack(anchor="w", pady=8)

        tk.Label(
            content,
            text="Safety guidance: slow down near schools, crossings and intersections; never use a phone while driving.",
            bg=BG, fg=MUTED,
            font=("Arial", 9),
            wraplength=750,
            justify="left"
        ).pack(anchor="w", pady=10)

    # --------------------------------------------------------
    # Traffic - built as something an officer on point duty could
    # actually glance at: a live light diagram plus one-tap manual
    # overrides, because no formula beats a human who can see the
    # ambulance coming.
    # --------------------------------------------------------

    def traffic_solution(self, m):
        w = self.solution_window(m)

        # keep timers tied to this window so they don't fire after
        # the officer closes it
        w.traffic_active_dir = None
        w.traffic_mode = "IDLE"
        w.traffic_countdown_job = None
        w.traffic_release_job = None
        w.traffic_counts = {"North": 18, "South": 22, "East": 14, "West": 27}

        body = tk.Frame(w, bg=BG)
        body.pack(fill="both", expand=True, padx=24, pady=18)

        tk.Label(
            body, text="POLICE TRAFFIC CONTROL PANEL",
            bg=BG, fg=CYAN,
            font=("Consolas", 15, "bold")
        ).pack(anchor="w")
        tk.Label(
            body,
            text="Live intersection view with manual override - the officer on duty always has final say over the algorithm.",
            bg=BG, fg=MUTED, font=("Arial", 9),
            wraplength=760, justify="left"
        ).pack(anchor="w", pady=(2, 12))

        columns = tk.Frame(body, bg=BG)
        columns.pack(fill="both", expand=True)

        # ---- left column: the live intersection diagram ----
        left_col = tk.Frame(columns, bg=BG)
        left_col.pack(side="left", fill="y", padx=(0, 20))

        signal_canvas = tk.Canvas(
            left_col, width=280, height=280,
            bg="#081725", highlightthickness=1,
            highlightbackground=BORDER
        )
        signal_canvas.pack()

        status_label = tk.Label(
            left_col, text="STATUS: ALL RED - INTERSECTION IDLE",
            bg=BG, fg=MUTED, font=("Consolas", 10, "bold"),
            wraplength=280, justify="left"
        )
        status_label.pack(pady=(10, 2), anchor="w")

        countdown_label = tk.Label(
            left_col, text="", bg=BG, fg=GREEN,
            font=("Consolas", 22, "bold")
        )
        countdown_label.pack(anchor="w")

        # ---- right column: counts, overrides, and the log ----
        right_col = tk.Frame(columns, bg=BG)
        right_col.pack(side="left", fill="both", expand=True)

        tk.Label(
            right_col, text="VEHICLE QUEUE COUNT (per lane)",
            bg=BG, fg=TEXT, font=("Consolas", 10, "bold")
        ).pack(anchor="w")

        entries = {}
        counts_row = tk.Frame(right_col, bg=BG)
        counts_row.pack(fill="x", pady=(6, 10))
        for d in ("North", "South", "East", "West"):
            cell = tk.Frame(counts_row, bg=BG)
            cell.pack(side="left", expand=True, padx=4)
            tk.Label(
                cell, text=d, bg=BG, fg=MUTED, font=("Consolas", 9)
            ).pack()
            e = tk.Entry(
                cell, bg="#10263A", fg=TEXT, width=6, justify="center",
                insertbackground=TEXT, relief="flat", font=("Consolas", 12, "bold")
            )
            e.insert(0, str(w.traffic_counts[d]))
            e.pack()
            entries[d] = e

        tk.Label(
            right_col, text="MANUAL OVERRIDE - force a direction green",
            bg=BG, fg=TEXT, font=("Consolas", 10, "bold")
        ).pack(anchor="w", pady=(4, 6))

        override_row = tk.Frame(right_col, bg=BG)
        override_row.pack(fill="x")
        override_buttons = {}

        log = tk.Text(
            right_col, height=10, bg="#081725",
            fg=TEXT, relief="flat", font=("Consolas", 9),
            state="disabled", wrap="word"
        )

        def add_log(line, tag=None):
            stamp = datetime.now().strftime("%H:%M:%S")
            log.config(state="normal")
            log.insert("end", f"[{stamp}] {line}\n")
            log.see("end")
            log.config(state="disabled")

        def draw_signals():
            signal_canvas.delete("all")
            cx, cy = 140, 140
            road_w = 46
            signal_canvas.create_rectangle(
                0, cy - road_w, 280, cy + road_w, fill="#1B2A38", outline=""
            )
            signal_canvas.create_rectangle(
                cx - road_w, 0, cx + road_w, 280, fill="#1B2A38", outline=""
            )
            signal_canvas.create_rectangle(
                cx - road_w, cy - road_w, cx + road_w, cy + road_w,
                fill="#233647", outline=""
            )

            positions = {
                "North": (cx, cy - 100),
                "South": (cx, cy + 100),
                "East": (cx + 100, cy),
                "West": (cx - 100, cy),
            }
            for d, (x, y) in positions.items():
                is_green = (d == w.traffic_active_dir)
                lit = GREEN if is_green else RED
                signal_canvas.create_rectangle(
                    x - 15, y - 24, x + 15, y + 24,
                    fill="#0B1B2B", outline="#2A4A63"
                )
                signal_canvas.create_oval(
                    x - 9, y - 16, x + 9, y - 0,
                    fill=(RED if not is_green else "#3A1418"), outline=""
                )
                signal_canvas.create_oval(
                    x - 9, y + 2, x + 9, y + 18,
                    fill=(GREEN if is_green else "#123A22"), outline=""
                )
                signal_canvas.create_text(
                    x, y + 34, text=d.upper(), fill=MUTED, font=("Consolas", 8, "bold")
                )

        def cancel_jobs():
            if w.traffic_countdown_job:
                try:
                    w.after_cancel(w.traffic_countdown_job)
                except tk.TclError:
                    pass
                w.traffic_countdown_job = None
            if w.traffic_release_job:
                try:
                    w.after_cancel(w.traffic_release_job)
                except tk.TclError:
                    pass
                w.traffic_release_job = None

        def set_active(direction, mode, seconds=None, on_finish=None):
            cancel_jobs()
            w.traffic_active_dir = direction
            w.traffic_mode = mode
            draw_signals()
            for d, b in override_buttons.items():
                b.config(bg=(m["color"] if d == direction else CARD))
            status_label.config(
                text=f"STATUS: {direction.upper()} GREEN  •  {mode}",
                fg=GREEN
            )

            if seconds:
                remaining = {"t": seconds}

                def tick():
                    if not w.winfo_exists():
                        return
                    remaining["t"] -= 1
                    if remaining["t"] <= 0:
                        countdown_label.config(text="")
                        w.traffic_countdown_job = None
                        if on_finish:
                            on_finish()
                        return
                    countdown_label.config(text=f"{remaining['t']:>2}s")
                    w.traffic_countdown_job = w.after(1000, tick)

                countdown_label.config(text=f"{seconds:>2}s")
                w.traffic_countdown_job = w.after(1000, tick)
            else:
                countdown_label.config(text="HOLD")

        def clear_active():
            cancel_jobs()
            w.traffic_active_dir = None
            w.traffic_mode = "IDLE"
            draw_signals()
            for b in override_buttons.values():
                b.config(bg=CARD)
            status_label.config(text="STATUS: ALL RED - INTERSECTION IDLE", fg=MUTED)
            countdown_label.config(text="")

        def manual_override(direction):
            set_active(direction, "MANUALLY HELD BY OFFICER")
            add_log(f"Officer manually set {direction.upper()} to GREEN (holding until changed).")
            self.add_action(55)
            beep()

        for d in ("North", "South", "East", "West"):
            b = tk.Button(
                override_row, text=d.upper(), width=8,
                bg=CARD, fg=WHITE, activebackground=m["color"],
                activeforeground=WHITE, relief="flat", bd=0,
                font=("Consolas", 9, "bold"), cursor="hand2",
                command=lambda dd=d: manual_override(dd)
            )
            b.pack(side="left", padx=3, pady=2)
            override_buttons[d] = b

        emergency_row = tk.Frame(right_col, bg=BG)
        emergency_row.pack(fill="x", pady=(10, 6))

        emergency_choice = tk.StringVar(value="North")
        tk.Label(
            emergency_row, text="Emergency corridor for:",
            bg=BG, fg=MUTED, font=("Arial", 9)
        ).pack(side="left")
        self.dark_dropdown(
            emergency_row, emergency_choice, ["North", "South", "East", "West"]
        ).pack(side="left", padx=8)

        def emergency_priority():
            direction = emergency_choice.get()

            def released():
                add_log(f"Emergency corridor for {direction.upper()} released - returning to normal control.")
                clear_active()

            set_active(direction, "EMERGENCY CORRIDOR (ambulance / VIP)", seconds=10, on_finish=released)
            add_log(f"EMERGENCY PRIORITY: clearing {direction.upper()} for 10s (ambulance/VIP passage).")
            self.add_action(90)
            beep("warning")

        self.button(
            emergency_row, "CLEAR FOR EMERGENCY VEHICLE",
            emergency_priority, RED, 24
        ).pack(side="left")

        def run_optimizer():
            try:
                counts = {d: int(e.get()) for d, e in entries.items()}
                total = sum(counts.values())
                if total <= 0 or any(v < 0 for v in counts.values()):
                    raise ValueError
            except ValueError:
                messagebox.showwarning(
                    "Invalid traffic data",
                    "Enter whole, non-negative numbers for vehicle counts.",
                    parent=w
                )
                return

            plan = {
                d: max(8, round(count / total * 90))
                for d, count in counts.items()
            }
            busiest = max(counts, key=counts.get)

            add_log("Auto-optimizer ran on current queue counts:")
            for d in ("North", "South", "East", "West"):
                add_log(f"   {d:<6} {counts[d]:>3} vehicles  ->  {plan[d]:>2}s green")
            add_log(f"Busiest lane is {busiest.upper()} - giving it the next green phase.")

            def finished():
                add_log(f"{busiest.upper()} green phase complete - awaiting next decision.")

            set_active(busiest, "AUTO-OPTIMIZED PHASE", seconds=plan[busiest], on_finish=finished)
            self.add_action(75)
            beep("success")

        self.button(
            right_col, "RUN AUTO-OPTIMIZER ON CURRENT COUNTS",
            run_optimizer, m["color"], 34
        ).pack(anchor="w", pady=(2, 10))

        tk.Label(
            right_col, text="OFFICER ACTIVITY LOG",
            bg=BG, fg=TEXT, font=("Consolas", 10, "bold")
        ).pack(anchor="w")
        log.pack(fill="both", expand=True, pady=(4, 0))

        draw_signals()
        add_log("Panel opened. All directions red - ready for officer input.")

        def on_close():
            cancel_jobs()
            w.destroy()

        w.protocol("WM_DELETE_WINDOW", on_close)

    # --------------------------------------------------------
    # Blood Response
    # --------------------------------------------------------

    def blood_solution(self, m):
        w = self.solution_window(m)

        frame = tk.Frame(w, bg=BG)
        frame.pack(fill="both", expand=True, padx=30, pady=25)

        donors = {
            "O-": ["Ayesha Rahman"],
            "O+": ["Nusrat Jahan", "Imran Ali"],
            "A-": ["Community Donor Network"],
            "A+": ["Tanvir Alam", "Sadia Noor"],
            "B-": ["Emergency Donor Network"],
            "B+": ["Farhana Kabir"],
            "AB-": ["Regional Donor Network"],
            "AB+": ["Rafiq Islam"],
        }

        tk.Label(
            frame, text="EMERGENCY BLOOD MATCH",
            bg=BG, fg=CYAN,
            font=("Consolas", 15, "bold")
        ).pack(anchor="w")

        row = tk.Frame(frame, bg=BG)
        row.pack(fill="x", pady=20)

        blood = tk.StringVar(value="O+")
        urgency = tk.StringVar(value="URGENT")

        tk.Label(
            row, text="Blood group",
            bg=BG, fg=MUTED
        ).pack(side="left")

        self.dark_dropdown(row, blood, donors.keys()).pack(side="left", padx=10)

        tk.Label(
            row, text="Urgency",
            bg=BG, fg=MUTED
        ).pack(side="left", padx=(25, 0))

        self.dark_dropdown(
            row, urgency, ["CRITICAL", "URGENT", "NORMAL"]
        ).pack(side="left", padx=10)

        result = tk.Label(
            frame, text="No request active.",
            bg=BG, fg=MUTED,
            font=("Consolas", 11),
            justify="left"
        )
        result.pack(anchor="w", pady=20)

        def match():
            group = blood.get()
            names = donors.get(group, [])
            self.add_action(100)
            result.config(
                text=(
                    f"REQUEST: {urgency.get()}\n"
                    f"REQUIRED GROUP: {group}\n\n"
                    f"Potential matches:\n"
                    + "\n".join("• " + n for n in names)
                    + "\n\nNext step: contact the donor/network and verify eligibility."
                ),
                fg=GREEN
            )
            beep("success")

        self.button(
            frame, "FIND COMPATIBLE DONORS",
            match, m["color"], 30
        ).pack(anchor="w")

    # --------------------------------------------------------
    # Clean City
    # --------------------------------------------------------

    def clean_solution(self, m):
        w = self.solution_window(m)

        frame = tk.Frame(w, bg=BG)
        frame.pack(fill="both", expand=True, padx=28, pady=20)

        tk.Label(
            frame, text="CITY SERVICE REPORT CENTER",
            bg=BG, fg=CYAN,
            font=("Consolas", 15, "bold")
        ).pack(anchor="w")

        location = tk.Entry(
            frame, bg="#10263A", fg=TEXT,
            insertbackground=TEXT, relief="flat"
        )
        location.insert(0, "Location / landmark")
        location.pack(fill="x", pady=10)

        desc = tk.Text(
            frame, height=7,
            bg="#10263A", fg=TEXT,
            insertbackground=TEXT, relief="flat"
        )
        desc.pack(fill="both", expand=True)

        result = tk.Label(
            frame, text="Report ready.",
            bg=BG, fg=MUTED,
            font=("Consolas", 10),
            justify="left"
        )
        result.pack(anchor="w", pady=12)

        def report():
            text = desc.get("1.0", "end").lower()
            if not location.get().strip():
                return
            if any(x in text for x in ("medical", "hazard", "overflow", "blocked drain")):
                priority = "CRITICAL"
            elif any(x in text for x in ("smell", "garbage", "blocked", "waste")):
                priority = "HIGH"
            else:
                priority = "NORMAL"

            self.add_action(70)
            ticket = f"CS-{random.randint(10000, 99999)}"
            result.config(
                text=(
                    f"REPORT SUBMITTED\n"
                    f"Ticket: {ticket}\n"
                    f"Priority: {priority}\n"
                    f"Status: QUEUED FOR REVIEW"
                ),
                fg=GREEN
            )
            beep("success")

        self.button(
            frame, "SUBMIT CITY REPORT",
            report, m["color"], 28
        ).pack(anchor="w")

    # --------------------------------------------------------
    # Food Rescue
    # --------------------------------------------------------

    def food_solution(self, m):
        w = self.solution_window(m)

        frame = tk.Frame(w, bg=BG)
        frame.pack(fill="both", expand=True, padx=28, pady=20)

        tk.Label(
            frame, text="SURPLUS FOOD MATCHING",
            bg=BG, fg=CYAN,
            font=("Consolas", 15, "bold")
        ).pack(anchor="w")

        fields = {}
        for label, default in [
            ("Food item", "Cooked rice / meals"),
            ("Quantity", "25 portions"),
            ("Pickup time", "Within 2 hours"),
        ]:
            tk.Label(
                frame, text=label,
                bg=BG, fg=MUTED
            ).pack(anchor="w", pady=(10, 2))
            e = tk.Entry(
                frame, bg="#10263A", fg=TEXT,
                insertbackground=TEXT, relief="flat"
            )
            e.insert(0, default)
            e.pack(fill="x")
            fields[label] = e

        result = tk.Label(
            frame, text="No listing created.",
            bg=BG, fg=MUTED,
            font=("Consolas", 10),
            justify="left"
        )
        result.pack(anchor="w", pady=20)

        def match():
            recipient = random.choice([
                "Community Kitchen",
                "Local Food Support Group",
                "Neighborhood Relief Center"
            ])
            self.add_action(80)
            result.config(
                text=(
                    "LISTING CREATED\n"
                    f"Item: {fields['Food item'].get()}\n"
                    f"Quantity: {fields['Quantity'].get()}\n"
                    f"Pickup: {fields['Pickup time'].get()}\n"
                    f"Suggested recipient: {recipient}\n\n"
                    "Reminder: only redistribute food that is safe and legally appropriate to donate."
                ),
                fg=GREEN
            )
            beep("success")

        self.button(
            frame, "MATCH WITH RECIPIENT",
            match, m["color"], 28
        ).pack(anchor="w")

    # --------------------------------------------------------
    # Education
    # --------------------------------------------------------

    def education_solution(self, m):
        w = self.solution_window(m)

        frame = tk.Frame(w, bg=BG)
        frame.pack(fill="both", expand=True, padx=28, pady=20)

        tk.Label(
            frame, text="PERSONAL LEARNING PATH",
            bg=BG, fg=CYAN,
            font=("Consolas", 15, "bold")
        ).pack(anchor="w")

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

        subject = tk.StringVar(value="Programming")
        self.dark_dropdown(frame, subject, subjects.keys()).pack(anchor="w", pady=15)

        listbox = tk.Listbox(
            frame, bg="#10263A", fg=TEXT,
            selectbackground="#24516D",
            relief="flat",
            font=("Consolas", 11)
        )
        listbox.pack(fill="both", expand=True)

        progress = tk.IntVar(value=0)

        def refresh():
            listbox.delete(0, "end")
            for item in subjects[subject.get()]:
                listbox.insert("end", "□ " + item)

        def complete():
            selection = listbox.curselection()
            if not selection:
                return
            idx = selection[0]
            old = listbox.get(idx)
            if old.startswith("□"):
                listbox.delete(idx)
                listbox.insert(idx, "✓ " + old[2:])
                progress.set(min(100, progress.get() + 25))
                self.add_action(45)
                beep("success")

            result.config(
                text=f"LEARNING PATH PROGRESS: {progress.get()}%",
                fg=GREEN
            )

        subject.trace_add("write", lambda *_: refresh())
        refresh()

        result = tk.Label(
            frame,
            text="LEARNING PATH PROGRESS: 0%",
            bg=BG, fg=MUTED,
            font=("Consolas", 10)
        )
        result.pack(anchor="w", pady=10)

        self.button(
            frame, "MARK SELECTED TOPIC COMPLETE",
            complete, m["color"], 32
        ).pack(anchor="w")

    # --------------------------------------------------------
    # Water
    # --------------------------------------------------------

    def water_solution(self, m):
        w = self.solution_window(m)

        frame = tk.Frame(w, bg=BG)
        frame.pack(fill="both", expand=True, padx=28, pady=20)

        tk.Label(
            frame, text="WATER USAGE ANALYZER",
            bg=BG, fg=CYAN,
            font=("Consolas", 15, "bold")
        ).pack(anchor="w")

        entries = {}
        for label, default in [
            ("Previous meter reading (L)", "1000"),
            ("Current meter reading (L)", "1080"),
            ("Hours elapsed", "24"),
        ]:
            tk.Label(
                frame, text=label,
                bg=BG, fg=MUTED
            ).pack(anchor="w", pady=(9, 2))
            e = tk.Entry(
                frame, bg="#10263A", fg=TEXT,
                insertbackground=TEXT, relief="flat"
            )
            e.insert(0, default)
            e.pack(fill="x")
            entries[label] = e

        result = tk.Label(
            frame, text="Scanner ready.",
            bg=BG, fg=MUTED,
            font=("Consolas", 11),
            justify="left"
        )
        result.pack(anchor="w", pady=20)

        def scan():
            try:
                old = float(entries["Previous meter reading (L)"].get())
                new = float(entries["Current meter reading (L)"].get())
                hours = float(entries["Hours elapsed"].get())

                if hours <= 0 or new < old:
                    raise ValueError

                rate = (new - old) / hours
                self.add_action(65)

                if rate > 5:
                    result.config(
                        text=(
                            f"⚠ POSSIBLE LEAK DETECTED\n"
                            f"Consumption: {new-old:.1f} L\n"
                            f"Rate: {rate:.2f} L/hour\n\n"
                            "Recommendation: inspect taps, toilets, pipes and outdoor lines."
                        ),
                        fg=RED
                    )
                    beep("warning")
                else:
                    result.config(
                        text=(
                            f"✓ USAGE APPEARS NORMAL\n"
                            f"Consumption: {new-old:.1f} L\n"
                            f"Rate: {rate:.2f} L/hour\n\n"
                            "Continue monitoring for sudden changes."
                        ),
                        fg=GREEN
                    )
                    beep("success")
            except ValueError:
                result.config(
                    text="Enter valid positive readings and elapsed hours.",
                    fg=ORANGE
                )

        self.button(
            frame, "RUN LEAK ANALYSIS",
            scan, m["color"], 28
        ).pack(anchor="w")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = CivicShield(root)
    root.mainloop()