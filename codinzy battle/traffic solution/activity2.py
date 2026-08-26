import os
import sys
import time
import random
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Dict


# ==============================================================================
# TERMINAL COLOR / STYLE ENGINE
# ==============================================================================

class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"

    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"


def enable_ansi_on_windows():
    if os.name == "nt":
        os.system("")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def clear_line(width: int = 90):
    sys.stdout.write("\r" + " " * width + "\r")
    sys.stdout.flush()


def color(text: str, *styles: str) -> str:
    return "".join(styles) + text + C.RESET


# ==============================================================================
# ANIMATION HELPERS
# ==============================================================================

def typewriter(text: str, delay: float = 0.016, style: str = "") -> None:
    for ch in text:
        sys.stdout.write(style + ch + (C.RESET if style else ""))
        sys.stdout.flush()
        time.sleep(delay)
    print()


def loading_bar(label: str, duration: float = 1.2, width: int = 30,
                 fill_color: str = C.BRIGHT_CYAN) -> None:
    steps = 22
    for i in range(steps + 1):
        filled = int(width * i / steps)
        bar = "█" * filled + "░" * (width - filled)
        pct = int(100 * i / steps)
        sys.stdout.write(f"\r{label} {fill_color}[{bar}]{C.RESET} {pct:3d}%")
        sys.stdout.flush()
        time.sleep(duration / steps)
    print()


def spinner(label: str, duration: float = 1.0) -> None:
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{color(frames[i % len(frames)], C.BRIGHT_CYAN)} {label}")
        sys.stdout.flush()
        time.sleep(0.06)
        i += 1
    clear_line()


def flash(text: str, times: int = 3, delay: float = 0.13,
          c1: str = C.BRIGHT_RED, c2: str = C.BRIGHT_YELLOW) -> None:
    for _ in range(times):
        sys.stdout.write(f"\r{color(text, C.BOLD, c1)}")
        sys.stdout.flush()
        time.sleep(delay)
        clear_line()
        sys.stdout.write(f"\r{color(text, C.BOLD, c2)}")
        sys.stdout.flush()
        time.sleep(delay)
        clear_line()
    print(color(text, C.BOLD, c1))


def fade_in_lines(lines: List[str], style: str = C.BRIGHT_CYAN, delay: float = 0.08) -> None:
    """Reveal a block of text line by line, for a cinematic build-up."""
    for line in lines:
        print(color(line, style))
        time.sleep(delay)


def box(text_lines: List[str], color_style: str = C.BRIGHT_CYAN, width: int = 56) -> str:
    top = "╔" + "═" * width + "╗"
    bottom = "╚" + "═" * width + "╝"
    body = []
    for line in text_lines:
        visible_len = len(strip_ansi(line))
        pad = max(width - 1 - visible_len, 0)
        body.append(f"║ {line}{' ' * pad}║")
    return color("\n".join([top] + body + [bottom]), color_style)


def strip_ansi(text: str) -> str:
    import re
    return re.sub(r"\033\[[0-9;]*m", "", text)


def press_enter(msg: str = "Press Enter to continue...") -> None:
    try:
        input(color(f"\n{msg}", C.DIM))
    except EOFError:
        pass


# ==============================================================================
# OPTIONAL TURTLE CINEMATIC INTRO
# ==============================================================================

def turtle_intro() -> None:
    """
    Draws an animated shield-and-radar badge using turtle graphics as a
    cinematic splash before the console menu loads. If no display is
    available (headless server, some IDEs), this silently falls back to
    a console-only animation - the program still runs perfectly.
    """
    try:
        import turtle
        screen = turtle.Screen()
        screen.setup(width=700, height=550)
        screen.bgcolor("black")
        screen.title("CIVIC SHIELD")
        screen.tracer(0)

        t = turtle.Turtle()
        t.hideturtle()
        t.speed(0)
        t.width(3)

        # Draw a shield outline
        t.penup()
        t.goto(0, 200)
        t.pendown()
        t.color("#00e5ff")
        t.setheading(-60)
        for _ in range(2):
            t.circle(140, 60)
            t.forward(140)
            t.right(120)
        screen.update()

        # Animated radar sweep line inside the shield
        radar = turtle.Turtle()
        radar.hideturtle()
        radar.speed(0)
        radar.width(2)
        radar.color("#39ff14")
        for angle in range(0, 720, 6):
            radar.clear()
            radar.penup()
            radar.goto(0, 60)
            radar.pendown()
            radar.setheading(angle)
            radar.forward(90)
            screen.update()
            time.sleep(0.01)

        # Title text
        writer = turtle.Turtle()
        writer.hideturtle()
        writer.color("white")
        writer.penup()
        writer.goto(0, -220)
        writer.write("CIVIC SHIELD", align="center", font=("Courier", 28, "bold"))
        screen.update()
        time.sleep(1.0)
        screen.bye()
    except Exception:
        # No display / tkinter unavailable / user closed window early -> fine.
        console_only_intro()


