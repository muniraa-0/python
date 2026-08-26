"""
==============================================================================
   RADAR EYE - Animated Speed Enforcement Console System
==============================================================================
A police-console style Python program with ASCII art, color, typewriter
text animation, a simulated radar scan, flashing violation alerts, and an
end-of-session ASCII bar-chart dashboard.

No external dependencies - uses only the Python standard library, so it
runs anywhere with `python3 radar_eye.py`.

How speed is measured:
    Classic two-point method (same as real speed cameras): a vehicle is
    timed crossing a known distance between two sensors.
    speed = distance / time

How fines are calculated:
    Tiered penalty system - the further over the limit, the steeper the
    per-km/h rate.
==============================================================================
"""

import os
import sys
import time
import random
import json
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


# ==============================================================================
# TERMINAL COLOR / STYLE ENGINE  (pure ANSI escape codes, no dependencies)
# ==============================================================================

class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    BLINK = "\033[5m"

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
    """Make ANSI escape codes work in older Windows terminals."""
    if os.name == "nt":
        os.system("")


def clear_line():
    sys.stdout.write("\r" + " " * 90 + "\r")
    sys.stdout.flush()


def color(text: str, *styles: str) -> str:
    return "".join(styles) + text + C.RESET


# ==============================================================================
# ANIMATION HELPERS
# ==============================================================================

def typewriter(text: str, delay: float = 0.018, style: str = "") -> None:
    """Print text one character at a time, like an old terminal typing it out."""
    for ch in text:
        sys.stdout.write(style + ch + (C.RESET if style else ""))
        sys.stdout.flush()
        time.sleep(delay)
    print()


def loading_bar(label: str, duration: float = 1.4, width: int = 30,
                 fill_color: str = C.BRIGHT_CYAN) -> None:
    """Animated progress bar, e.g. for 'scanning radar' or 'processing plate'."""
    steps = 24
    for i in range(steps + 1):
        filled = int(width * i / steps)
        bar = "█" * filled + "░" * (width - filled)
        pct = int(100 * i / steps)
        sys.stdout.write(f"\r{label} {fill_color}[{bar}]{C.RESET} {pct:3d}%")
        sys.stdout.flush()
        time.sleep(duration / steps)
    print()


