import tkinter as tk
import math
import random
import platform
import os
import shutil
import subprocess
import tempfile
import atexit
import struct
import wave
import time


# ==============================================================================
# COLORS
# ==============================================================================

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

SHIELD_FILL = "#0b2030"
RADAR_GRID = "#16445c"
TRACK_BG = "#13293d"
BUTTON_BG = "#126d98"
HEADER_BG = "#0b1d2e"
MED_ACCENT = "#e83e5b"
FOOD_ACCENT = "#f57c36"

# Dedicated colors for input fields - distinct from CARD so they read as
# "things you can click into" rather than blending into the background.
FIELD_BG = "#0f2233"
FIELD_BORDER = "#1f3f57"


# ==============================================================================
# COLOR HELPERS (used for the smooth hover / fade animations)
# ==============================================================================

def _hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def _rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def _interpolate_color(c1, c2, t):
    """Blend between two hex colors; t=0 -> c1, t=1 -> c2."""
    r1, g1, b1 = _hex_to_rgb(c1)
    r2, g2, b2 = _hex_to_rgb(c2)
    r = round(r1 + (r2 - r1) * t)
    g = round(g1 + (g2 - g1) * t)
    b = round(b1 + (b2 - b1) * t)
    return _rgb_to_hex((r, g, b))


def _lighten(hex_color, amount=0.18):
    """A slightly lighter shade, used for button hover/active states."""
    try:
        r, g, b = _hex_to_rgb(hex_color)
    except Exception:
        return hex_color
    r = min(255, round(r + (255 - r) * amount))
    g = min(255, round(g + (255 - g) * amount))
    b = min(255, round(b + (255 - b) * amount))
    return _rgb_to_hex((r, g, b))


# ==============================================================================
# QUOTES
# ==============================================================================

QUOTES = [
    '"Small actions can create big changes."',
    '"Technology becomes meaningful when it improves lives."',
    '"Together, we can solve problems that affect everyone."',
    '"Every community becomes stronger when people take action."',
    '"The future is built by the problems we choose to solve."',
]


# ==============================================================================
# MODULE DATA
# ==============================================================================

MODULES = [
    ("RAD", "ROAD SAFETY", "Speed Detection & Fine System", RED),
    ("SIG", "SMART TRAFFIC", "Adaptive Signal Management", ORANGE),
    ("MED", "BLOOD RESPONSE", "Emergency Donor Finder", MED_ACCENT),
    ("CLN", "CLEAN CITY", "Garbage Reporting System", GREEN),
    ("FOD", "FOOD RESCUE", "Food Redistribution Network", FOOD_ACCENT),
    ("EDU", "EDUCATION", "Free Learning Resources", BLUE),
    ("WTR", "WATER PROTECTION", "Leak Detection System", CYAN),
]


# ==============================================================================
# SOUND ENGINE
# ------------------------------------------------------------------------------
# The original only played sound on Windows (winsound). This version
# generates a short sine-wave tone as a .wav file using nothing but the
# standard library, then plays it with whatever the OS has available -
# so clicks and alerts are audible on macOS and Linux too, not just
# Windows. If no audio backend is found at all, these calls simply do
# nothing; they never raise or interrupt the app.
# ==============================================================================

def _audio_backend():
    if platform.system() == "Windows":
        return "winsound"
    for player in ("afplay", "paplay", "aplay", "play"):
        if shutil.which(player):
            return player
    return None


_BACKEND = _audio_backend()
_SOUND_DIR = tempfile.mkdtemp(prefix="civicshield_snd_")
atexit.register(lambda: shutil.rmtree(_SOUND_DIR, ignore_errors=True))
_TONE_CACHE = {}
_bg_procs = []  # tracks fire-and-forget player processes so we can reap finished ones