def console_only_intro() -> None:
    """Fallback cinematic intro using only the terminal (always works)."""
    frames = [
        "        .   *  .    .   *   .",
        "      *    .  🛡️   .    *  .",
        "        .   *  .    .   *   .",
    ]
    for f in frames:
        clear_line()
        sys.stdout.write("\r" + color(f, C.DIM))
        sys.stdout.flush()
        time.sleep(0.2)
    clear_line()
    radar_pulse()


def radar_pulse(duration: float = 1.4) -> None:
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(
            f"\r  {color('[RADAR ' + frames[i % 4] + ']', C.BRIGHT_GREEN)} "
            f"initializing civic systems..."
        )
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    clear_line()


# ==============================================================================
# ASCII ART
# ==============================================================================

TITLE_ART = r"""
   ____ _____     _____ ____    ____  _   _ ___ _____ _     ____
  / ___|_ _\ \   / /_ _/ ___|  / ___|| | | |_ _| ____| |   |  _ \
 | |    | | \ \ / / | | |      \___ \| |_| || ||  _| | |   | | | |
 | |___ | |  \ V /  | | |___    ___) |  _  || || |___| |___| |_| |
  \____|___|  \_/  |___\____|  |____/|_| |_|___|_____|_____|____/

        C O M M U N I T Y   I M P A C T   C O N S O L E
"""


def print_title() -> None:
    print(color(TITLE_ART, C.BOLD, C.BRIGHT_CYAN))


# ==============================================================================
# MAIN MENU
# ==============================================================================

MENU_ITEMS = [
    ("1", "🚗", "Car Speeding Fine System", C.BRIGHT_RED),
    ("2", "🚦", "Smart Traffic Management System", C.BRIGHT_YELLOW),
    ("3", "🩸", "Emergency Blood Donor Finder", C.BRIGHT_RED),
    ("4", "🗑️", "Garbage Collection Reporting System", C.GREEN),
    ("5", "🍲", "Food Waste Redistribution System", C.BRIGHT_YELLOW),
    ("6", "📚", "Free Education Resource Finder", C.BRIGHT_BLUE),
    ("7", "💧", "Water Leakage Detection System", C.BRIGHT_CYAN),
    ("0", "🚪", "Exit", C.DIM),
]


def show_menu() -> None:
    print(color("╔" + "═" * 58 + "╗", C.BRIGHT_CYAN))
    print(color("║", C.BRIGHT_CYAN) + color("  SELECT A PROGRAM".ljust(58), C.BOLD) + color("║", C.BRIGHT_CYAN))
    print(color("╠" + "═" * 58 + "╣", C.BRIGHT_CYAN))
    for key, icon, label, style in MENU_ITEMS:
        line = f"  {color('[' + key + ']', C.BOLD, C.BRIGHT_YELLOW)} {icon}  {color(label, style)}"
        pad = 58 - len(strip_ansi(f"  [{key}] {icon}  {label}")) + 2
        print(color("║", C.BRIGHT_CYAN) + line + " " * max(pad, 0) + color("║", C.BRIGHT_CYAN))
    print(color("╚" + "═" * 58 + "╝", C.BRIGHT_CYAN))


def module_banner(icon: str, title: str, style: str) -> None:
    clear_screen()
    print(color("─" * 62, style))
    typewriter(f"  {icon}  {title}", delay=0.012, style=style + C.BOLD)
    print(color("─" * 62, style))
    print()


# ==============================================================================
# GENERIC INPUT HELPERS
# ==============================================================================

def ask_text(prompt: str) -> str:
    return input(color(prompt, C.CYAN)).strip()