def radar_sweep(duration: float = 1.6) -> None:
    """A little rotating radar-dish animation, purely decorative."""
    frames = ["|", "/", "-", "\\"]
    blips = ["·", "•", "∘", "○"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        frame = frames[i % len(frames)]
        blip = random.choice(blips)
        sys.stdout.write(
            f"\r  {C.BRIGHT_GREEN}[RADAR {frame}]{C.RESET} "
            f"scanning for vehicles {color(blip, C.DIM)}   "
        )
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    clear_line()


def flash_alert(text: str, times: int = 4, delay: float = 0.15) -> None:
    """Flash a warning message on/off like a police siren light."""
    for i in range(times):
        sys.stdout.write(f"\r{color(text, C.BOLD, C.BRIGHT_RED)}")
        sys.stdout.flush()
        time.sleep(delay)
        clear_line()
        sys.stdout.write(f"\r{color(text, C.BOLD, C.BRIGHT_YELLOW)}")
        sys.stdout.flush()
        time.sleep(delay)
        clear_line()
    print(color(text, C.BOLD, C.BRIGHT_RED))


def siren_bar() -> None:
    """A quick red/blue flashing bar for dramatic effect above a citation."""
    pattern = [C.BG_RED, C.BG_BLUE] * 3
    for bg in pattern:
        sys.stdout.write(f"\r{bg}{' ' * 60}{C.RESET}")
        sys.stdout.flush()
        time.sleep(0.07)
    clear_line()


# ==============================================================================
# ASCII ART
# ==============================================================================

BANNER = r"""
 ____          _              ______            
|  _ \ __ _  __| | __ _ _ __  / ____|_   _  ___  
| |_) / _` |/ _` |/ _` | '__| | |    | | | |/ _ \ 
|  _ < (_| | (_| | (_| | |    | |___ | |_| |  __/ 
|_| \_\__,_|\__,_|\__,_|_|     \_____|\__, |\___| 
                                       |___/       
       S P E E D   E N F O R C E M E N T
"""

CAR_ICON = r"""
        ______
      _/______\_,
     |  ___  __ )
    '-()---()-'
"""

SIREN_ICON = "🚨" if sys.stdout.encoding and "UTF" in sys.stdout.encoding.upper() else "[!]"


def print_banner() -> None:
    print(color(BANNER, C.BOLD, C.BRIGHT_CYAN))
    print(color(CAR_ICON, C.BRIGHT_BLUE))


def box(text_lines: List[str], color_style: str = C.BRIGHT_CYAN, width: int = 56) -> str:
    """Wrap a list of text lines in a decorative box-drawing border."""
    top = "╔" + "═" * width + "╗"
    bottom = "╚" + "═" * width + "╝"
    body = []
    for line in text_lines:
        padded = line.ljust(width - 1)
        body.append(f"║ {padded}║")
    return color("\n".join([top] + body + [bottom]), color_style)


# ==============================================================================
# DATA MODELS
# ==============================================================================

@dataclass
class Zone:
    name: str
    speed_limit_kmh: float
    distance_m: float


@dataclass
class Violation:
    plate_number: str
    zone_name: str
    speed_limit_kmh: float
    measured_speed_kmh: float
    excess_kmh: float
    fine_amount: float
    timestamp: str
    severity: str

    def to_dict(self) -> dict:
        return {
            "plate_number": self.plate_number,
            "zone": self.zone_name,
            "speed_limit_kmh": self.speed_limit_kmh,
            "measured_speed_kmh": round(self.measured_speed_kmh, 1),
            "excess_kmh": round(self.excess_kmh, 1),
            "severity": self.severity,
            "fine_amount": self.fine_amount,
            "timestamp": self.timestamp,
        }


SEVERITY_COLOR = {
    "Minor": C.BRIGHT_YELLOW,
    "Moderate": C.YELLOW,
    "Severe": C.BRIGHT_RED,
    "Reckless": C.BOLD + C.BRIGHT_RED,
}

SEVERITY_ICON = {
    "Minor": "⚠",
    "Moderate": "⚠⚠",
    "Severe": "☠",
    "Reckless": "☠☠☠",
}


# ==============================================================================
# FINE CALCULATION
# ==============================================================================

FINE_TIERS = [
    (10, "Minor", 50, 5),
    (20, "Moderate", 100, 10),
    (40, "Severe", 250, 20),
    (float("inf"), "Reckless", 600, 35),
]


def calculate_fine(excess_kmh: float):
    if excess_kmh <= 0:
        return 0.0, "None"
    lower_bound = 0
    for max_excess, label, base_fine, rate_per_kmh in FINE_TIERS:
        if excess_kmh <= max_excess:
            amount_into_tier = excess_kmh - lower_bound
            fine = base_fine + amount_into_tier * rate_per_kmh
            return round(fine, 2), label
        lower_bound = max_excess
    return 0.0, "Reckless"


# ==============================================================================
# CORE SYSTEM
# ==============================================================================

class SpeedEnforcementSystem:
    def __init__(self):
        self.zones = {}
        self.violations: List[Violation] = []

    def add_zone(self, name, speed_limit_kmh, distance_m) -> None:
        self.zones[name] = Zone(name, speed_limit_kmh, distance_m)

    def detect_vehicle(self, plate_number, zone_name, time_seconds,
                        timestamp: Optional[str] = None) -> Optional[Violation]:
        if zone_name not in self.zones:
            raise ValueError(f"Unknown zone: {zone_name}")
        if time_seconds <= 0:
            raise ValueError("time_seconds must be positive")

        zone = self.zones[zone_name]
        speed_ms = zone.distance_m / time_seconds
        speed_kmh = speed_ms * 3.6

        if speed_kmh <= zone.speed_limit_kmh:
            return None

        excess = speed_kmh - zone.speed_limit_kmh
        fine, severity = calculate_fine(excess)

        violation = Violation(
            plate_number=plate_number,
            zone_name=zone.name,
            speed_limit_kmh=zone.speed_limit_kmh,
            measured_speed_kmh=speed_kmh,
            excess_kmh=excess,
            fine_amount=fine,
            timestamp=timestamp or datetime.now().isoformat(timespec="seconds"),
            severity=severity,
        )
        self.violations.append(violation)
        return violation

    def total_fines(self) -> float:
        return round(sum(v.fine_amount for v in self.violations), 2)

    def export_json(self, path: str) -> None:
        with open(path, "w") as f:
            json.dump([v.to_dict() for v in self.violations], f, indent=2)

    def counts_by_severity(self) -> dict:
        counts = {"Minor": 0, "Moderate": 0, "Severe": 0, "Reckless": 0}
        for v in self.violations:
            counts[v.severity] = counts.get(v.severity, 0) + 1
        return counts


# ==============================================================================
# INPUT HELPERS
# ==============================================================================

def ask_float(prompt: str, min_value: float = None) -> float:
    while True:
        raw = input(color(prompt, C.CYAN)).strip()
        try:
            value = float(raw)
            if min_value is not None and value <= min_value:
                print(color(f"  Please enter a number greater than {min_value}.", C.RED))
                continue
            return value
        except ValueError:
            print(color("  That's not a valid number, try again.", C.RED))


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


# ==============================================================================
# PRESENTATION LAYER (this is where the "engagement" happens)
# ==============================================================================

def show_citation(v: Violation) -> None:
    sev_color = SEVERITY_COLOR.get(v.severity, C.WHITE)
    sev_icon = SEVERITY_ICON.get(v.severity, "")

    siren_bar()
    flash_alert(f"  {SIREN_ICON} SPEED VIOLATION DETECTED {SIREN_ICON}  ", times=3, delay=0.12)

    lines = [
        f"{color('Plate:', C.BOLD)}          {v.plate_number}",
        f"{color('Zone:', C.BOLD)}           {v.zone_name}",
        f"{color('Speed limit:', C.BOLD)}    {v.speed_limit_kmh:.0f} km/h",
        f"{color('Measured speed:', C.BOLD)} {sev_color}{v.measured_speed_kmh:.1f} km/h{C.RESET}",
        f"{color('Excess:', C.BOLD)}         {sev_color}+{v.excess_kmh:.1f} km/h{C.RESET}",
        f"{color('Severity:', C.BOLD)}       {sev_color}{v.severity} {sev_icon}{C.RESET}",
        f"{color('Fine:', C.BOLD)}           {color(f'${v.fine_amount:,.2f}', C.BRIGHT_GREEN, C.BOLD)}",
        f"{color('Time:', C.BOLD)}           {v.timestamp}",
    ]
    print(box(lines, color_style=sev_color, width=50))
    print()


def show_clear(plate: str, speed_kmh: float, limit: float) -> None:
    msg = f"  ✓ {plate} clear — {speed_kmh:.1f} km/h in a {limit:.0f} km/h zone"
    print(color(msg, C.BRIGHT_GREEN))
    print()


def ascii_bar_chart(counts: dict) -> None:
    print(color("\n  VIOLATIONS BY SEVERITY", C.BOLD, C.BRIGHT_CYAN))
    print(color("  " + "-" * 40, C.DIM))
    max_count = max(counts.values()) if counts.values() else 0
    for severity, count in counts.items():
        bar_color = SEVERITY_COLOR.get(severity, C.WHITE)
        bar_len = int((count / max_count) * 25) if max_count else 0
        bar = "█" * bar_len
        print(f"  {severity:<10} {color(bar, bar_color)} {count}")
    print(color("  " + "-" * 40, C.DIM))


def show_dashboard(system: SpeedEnforcementSystem) -> None:
    total = len(system.violations)
    fines = system.total_fines()

    print()
    print(color("=" * 56, C.BRIGHT_CYAN))
    typewriter("   SESSION DASHBOARD", delay=0.01, style=C.BOLD + C.BRIGHT_CYAN)
    print(color("=" * 56, C.BRIGHT_CYAN))

    loading_bar("  Compiling report", duration=1.0)

    summary_lines = [
        f"Total violations:        {color(str(total), C.BOLD, C.BRIGHT_RED)}",
        f"Total fines issued:      {color(f'${fines:,.2f}', C.BOLD, C.BRIGHT_GREEN)}",
    ]
    print(box(summary_lines, color_style=C.BRIGHT_CYAN, width=50))

    if total:
        ascii_bar_chart(system.counts_by_severity())

        worst = max(system.violations, key=lambda v: v.excess_kmh)
        print()
        print(color(
            f"  🏁 Worst offender: {worst.plate_number} at "
            f"{worst.measured_speed_kmh:.1f} km/h "
            f"(+{worst.excess_kmh:.1f} over limit) in {worst.zone_name}",
            C.BOLD, C.BRIGHT_MAGENTA
        ))
    print()


# ==============================================================================
# SETUP FLOWS
# ==============================================================================

def setup_zones(system: SpeedEnforcementSystem) -> None:
    typewriter("STEP 1 — Configure monitored road zones", delay=0.012, style=C.BOLD + C.BRIGHT_YELLOW)
    print(color("A zone is a stretch of road with two sensors a known distance apart.\n", C.DIM))

    if ask_yes_no("Use default sample zones (School Zone, Highway, Bridge)?"):
        loading_bar("  Loading default zones", duration=0.9, fill_color=C.BRIGHT_GREEN)
        system.add_zone("Main Street School Zone", speed_limit_kmh=30, distance_m=100)
        system.add_zone("Highway 7 North", speed_limit_kmh=100, distance_m=500)
        system.add_zone("Downtown Bridge", speed_limit_kmh=50, distance_m=200)
        print(color("  ✓ Default zones loaded.\n", C.BRIGHT_GREEN))
        return

    while True:
        name = input(color("\nZone name: ", C.CYAN)).strip()
        limit = ask_float("Speed limit (km/h): ", min_value=0)
        distance = ask_float("Distance between sensors (meters): ", min_value=0)
        system.add_zone(name, limit, distance)
        print(color(f"  ✓ Zone '{name}' added ({limit} km/h limit, {distance} m gap).", C.BRIGHT_GREEN))
        if not ask_yes_no("Add another zone?"):
            break


def process_vehicles(system: SpeedEnforcementSystem) -> int:
    """Returns the number of vehicles that passed WITHOUT a violation."""
    typewriter("\nSTEP 2 — Live vehicle detection", delay=0.012, style=C.BOLD + C.BRIGHT_YELLOW)
    zone_names = list(system.zones.keys())
    clear_count = 0

    if not zone_names:
        print(color("No zones configured — nothing to detect.", C.RED))
        return 0

    while True:
        print()
        plate = input(color("Vehicle plate number: ", C.CYAN)).strip().upper()
        zone_name = ask_choice("Which zone did it pass through?", zone_names)
        transit_time = ask_float("Time taken to cross the zone (seconds): ", min_value=0)

        radar_sweep(duration=1.3)
        loading_bar("  Calculating speed", duration=0.8, fill_color=C.BRIGHT_MAGENTA)

        result = system.detect_vehicle(plate, zone_name, transit_time)
        if result:
            show_citation(result)
        else:
            zone = system.zones[zone_name]
            speed_kmh = (zone.distance_m / transit_time) * 3.6
            show_clear(plate, speed_kmh, zone.speed_limit_kmh)
            clear_count += 1

        if not ask_yes_no("Scan another vehicle?"):
            break

    return clear_count


# ==============================================================================
# MAIN
# ==============================================================================

system_clear_count = 0  # tracked globally just for the dashboard easter-egg line


def main():
    enable_ansi_on_windows()
    global system_clear_count

    os.system("cls" if os.name == "nt" else "clear") if ask_yes_no_safe() else None
    print_banner()
    typewriter("Welcome, Officer. Booting radar console...", delay=0.02, style=C.BRIGHT_CYAN)
    loading_bar("  System initializing", duration=1.2, fill_color=C.BRIGHT_GREEN)
    print()

    system = SpeedEnforcementSystem()
    setup_zones(system)
    system_clear_count = process_vehicles(system)

    show_dashboard(system)

    if system.violations and ask_yes_no("Save violation log to violations.json?"):
        system.export_json("violations.json")
        print(color("  ✓ Saved to violations.json", C.BRIGHT_GREEN))

    typewriter("\nSession complete. Drive safe out there.", delay=0.02, style=C.BOLD + C.BRIGHT_CYAN)


def ask_yes_no_safe() -> bool:
    """Wrapper so a screen-clear is optional and never crashes non-interactive runs."""
    try:
        return ask_yes_no("Clear the screen for a clean start?")
    except EOFError:
        return False


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(color("\n\nSession interrupted by user. Goodbye, Officer.", C.YELLOW))