def _make_tone(freq, duration_ms, volume=0.3):
    """Generate (and cache) a short sine-wave tone as a .wav file on disk."""
    key = (round(freq), round(duration_ms))
    if key in _TONE_CACHE:
        return _TONE_CACHE[key]

    rate = 44100
    n_samples = max(int(rate * duration_ms / 1000), 1)
    fade_samples = max(int(rate * 0.01), 1)  # 10ms fade in/out avoids audible clicks

    frames = bytearray()
    for i in range(n_samples):
        envelope = min(i / fade_samples, (n_samples - i) / fade_samples, 1.0)
        sample = volume * envelope * math.sin(2 * math.pi * freq * i / rate)
        frames += struct.pack("<h", int(sample * 32767))

    path = os.path.join(_SOUND_DIR, f"tone_{key[0]}_{key[1]}.wav")
    with wave.open(path, "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(rate)
        f.writeframes(bytes(frames))

    _TONE_CACHE[key] = path
    return path


def _play(freq, duration_ms, volume=0.3):
    global _bg_procs
    if _BACKEND is None:
        return
    try:
        if _BACKEND == "winsound":
            import winsound
            winsound.Beep(max(37, min(int(freq), 32767)), max(int(duration_ms), 1))
        else:
            _bg_procs = [p for p in _bg_procs if p.poll() is None]  # drop finished ones
            path = _make_tone(freq, duration_ms, volume)
            proc = subprocess.Popen(
                [_BACKEND, path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            _bg_procs.append(proc)
    except Exception:
        pass  # sound should never be able to crash the app


def click_sound():
    _play(850, 40)


def success_sound():
    _play(700, 60)
    time.sleep(0.05)
    _play(1000, 80)


def warning_sound():
    _play(1000, 120)
    time.sleep(0.05)
    _play(600, 150)


# ==============================================================================
# THEMED WIDGET HELPERS
# ------------------------------------------------------------------------------
# The original repeated the same 10+ line tk.Label(...)/tk.Button(...) call
# for every single piece of text or button. These helpers collapse that
# down to one line each, so the module code below reads as "what" rather
# than "how".
# ==============================================================================

def styled_label(parent, text, font, fg, bg=BG, **kwargs):
    return tk.Label(parent, text=text, font=font, fg=fg, bg=bg, **kwargs)


def styled_button(parent, text, bg, command, fg="white",
                   font=("Consolas", 11, "bold"), padx=25, pady=10):
    return tk.Button(
        parent, text=text, font=font, bg=bg, fg=fg,
        activebackground=_lighten(bg), activeforeground=fg,
        bd=0, padx=padx, pady=pady, cursor="hand2", command=command,
    )


def style_dropdown(menu_widget):
    """Applies the dark theme to a tk.OptionMenu and its dropdown list."""
    menu_widget.config(
        bg=FIELD_BG, fg=TEXT, activebackground=_lighten(FIELD_BG),
        activeforeground=TEXT, relief="flat", highlightthickness=0,
    )
    menu_widget["menu"].config(bg=FIELD_BG, fg=TEXT)


class PlaceholderEntry(tk.Entry):
    """
    A themed text field that shows grey hint text (e.g. "e.g. DHA-1234")
    until you click in. This fixes a bug in the original: it pre-filled
    entries with hint text using plain .insert(), so if a user didn't
    manually delete it first, that hint text got treated as real input.

    Always read input with .get_value(), not .get() - it returns "" while
    only the hint is showing, instead of the hint text itself.
    """

    def __init__(self, parent, placeholder, width=32):
        super().__init__(
            parent, width=width, font=("Arial", 12),
            bg=FIELD_BG, fg=TEXT, insertbackground=TEXT,
            relief="flat", highlightthickness=1,
            highlightbackground=FIELD_BORDER, highlightcolor=CYAN,
        )
        self.placeholder = placeholder
        self._showing_placeholder = False
        self._show_placeholder()
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._restore_placeholder)

    def _show_placeholder(self):
        self.delete(0, "end")
        self.insert(0, self.placeholder)
        self.config(fg=MUTED)
        self._showing_placeholder = True

    def _clear_placeholder(self, event=None):
        if self._showing_placeholder:
            self.delete(0, "end")
            self.config(fg=TEXT)
            self._showing_placeholder = False

    def _restore_placeholder(self, event=None):
        if not self.get():
            self._show_placeholder()

    def get_value(self):
        """The user's real input, or '' if only the hint text is showing."""
        return "" if self._showing_placeholder else self.get()


def themed_text(parent, width, height):
    """A tk.Text box styled to match the dark theme (multi-line fields)."""
    return tk.Text(
        parent, width=width, height=height, bg=FIELD_BG, fg=TEXT,
        insertbackground=TEXT, relief="flat", highlightthickness=1,
        highlightbackground=FIELD_BORDER, highlightcolor=CYAN,
    )


# ==============================================================================
# MAIN APP
# ==============================================================================

class CivicShieldApp:

    def __init__(self, root):
        self.root = root
        self.root.title("CIVIC SHIELD")
        self.root.geometry("1200x760")
        self.root.minsize(950, 650)
        self.root.configure(bg=BG)

        self.radar_running = True
        self.show_intro()

    # ------------------------------------------------------------------
    # SCREEN MANAGEMENT
    # ------------------------------------------------------------------

    def clear_screen(self):
        self.radar_running = False
        for widget in self.root.winfo_children():
            widget.destroy()

    # ------------------------------------------------------------------
    # INTRO SCREEN
    # ------------------------------------------------------------------

    def show_intro(self):
        self.clear_screen()
        self.radar_running = True

        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill="both", expand=True)

        styled_label(frame, "SECURE COMMUNITY SYSTEM // VERSION 2.0",
                     ("Consolas", 11, "bold"), MUTED).pack(pady=(30, 10))

        self.radar_canvas = tk.Canvas(frame, width=300, height=220, bg=BG,
                                       highlightthickness=0)
        self.radar_canvas.pack(pady=5)
        self._build_radar()
        self.radar_angle = 0
        self._blip_tick = 0
        self.animate_radar()

        styled_label(frame, "CIVIC SHIELD", ("Arial", 38, "bold"), TEXT).pack()
        styled_label(frame, "COMMUNITY IMPACT CONTROL SYSTEM",
                     ("Consolas", 14, "bold"), CYAN).pack(pady=(5, 15))

        self.quote_index = 0
        self.quote_label = styled_label(frame, QUOTES[0], ("Georgia", 14, "italic"),
                                         MUTED, wraplength=750)
        self.quote_label.pack(pady=15)
        self.rotate_quotes()

        styled_label(frame, "\u25cf 7 MODULES READY", ("Consolas", 12, "bold"),
                     GREEN).pack(pady=15)

        styled_button(frame, "ENTER CIVIC NETWORK", BUTTON_BG, self.enter_dashboard,
                      font=("Consolas", 13, "bold"), padx=40, pady=15).pack(pady=10)

    # ------------------------------------------------------------------
    # RADAR ANIMATION
    # ------------------------------------------------------------------
    # Built once here, then only the pieces that actually move get
    # updated each frame (see animate_radar). Recreating every shape on
    # every tick - like the original did - is what caused the flicker.

    def _build_radar(self):
        c = self.radar_canvas
        cx, cy = 150, 105
        self._radar_cx, self._radar_cy = cx, cy

        points = [cx, 10, cx + 85, 45, cx + 70, 140, cx, 200, cx - 70, 140, cx - 85, 45]
        c.create_polygon(points, outline=CYAN, fill=SHIELD_FILL, width=3)

        for radius in (25, 50, 75):
            c.create_oval(cx - radius, cy - radius, cx + radius, cy + radius,
                          outline=RADAR_GRID)
        c.create_line(cx - 75, cy, cx + 75, cy, fill=RADAR_GRID)
        c.create_line(cx, cy - 75, cx, cy + 75, fill=RADAR_GRID)

        # The one piece that moves every frame.
        self._radar_sweep = c.create_line(cx, cy, cx, cy - 75, fill=GREEN, width=3)

        c.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill=CYAN, outline="")

        # A small fixed pool of blips, repositioned occasionally rather
        # than respawned every frame - that constant random jumping was
        # a big part of what read as "glitchy".
        self._blip_ids = [c.create_oval(0, 0, 4, 4, fill=GREEN, outline="")
                           for _ in range(3)]
        for blip in self._blip_ids:
            c.itemconfig(blip, state="hidden")

    def animate_radar(self):
        if not self.radar_running or not hasattr(self, "radar_canvas"):
            return
        try:
            c = self.radar_canvas
            if not c.winfo_exists():
                return

            cx, cy = self._radar_cx, self._radar_cy
            angle = math.radians(self.radar_angle)
            x = cx + math.cos(angle) * 75
            y = cy + math.sin(angle) * 75
            c.coords(self._radar_sweep, cx, cy, x, y)

            # Reposition the blips a couple of times a second instead of
            # every single frame.
            self._blip_tick += 1
            if self._blip_tick % 16 == 0:
                for blip in self._blip_ids:
                    a = random.uniform(0, math.pi * 2)
                    r = random.uniform(20, 70)
                    bx, by = cx + math.cos(a) * r, cy + math.sin(a) * r
                    c.coords(blip, bx - 2, by - 2, bx + 2, by + 2)
                    c.itemconfig(blip, state="normal")

            self.radar_angle = (self.radar_angle + 4) % 360
            self.root.after(28, self.animate_radar)
        except tk.TclError:
            return

    # ------------------------------------------------------------------
    # QUOTE ROTATION
    # ------------------------------------------------------------------

    def rotate_quotes(self):
        try:
            if not self.quote_label.winfo_exists():
                return
            self.quote_index = (self.quote_index + 1) % len(QUOTES)
            self.quote_label.config(text=QUOTES[self.quote_index])
            self.root.after(4000, self.rotate_quotes)
        except tk.TclError:
            pass

    # ------------------------------------------------------------------
    # LOADING SCREEN
    # ------------------------------------------------------------------

    def enter_dashboard(self):
        click_sound()
        self.show_loading()

    def show_loading(self):
        self.clear_screen()
        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill="both", expand=True)

        styled_label(frame, "INITIALIZING CIVIC MODULES", ("Consolas", 25, "bold"),
                     CYAN).pack(pady=(250, 30))

        self.load_label = styled_label(frame, "LOADING 0%", ("Consolas", 13), MUTED)
        self.load_label.pack()

        self.progress_canvas = tk.Canvas(frame, width=500, height=25, bg=BG,
                                          highlightthickness=0)
        self.progress_canvas.pack(pady=20)

        # Track and fill bar are created once; each tick just resizes the
        # fill instead of clearing and redrawing both rectangles.
        self.progress_canvas.create_rectangle(0, 0, 500, 20, fill=TRACK_BG, outline="")
        self._progress_fill = self.progress_canvas.create_rectangle(
            0, 0, 0, 20, fill=GREEN, outline=""
        )

        self.load_value = 0
        self.loading_animation()

    def loading_animation(self):
        self.load_value = min(self.load_value + 3, 100)
        width = 500 * self.load_value / 100
        self.progress_canvas.coords(self._progress_fill, 0, 0, width, 20)
        self.load_label.config(text=f"LOADING {self.load_value}%")

        if self.load_value < 100:
            self.root.after(20, self.loading_animation)
        else:
            success_sound()
            self.root.after(300, self.show_dashboard)

    # ------------------------------------------------------------------
    # DASHBOARD
    # ------------------------------------------------------------------

    def show_dashboard(self):
        self.clear_screen()
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True)

        header = tk.Frame(main, bg=HEADER_BG, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        styled_label(header, "CIVIC SHIELD", ("Arial", 25, "bold"), TEXT,
                     bg=HEADER_BG).pack(side="left", padx=30, pady=20)
        styled_label(header, "\u25cf ALL SYSTEMS ONLINE", ("Consolas", 11, "bold"),
                     GREEN, bg=HEADER_BG).pack(side="right", padx=30)

        styled_label(main, "COMMUNITY PROTECTION MODULES", ("Consolas", 19, "bold"),
                     CYAN).pack(pady=(20, 3))
        styled_label(main, "Select a system to begin", ("Arial", 12), MUTED).pack(
            pady=(0, 15))

        grid = tk.Frame(main, bg=BG)
        grid.pack(expand=True)
        for col in range(4):
            grid.grid_columnconfigure(col, weight=1)

        for i, module in enumerate(MODULES):
            row, col = i // 4, i % 4
            self.create_card(grid, module, row, col)

    # ------------------------------------------------------------------
    # MODULE CARD (with smooth hover fade)
    # ------------------------------------------------------------------

    def create_card(self, parent, module, row, col):
        icon, title, subtitle, accent = module

        card = tk.Frame(parent, bg=CARD, width=220, height=175, cursor="hand2")
        card.grid(row=row, column=col, padx=12, pady=12)
        card.grid_propagate(False)
        card._hover_job = None  # tracks any in-progress fade so it can be cancelled

        icon_label = styled_label(card, icon, ("Consolas", 16, "bold"), "white",
                                   bg=accent, width=7, height=2)
        icon_label.pack(pady=(20, 10))

        title_label = styled_label(card, title, ("Consolas", 12, "bold"), TEXT, bg=CARD)
        title_label.pack()

        sub_label = styled_label(card, subtitle, ("Arial", 10), MUTED, bg=CARD)
        sub_label.pack(pady=5)

        open_label = styled_label(card, "OPEN MODULE  \u2192", ("Consolas", 9, "bold"),
                                   accent, bg=CARD)
        open_label.pack(pady=5)

        # The icon block keeps its own accent color on hover, so each
        # module stays instantly recognizable - only these three fade.
        fade_widgets = [card, title_label, sub_label, open_label]

        def on_enter(event=None):
            if card._hover_job:
                self.root.after_cancel(card._hover_job)
                card._hover_job = None
            self._animate_card_bg(card, fade_widgets, CARD_HOVER)

        def on_leave(event=None):
            if card._hover_job:
                self.root.after_cancel(card._hover_job)
                card._hover_job = None
            self._animate_card_bg(card, fade_widgets, CARD)

        def on_click(event=None):
            click_sound()
            self.open_module(module)

        for widget in (card, icon_label, title_label, sub_label, open_label):
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)

    def _animate_card_bg(self, card, widgets, target_hex, start_hex=None,
                          step=0, steps=6, delay=15):
        """
        Fades a card's background toward target_hex over a few quick steps
        instead of snapping instantly. Reads the CURRENT color as the
        starting point each time it's (re)triggered, so if you leave
        while it's still fading in, the reverse fade continues smoothly
        from wherever it actually is - it can't stutter or jump.
        """
        if start_hex is None:
            try:
                start_hex = widgets[0].cget("bg")
            except tk.TclError:
                return

        t = step / steps
        current = _interpolate_color(start_hex, target_hex, t)
        try:
            for w in widgets:
                w.config(bg=current)
        except tk.TclError:
            card._hover_job = None
            return

        if step >= steps:
            card._hover_job = None
            return

        card._hover_job = self.root.after(
            delay,
            lambda: self._animate_card_bg(card, widgets, target_hex, start_hex,
                                           step + 1, steps, delay),
        )

    # ------------------------------------------------------------------
    # OPEN MODULE
    # ------------------------------------------------------------------

    def open_module(self, module):
        icon, title, subtitle, color = module
        handlers = {
            "ROAD SAFETY": self.speeding_module,
            "SMART TRAFFIC": self.traffic_module,
            "BLOOD RESPONSE": self.blood_module,
            "CLEAN CITY": self.garbage_module,
            "FOOD RESCUE": self.food_module,
            "EDUCATION": self.education_module,
            "WATER PROTECTION": self.water_module,
        }
        handler = handlers.get(title)
        if handler:
            handler(title, color)

    # ------------------------------------------------------------------
    # SHARED MODULE WINDOW (with a quick fade-in)
    # ------------------------------------------------------------------

    def module_window(self, title, color, instructions=""):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("650x550")
        window.configure(bg=BG)

        try:
            window.attributes("-alpha", 0.0)
            self._fade_in(window)
        except tk.TclError:
            pass  # some window managers don't support transparency - harmless

        styled_label(window, title, ("Consolas", 22, "bold"), color).pack(pady=(25, 5))
        if instructions:
            styled_label(window, instructions, ("Arial", 11), MUTED,
                         wraplength=560, justify="center").pack(pady=(0, 15))
        return window

    def _fade_in(self, window, opacity=0.0):
        try:
            if not window.winfo_exists():
                return
            opacity = min(opacity + 0.18, 1.0)
            window.attributes("-alpha", opacity)
            if opacity < 1.0:
                self.root.after(15, lambda: self._fade_in(window, opacity))
        except tk.TclError:
            return

    # ------------------------------------------------------------------
    # ROAD SAFETY
    # ------------------------------------------------------------------

    def speeding_module(self, title, color):
        w = self.module_window(
            title, color,
            "Enter the vehicle's plate, its measured speed, and the posted limit."
        )

        plate = PlaceholderEntry(w, "e.g. DHA-1234", width=36)
        plate.pack(pady=8)
        speed = PlaceholderEntry(w, "Measured speed (km/h)", width=36)
        speed.pack(pady=8)
        limit = PlaceholderEntry(w, "Posted speed limit (km/h)", width=36)
        limit.pack(pady=8)

        result = styled_label(w, "READY FOR SCAN", ("Consolas", 12), MUTED,
                               wraplength=560, justify="center")
        result.pack(pady=20)

        def scan():
            try:
                measured = float(speed.get_value())
                limit_val = float(limit.get_value())
            except ValueError:
                result.config(text="ENTER VALID NUMBERS FOR SPEED AND LIMIT", fg=ORANGE)
                return

            plate_text = plate.get_value().strip() or "UNKNOWN PLATE"
            excess = measured - limit_val

            if excess <= 0:
                result.config(text=f"\u2713 {plate_text} CLEAR \u2014 WITHIN LIMIT", fg=GREEN)
                success_sound()
            else:
                fine = 500 + excess * 100
                result.config(
                    text=(f"\u26a0 SPEED VIOLATION \u2014 {plate_text}\n"
                          f"EXCESS: {excess:.1f} km/h\n"
                          f"FINE: {fine:.0f} BDT"),
                    fg=RED,
                )
                warning_sound()

        styled_button(w, "SCAN VEHICLE", color, scan).pack(pady=10)

    # ------------------------------------------------------------------
    # SMART TRAFFIC
    # ------------------------------------------------------------------

    def traffic_module(self, title, color):
        w = self.module_window(
            title, color,
            "Enter how many vehicles are waiting in each direction; green-light "
            "time is allocated automatically. Leave a direction blank for 0 cars."
        )

        entries = {}
        for direction in ("North", "South", "East", "West"):
            styled_label(w, f"{direction} vehicles:", ("Arial", 11), TEXT).pack()
            entry = PlaceholderEntry(w, "e.g. 12", width=20)
            entry.pack(pady=3)
            entries[direction] = entry

        result = styled_label(w, "", ("Consolas", 11), TEXT, justify="left")
        result.pack(pady=15)

        def optimize():
            try:
                data = {d: int(e.get_value() or 0) for d, e in entries.items()}
            except ValueError:
                result.config(text="ENTER WHOLE NUMBERS ONLY", fg=RED)
                return

            total = sum(data.values())
            if total == 0:
                result.config(text="NO TRAFFIC DETECTED", fg=GREEN)
                return

            lines = []
            for d, count in data.items():
                seconds = max(8, round(count / total * 90))
                lines.append(f"{d}: {seconds}s GREEN   ({count} cars)")
            result.config(text="\n".join(lines), fg=GREEN)
            success_sound()

        styled_button(w, "OPTIMIZE SIGNAL", color, optimize).pack()

    # ------------------------------------------------------------------
    # BLOOD RESPONSE
    # ------------------------------------------------------------------

    def blood_module(self, title, color):
        w = self.module_window(
            title, color,
            "Choose a blood type to find matching donors on file."
        )

        donors = {
            "O-": ["Ayesha Rahman"],
            "O+": ["Nusrat Jahan", "Imran Ali"],
            "A+": ["Tanvir Alam"],
            "B+": ["Farhana Kabir"],
            "AB+": ["Rafiq Islam"],
        }

        selected = tk.StringVar(value="O+")
        menu = tk.OptionMenu(w, selected, "O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+")
        style_dropdown(menu)
        menu.pack(pady=15)

        result = styled_label(w, "SELECT A BLOOD TYPE AND SEARCH", ("Consolas", 12),
                               MUTED, wraplength=560, justify="center")
        result.pack(pady=20)

        def search():
            blood = selected.get()
            found = donors.get(blood, [])
            if found:
                result.config(text=f"DONORS FOUND FOR {blood}\n\n" + "\n".join(found),
                              fg=GREEN)
                success_sound()
            else:
                result.config(text=f"NO DONORS ON FILE FOR {blood} YET", fg=ORANGE)

        styled_button(w, "SEARCH DONORS", color, search).pack()

    # ------------------------------------------------------------------
    # CLEAN CITY
    # ------------------------------------------------------------------

    def garbage_module(self, title, color):
        w = self.module_window(
            title, color,
            "Describe the issue - priority is detected automatically from "
            "keywords like 'hazard', 'medical', or 'overflow'."
        )

        styled_label(w, "Location:", ("Arial", 11), TEXT).pack()
        location = PlaceholderEntry(w, "e.g. Main Street, near the market", width=45)
        location.pack(pady=8)

        styled_label(w, "Problem description:", ("Arial", 11), TEXT).pack()
        description = themed_text(w, width=45, height=7)
        description.pack(pady=8)

        result = styled_label(w, "", ("Consolas", 11), TEXT, wraplength=560,
                               justify="center")
        result.pack(pady=15)

        def report():
            if not location.get_value().strip():
                result.config(text="LOCATION REQUIRED", fg=RED)
                return

            text = description.get("1.0", "end").lower()
            priority = "LOW"
            if any(word in text for word in ("hazard", "medical", "overflow")):
                priority = "HIGH"
            elif any(word in text for word in ("smell", "blocked")):
                priority = "MEDIUM"

            result.config(text=f"REPORT SENT\nPRIORITY: {priority}", fg=GREEN)
            success_sound()

        styled_button(w, "SEND REPORT", color, report).pack()

    # ------------------------------------------------------------------
    # FOOD RESCUE
    # ------------------------------------------------------------------

    def food_module(self, title, color):
        w = self.module_window(
            title, color,
            "List surplus food so nearby shelters and food banks can claim it."
        )

        item = PlaceholderEntry(w, "e.g. Rice & curry, 20 servings", width=40)
        donor = PlaceholderEntry(w, "Restaurant / donor name", width=40)
        hours = PlaceholderEntry(w, "Hours until it's no longer safe to eat", width=40)

        for label_text, field in (("Food item", item), ("Donor name", donor),
                                   ("Hours remaining", hours)):
            styled_label(w, label_text, ("Arial", 11), TEXT).pack()
            field.pack(pady=5)

        result = styled_label(w, "", ("Consolas", 11), TEXT, wraplength=560,
                               justify="center")
        result.pack(pady=20)

        def publish():
            item_text = item.get_value().strip()
            donor_text = donor.get_value().strip()
            if not item_text or not donor_text:
                result.config(text="PLEASE FILL IN THE FOOD ITEM AND DONOR NAME",
                              fg=ORANGE)
                return

            result.config(
                text=(f"\u2713 '{item_text}' FROM {donor_text} PUBLISHED\n"
                      f"Available for community organizations to claim."),
                fg=GREEN,
            )
            success_sound()

        styled_button(w, "PUBLISH LISTING", color, publish).pack()

    # ------------------------------------------------------------------
    # EDUCATION
    # ------------------------------------------------------------------

    def education_module(self, title, color):
        w = self.module_window(
            title, color,
            "Pick a subject to see free, reputable learning resources."
        )

        resources = {
            "Programming": ["freeCodeCamp", "CS50"],
            "Mathematics": ["Khan Academy", "OpenStax"],
            "Science": ["MIT OpenCourseWare"],
            "English": ["BBC Learning English", "British Council"],
        }

        selected = tk.StringVar(value="Programming")
        menu = tk.OptionMenu(w, selected, *resources.keys())
        style_dropdown(menu)
        menu.pack(pady=20)

        result = styled_label(w, "", ("Consolas", 12), CYAN, justify="left")
        result.pack(pady=20)

        def find():
            subject = selected.get()
            lines = [f"FREE {subject.upper()} RESOURCES", ""]
            lines += [f"\u2022 {x}" for x in resources[subject]]
            result.config(text="\n".join(lines), fg=CYAN)
            success_sound()

        styled_button(w, "FIND RESOURCES", color, find).pack()

    # ------------------------------------------------------------------
    # WATER PROTECTION
    # ------------------------------------------------------------------

    def water_module(self, title, color):
        w = self.module_window(
            title, color,
            "Enter two meter readings and the time between them to check "
            "for a possible leak."
        )

        zone = PlaceholderEntry(w, "e.g. Building A, Floor 2", width=40)
        previous = PlaceholderEntry(w, "Previous meter reading (liters)", width=40)
        current = PlaceholderEntry(w, "Current meter reading (liters)", width=40)
        hours = PlaceholderEntry(w, "Hours between readings", width=40)

        for label_text, field in (("Zone name", zone), ("Previous reading", previous),
                                   ("Current reading", current), ("Hours elapsed", hours)):
            styled_label(w, label_text, ("Arial", 11), TEXT).pack()
            field.pack(pady=4)

        result = styled_label(w, "", ("Consolas", 11), TEXT, wraplength=560,
                               justify="center")
        result.pack(pady=15)

        def analyze():
            try:
                old = float(previous.get_value())
                new = float(current.get_value())
                elapsed = float(hours.get_value())
            except ValueError:
                result.config(text="ENTER VALID NUMBERS FOR ALL READINGS", fg=ORANGE)
                return

            if new < old:
                result.config(text="CURRENT READING CAN'T BE LOWER THAN THE PREVIOUS ONE",
                              fg=RED)
                return
            if elapsed <= 0:
                result.config(text="HOURS ELAPSED MUST BE GREATER THAN ZERO", fg=RED)
                return

            zone_text = zone.get_value().strip() or "This zone"
            rate = (new - old) / elapsed

            if rate > 5:
                result.config(text=f"\u26a0 POSSIBLE LEAK \u2014 {zone_text}\n"
                                    f"FLOW: {rate:.2f} L/hour", fg=RED)
                warning_sound()
            else:
                result.config(text=f"\u2713 NORMAL FLOW \u2014 {zone_text}\n"
                                    f"FLOW: {rate:.2f} L/hour", fg=GREEN)
                success_sound()

        styled_button(w, "RUN LEAK SCAN", color, analyze).pack()


# ==============================================================================
# RUN
# ==============================================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = CivicShieldApp(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        root.destroy()q