def ask_float(prompt: str, min_value: float = None) -> float:
    while True:
        raw = input(color(prompt, C.CYAN)).strip()
        try:
            value = float(raw)
            if min_value is not None and value < min_value:
                print(color(f"  Please enter a number ≥ {min_value}.", C.RED))
                continue
            return value
        except ValueError:
            print(color("  That's not a valid number, try again.", C.RED))


def ask_int(prompt: str, min_value: int = None) -> int:
    while True:
        raw = input(color(prompt, C.CYAN)).strip()
        try:
            value = int(raw)
            if min_value is not None and value < min_value:
                print(color(f"  Please enter a whole number ≥ {min_value}.", C.RED))
                continue
            return value
        except ValueError:
            print(color("  That's not a whole number, try again.", C.RED))


def ask_choice(prompt: str, options: List[str]) -> str:
    while True:
        print(color(prompt, C.CYAN))
        for i, opt in enumerate(options, start=1):
            print(f"  {color(str(i), C.BRIGHT_YELLOW)}. {opt}")
        raw = input(color("Enter number: ", C.CYAN)).strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        print(color("  Invalid choice, try again.\n", C.RED))


def ask_yes_no(prompt: str) -> bool:
    while True:
        raw = input(color(f"{prompt} (y/n): ", C.CYAN)).strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print(color("  Please answer y or n.", C.RED))


def now_str() -> str:
    return datetime.now().isoformat(timespec="seconds")


# ==============================================================================
# 🚗 MODULE 1 — CAR SPEEDING FINE SYSTEM
# ==============================================================================

FINE_TIERS = [
    (10, "Minor", 50, 5),
    (20, "Moderate", 100, 10),
    (40, "Severe", 250, 20),
    (float("inf"), "Reckless", 600, 35),
]

SEVERITY_COLOR = {
    "Minor": C.BRIGHT_YELLOW, "Moderate": C.YELLOW,
    "Severe": C.BRIGHT_RED, "Reckless": C.BOLD + C.BRIGHT_RED,
}


def calc_fine(excess: float):
    if excess <= 0:
        return 0.0, "None"
    lower = 0
    for cap, label, base, rate in FINE_TIERS:
        if excess <= cap:
            return round(base + (excess - lower) * rate, 2), label
        lower = cap
    return 0.0, "Reckless"


def module_speeding() -> None:
    module_banner("🚗", "Car Speeding Fine System", C.BRIGHT_RED)
    zones = {
        "School Zone": (30, 100),
        "Highway": (100, 500),
        "Bridge": (50, 200),
    }
    print(color("Zones on file:", C.DIM))
    for name, (limit, dist) in zones.items():
        print(f"   • {name} — limit {limit} km/h, sensor gap {dist} m")

    violations = []
    while True:
        print()
        plate = ask_text("Vehicle plate: ").upper()
        zone_name = ask_choice("Zone:", list(zones.keys()))
        t = ask_float("Transit time across sensors (seconds): ", min_value=0.1)

        spinner("Radar calculating speed...", 1.0)
        limit, dist = zones[zone_name]
        speed = (dist / t) * 3.6

        if speed <= limit:
            print(color(f"  ✓ {plate} clear at {speed:.1f} km/h (limit {limit})\n", C.BRIGHT_GREEN))
        else:
            excess = speed - limit
            fine, severity = calc_fine(excess)
            flash("  🚨 SPEED VIOLATION DETECTED 🚨", times=3)
            lines = [
                f"{color('Plate:', C.BOLD)} {plate}   {color('Zone:', C.BOLD)} {zone_name}",
                f"{color('Speed:', C.BOLD)} {speed:.1f} km/h  (limit {limit})",
                f"{color('Severity:', C.BOLD)} {color(severity, SEVERITY_COLOR[severity])}",
                f"{color('Fine:', C.BOLD)} {color(f'${fine:,.2f}', C.BRIGHT_GREEN, C.BOLD)}",
            ]
            print(box(lines, color_style=SEVERITY_COLOR[severity], width=50))
            violations.append((plate, zone_name, speed, fine, severity))

        if not ask_yes_no("Scan another vehicle?"):
            break

    if violations:
        print(color(f"\n  Session total: {len(violations)} violation(s), "
                     f"${sum(v[3] for v in violations):,.2f} in fines.", C.BOLD, C.BRIGHT_CYAN))
    press_enter()


