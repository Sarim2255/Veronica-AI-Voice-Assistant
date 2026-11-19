"""
Configuration file for VERONICA AI Voice Assistant.
Contains application constants, supported URLs, application paths,
voice preferences, and Iron Man HUD theme configurations.
"""

import os
from typing import Dict, List

# Assistant Metadata
ASSISTANT_NAME: str = "Veronica"
ASSISTANT_TAGLINE: str = "ORBITAL INTELLIGENCE & TACTICAL HUD SYSTEM — MK-IV"
ASSISTANT_VERSION: str = "2.0.0"

# Default Speech Engine Settings
DEFAULT_VOICE_RATE: int = 175       # Words per minute (100 - 250)
DEFAULT_VOICE_VOLUME: float = 1.0   # Volume level (0.0 - 1.0)
SPEECH_RECOGNITION_TIMEOUT: int = 4
SPEECH_PHRASE_TIME_LIMIT: int = 7
ENERGY_THRESHOLD: int = 400
DYNAMIC_ENERGY_THRESHOLD: bool = True
RECOGNITION_TIMEOUT: int = 6

# Supported Websites Mapping (Retaining all guidelines)
WEBSITE_URLS: Dict[str, str] = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "gmail": "https://mail.google.com",
    "github": "https://www.github.com",
    "linkedin": "https://www.linkedin.com",
    "stack overflow": "https://stackoverflow.com",
    "stackoverflow": "https://stackoverflow.com",
    "naukri": "https://www.naukri.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
}

# Windows Desktop Applications Mapping (Retaining all guidelines)
APP_COMMANDS: Dict[str, str] = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "command prompt": "cmd.exe",
    "cmd": "cmd.exe",
    "file explorer": "explorer.exe",
    "explorer": "explorer.exe",
    "visual studio code": "code",
    "vs code": "code",
    "settings": "ms-settings:",
    "windows settings": "ms-settings:",
}

# Supported Wake Words / Trigger Prefixes
TRIGGER_WORDS: List[str] = [
    "veronica",
    "hey veronica",
    "hello veronica",
    "ok veronica",
    "okay veronica",
    "jarvis",
    "hey jarvis",
    "hello jarvis",
]

# Iron Man / VERONICA HUD Color Palette & Theme Constants
THEME_MODE: str = "dark"
BG_COLOR_DARK: str = "#050811"         # Deep Space Obsidian
PANEL_BG: str = "#080e1b"              # Cockpit Glass Dark Slate
CARD_BG_COLOR: str = "#0c1527"         # Tactical Panel Slate
CARD_BORDER_COLOR: str = "#162844"     # Glowing Panel Boundary
ACCENT_COLOR: str = "#00f0ff"          # Holographic Cyan / Electric Arc Blue
ACCENT_HOVER: str = "#00b8cc"
ACCENT_GOLD: str = "#ffb800"           # Arc Reactor Gold / Iron Man Gold
ACCENT_GOLD_HOVER: str = "#d49800"
TEXT_PRIMARY: str = "#e6f8ff"          # Holographic White-Cyan
TEXT_SECONDARY: str = "#6c8aa6"        # Tactical HUD Gray
STATUS_LISTENING: str = "#00ff9d"       # Quantum Emerald Green
STATUS_PROCESSING: str = "#ffaa00"      # Tactical Amber
STATUS_SPEAKING: str = "#00f0ff"        # Arc Core Cyan
STATUS_IDLE: str = "#455a75"            # Standby Slate
STATUS_ERROR: str = "#ff3366"           # Critical Red

# Assets Paths
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR: str = os.path.join(BASE_DIR, "assets")
ICON_PATH: str = os.path.join(ASSETS_DIR, "jarvis_icon.ico")