# ==============================================================================
# 🚦 MODULE 2 — SMART TRAFFIC MANAGEMENT SYSTEM
# ==============================================================================

def module_traffic() -> None:
    module_banner("🚦", "Smart Traffic Management System", C.BRIGHT_YELLOW)
    print(color("Enter live vehicle counts waiting at each approach.", C.DIM))
    print(color("The signal will allocate green-light time proportionally.\n", C.DIM))

    directions = ["North", "South", "East", "West"]
    counts = {}
    for d in directions:
        counts[d] = ask_int(f"Vehicles waiting — {d}: ", min_value=0)

    total = sum(counts.values())
    if total == 0:
        print(color("\nNo traffic reported — signal stays on default 15s cycles.", C.YELLOW))
        press_enter()
        return

    min_green, max_green, cycle_pool = 8, 60, 90
    allocations = {}
    for d in directions:
        share = counts[d] / total
        allocations[d] = max(min_green, min(max_green, round(share * cycle_pool)))

    print()
    spinner("Optimizing signal timing...", 1.2)
    print(color("\nADAPTIVE SIGNAL PLAN", C.BOLD, C.BRIGHT_CYAN))
    print(color("-" * 40, C.DIM))
    for d in directions:
        bar = "█" * int(allocations[d] / 2)
        print(f"  {d:<6} {counts[d]:>3} cars  {color(bar, C.BRIGHT_GREEN)} {allocations[d]}s green")
    print(color("-" * 40, C.DIM))

    print(color("\nSimulating one live cycle:\n", C.DIM))
    for d in directions:
        secs = allocations[d]
        demo_secs = min(secs, 5)  # keep the live demo short
        for remaining in range(demo_secs, 0, -1):
            sys.stdout.write(
                f"\r  {color('●', C.BRIGHT_GREEN)} {d} GREEN — {remaining}s "
                f"(full allocation: {secs}s)   "
            )
            sys.stdout.flush()
            time.sleep(0.3)
        clear_line()
        sys.stdout.write(f"\r  {color('●', C.BRIGHT_YELLOW)} {d} YELLOW — clearing intersection   ")
        sys.stdout.flush()
        time.sleep(0.4)
        clear_line()
        print(f"  {color('●', C.BRIGHT_RED)} {d} RED — {allocations[d]}s allocated this cycle")

    print(color("\n  ✓ Signal plan applied. Busiest approach gets the longest green.", C.BRIGHT_GREEN))
    press_enter()


# ==============================================================================
# 🩸 MODULE 3 — EMERGENCY BLOOD DONOR FINDER
# ==============================================================================

BLOOD_TYPES = ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"]

SAMPLE_DONORS = [
    {"name": "Ayesha Rahman", "blood_type": "O-", "location": "Chattogram", "phone": "01711-000111"},
    {"name": "Tanvir Alam", "blood_type": "A+", "location": "Dhaka", "phone": "01822-000222"},
    {"name": "Farhana Kabir", "blood_type": "B+", "location": "Chattogram", "phone": "01933-000333"},
    {"name": "Rafiq Islam", "blood_type": "AB+", "location": "Sylhet", "phone": "01644-000444"},
    {"name": "Nusrat Jahan", "blood_type": "O+", "location": "Chattogram", "phone": "01555-000555"},
]


def module_blood() -> None:
    module_banner("🩸", "Emergency Blood Donor Finder", C.BRIGHT_RED)
    donors = list(SAMPLE_DONORS)
    print(color(f"Registry loaded: {len(donors)} sample donors on file.\n", C.DIM))

    while True:
        action = ask_choice("What would you like to do?", [
            "Search donors by blood type",
            "Register a new donor",
            "List all donors",
            "Back to main menu",
        ])

        if action == "Search donors by blood type":
            bt = ask_choice("Blood type needed:", BLOOD_TYPES)
            spinner("Searching registry...", 0.8)
            matches = [d for d in donors if d["blood_type"] == bt]
            if matches:
                print(color(f"\n  🩸 {len(matches)} donor(s) found for {bt}:", C.BOLD, C.BRIGHT_RED))
                for d in matches:
                    print(f"   • {d['name']}  |  {d['location']}  |  {d['phone']}")
            else:
                print(color(f"\n  No donors on file for {bt} yet.", C.YELLOW))

        elif action == "Register a new donor":
            name = ask_text("Donor name: ")
            bt = ask_choice("Blood type:", BLOOD_TYPES)
            loc = ask_text("Location/city: ")
            phone = ask_text("Phone number: ")
            donors.append({"name": name, "blood_type": bt, "location": loc, "phone": phone})
            print(color(f"\n  ✓ {name} registered as a {bt} donor. Thank you! 🩸", C.BRIGHT_GREEN))

        elif action == "List all donors":
            print(color(f"\n  All donors ({len(donors)}):", C.BOLD, C.BRIGHT_CYAN))
            for d in donors:
                print(f"   • {d['name']:<18} {d['blood_type']:<4} {d['location']:<12} {d['phone']}")

        else:
            break
        print()

    press_enter()


# ==============================================================================
# 🗑️ MODULE 4 — GARBAGE COLLECTION REPORTING SYSTEM
# ==============================================================================

PRIORITY_KEYWORDS = {
    "hazard": "High", "medical": "High", "overflow": "High",
    "smell": "Medium", "blocked": "Medium",
}


def guess_priority(description: str) -> str:
    desc = description.lower()
    for keyword, level in PRIORITY_KEYWORDS.items():
        if keyword in desc:
            return level
    return "Low"


PRIORITY_COLOR = {"High": C.BRIGHT_RED, "Medium": C.BRIGHT_YELLOW, "Low": C.BRIGHT_GREEN}


def module_garbage() -> None:
    module_banner("🗑️", "Garbage Collection Reporting System", C.GREEN)
    reports = []

    while True:
        action = ask_choice("Choose an action:", [
            "Report an uncollected garbage spot",
            "View all reports",
            "Mark a report resolved",
            "Back to main menu",
        ])

        if action == "Report an uncollected garbage spot":
            location = ask_text("Location (street / landmark): ")
            desc = ask_text("Brief description: ")
            priority = guess_priority(desc)
            report = {
                "id": len(reports) + 1,
                "location": location,
                "description": desc,
                "priority": priority,
                "status": "Open",
                "timestamp": now_str(),
            }
            reports.append(report)
            spinner("Filing report...", 0.6)
            print(color(f"\n  ✓ Report #{report['id']} filed — priority auto-detected: "
                         f"{color(priority, PRIORITY_COLOR[priority])}", C.BRIGHT_GREEN))

        elif action == "View all reports":
            if not reports:
                print(color("\n  No reports filed yet.", C.YELLOW))
            else:
                print(color(f"\n  {len(reports)} report(s):", C.BOLD, C.BRIGHT_CYAN))
                for r in sorted(reports, key=lambda x: {"High": 0, "Medium": 1, "Low": 2}[x["priority"]]):
                    status_color = C.BRIGHT_GREEN if r["status"] == "Resolved" else C.BRIGHT_YELLOW
                    print(
                        f"   #{r['id']} [{color(r['priority'], PRIORITY_COLOR[r['priority']])}] "
                        f"{r['location']} — {r['description']} "
                        f"({color(r['status'], status_color)})"
                    )

        elif action == "Mark a report resolved":
            if not reports:
                print(color("\n  No reports to update.", C.YELLOW))
            else:
                rid = ask_int("Report ID to mark resolved: ", min_value=1)
                match = next((r for r in reports if r["id"] == rid), None)
                if match:
                    match["status"] = "Resolved"
                    print(color(f"\n  ✓ Report #{rid} marked resolved. Nice work! 🧹", C.BRIGHT_GREEN))
                else:
                    print(color("\n  No report with that ID.", C.RED))

        else:
            break
        print()

    press_enter()


# ==============================================================================
# 🍲 MODULE 5 — FOOD WASTE REDISTRIBUTION SYSTEM
# ==============================================================================

def module_food_waste() -> None:
    module_banner("🍲", "Food Waste Redistribution System", C.BRIGHT_YELLOW)
    listings = [
        {"id": 1, "item": "Cooked rice & curry (20 servings)", "donor": "Green Leaf Restaurant",
         "expires_hours": 4, "location": "Agrabad", "claimed": False},
        {"id": 2, "item": "Bread & pastries (15 kg)", "donor": "City Bakery",
         "expires_hours": 10, "location": "GEC Circle", "claimed": False},
    ]
    next_id = 3

    while True:
        action = ask_choice("Choose an action:", [
            "Donate surplus food",
            "View available food",
            "Claim a listing for a shelter/food bank",
            "Back to main menu",
        ])

        if action == "Donate surplus food":
            item = ask_text("Food item & quantity: ")
            donor = ask_text("Donor / restaurant name: ")
            expires = ask_float("Safe to consume for how many more hours?: ", min_value=0.5)
            loc = ask_text("Pickup location: ")
            listings.append({
                "id": next_id, "item": item, "donor": donor,
                "expires_hours": expires, "location": loc, "claimed": False,
            })
            spinner("Publishing listing...", 0.6)
            print(color(f"\n  ✓ Listing #{next_id} published. Thank you for reducing waste! 🍲", C.BRIGHT_GREEN))
            next_id += 1

        elif action == "View available food":
            available = [l for l in listings if not l["claimed"]]
            if not available:
                print(color("\n  No surplus food listed right now.", C.YELLOW))
            else:
                print(color(f"\n  {len(available)} listing(s) available "
                             f"(soonest expiry first):", C.BOLD, C.BRIGHT_CYAN))
                for l in sorted(available, key=lambda x: x["expires_hours"]):
                    urgency = C.BRIGHT_RED if l["expires_hours"] <= 4 else C.BRIGHT_GREEN
                    print(
                        f"   #{l['id']} {l['item']} — {l['donor']} @ {l['location']} "
                        f"({color(f'{l['expires_hours']:.1f}h left', urgency)})"
                    )

        elif action == "Claim a listing for a shelter/food bank":
            available = [l for l in listings if not l["claimed"]]
            if not available:
                print(color("\n  Nothing to claim right now.", C.YELLOW))
            else:
                lid = ask_int("Listing ID to claim: ", min_value=1)
                match = next((l for l in listings if l["id"] == lid and not l["claimed"]), None)
                if match:
                    org = ask_text("Your organization name: ")
                    match["claimed"] = True
                    print(color(f"\n  ✓ {org} claimed listing #{lid}: {match['item']}. "
                                 f"Coordinate pickup at {match['location']}.", C.BRIGHT_GREEN))
                else:
                    print(color("\n  No unclaimed listing with that ID.", C.RED))

        else:
            break
        print()

    press_enter()


# ==============================================================================
# 📚 MODULE 6 — FREE EDUCATION RESOURCE FINDER
# ==============================================================================

EDUCATION_RESOURCES = [
    {"subject": "Mathematics", "title": "Khan Academy — Full Math Curriculum", "type": "Course",
     "note": "Free, self-paced, K-12 through calculus"},
    {"subject": "Programming", "title": "freeCodeCamp", "type": "Course",
     "note": "Free certifications in web dev, Python, data science"},
    {"subject": "Science", "title": "MIT OpenCourseWare", "type": "Lecture Notes + Video",
     "note": "Full university-level science & engineering courses"},
    {"subject": "Language Learning", "title": "Duolingo", "type": "App",
     "note": "Free gamified language courses"},
    {"subject": "Programming", "title": "CS50 by Harvard (edX)", "type": "Course",
     "note": "Free intro to computer science, certificate optional fee"},
    {"subject": "General/K-12", "title": "OpenStax", "type": "Textbooks",
     "note": "Free peer-reviewed textbooks, downloadable PDFs"},
    {"subject": "Mathematics", "title": "Brilliant (free tier)", "type": "Interactive Course",
     "note": "Problem-solving based math & logic"},
]


def module_education() -> None:
    module_banner("📚", "Free Education Resource Finder", C.BRIGHT_BLUE)
    subjects = sorted(set(r["subject"] for r in EDUCATION_RESOURCES))

    while True:
        keyword = ask_text("Search a subject/keyword (or press Enter to browse all): ")
        spinner("Searching open education database...", 0.9)

        if keyword:
            results = [r for r in EDUCATION_RESOURCES
                       if keyword.lower() in r["subject"].lower()
                       or keyword.lower() in r["title"].lower()]
        else:
            results = EDUCATION_RESOURCES

        if not results:
            print(color(f"\n  No resources found for '{keyword}'. Try: "
                         f"{', '.join(subjects)}", C.YELLOW))
        else:
            print(color(f"\n  📚 {len(results)} resource(s) found:\n", C.BOLD, C.BRIGHT_CYAN))
            for r in results:
                print(f"   • {color(r['title'], C.BOLD)}  [{r['type']}]")
                print(f"     {color(r['subject'], C.DIM)} — {r['note']}")

        if not ask_yes_no("\nSearch again?"):
            break
        print()

    press_enter()


# ==============================================================================
# 💧 MODULE 7 — WATER LEAKAGE DETECTION SYSTEM
# ==============================================================================

LEAK_THRESHOLD_LPH = 5.0  # liters/hour of unexplained flow = suspected leak


def module_water() -> None:
    module_banner("💧", "Water Leakage Detection System", C.BRIGHT_CYAN)
    print(color("Enter meter readings to check for unexplained flow (a leak signature).\n", C.DIM))

    zones_checked = 0
    leaks_found = 0

    while True:
        zone = ask_text("Zone / property name: ")
        prev = ask_float("Previous meter reading (liters): ", min_value=0)
        curr = ask_float("Current meter reading (liters): ", min_value=0)
        hours = ask_float("Hours elapsed between readings: ", min_value=0.1)

        spinner("Analyzing flow pattern...", 1.0)
        used = curr - prev
        rate = used / hours if hours else 0
        zones_checked += 1

        print(color(f"\n  Flow rate: {rate:.2f} L/hour", C.BOLD))

        if used < 0:
            print(color("  ⚠ Reading error: current reading is lower than previous.", C.RED))
        elif rate > LEAK_THRESHOLD_LPH:
            leaks_found += 1
            flash(f"  💧 POSSIBLE LEAK DETECTED — {zone.upper()} 💧", times=3,
                  c1=C.BRIGHT_CYAN, c2=C.BRIGHT_RED)
            lines = [
                f"{color('Zone:', C.BOLD)} {zone}",
                f"{color('Flow rate:', C.BOLD)} {rate:.2f} L/h (threshold {LEAK_THRESHOLD_LPH} L/h)",
                f"{color('Recommendation:', C.BOLD)} Inspect pipes/fixtures for leaks.",
            ]
            print(box(lines, color_style=C.BRIGHT_RED, width=50))
        else:
            print(color(f"  ✓ {zone} flow is within normal range.\n", C.BRIGHT_GREEN))

        if not ask_yes_no("Check another zone?"):
            break

    print(color(f"\n  Session summary: {zones_checked} zone(s) checked, "
                 f"{leaks_found} possible leak(s) flagged.", C.BOLD, C.BRIGHT_CYAN))
    press_enter()


# ==============================================================================
# MAIN LOOP
# ==============================================================================

MODULE_DISPATCH = {
    "1": module_speeding,
    "2": module_traffic,
    "3": module_blood,
    "4": module_garbage,
    "5": module_food_waste,
    "6": module_education,
    "7": module_water,
}


def opening_sequence() -> None:
    clear_screen()
    turtle_intro()          # tries turtle graphics, falls back automatically
    clear_screen()
    print_title()
    fade_in_lines([
        "  Seven tools. One console. Real community impact.",
    ], style=C.DIM, delay=0.05)
    loading_bar("  Loading civic modules", duration=1.1, fill_color=C.BRIGHT_GREEN)
    print()


def main() -> None:
    enable_ansi_on_windows()
    opening_sequence()

    while True:
        show_menu()
        choice = input(color("\n  Enter your choice: ", C.BOLD, C.BRIGHT_CYAN)).strip()

        if choice == "0":
            clear_screen()
            typewriter("Thank you for using Civic Shield. Stay safe out there. 🛡️",
                       delay=0.02, style=C.BOLD + C.BRIGHT_CYAN)
            break

        handler = MODULE_DISPATCH.get(choice)
        if handler:
            try:
                handler()
            except EOFError:
                break
        else:
            print(color("  Invalid choice — pick a number from the menu.\n", C.RED))

        clear_screen()
        print_title()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(color("\n\nSession interrupted. Goodbye! 🛡️", C.YELLOW))