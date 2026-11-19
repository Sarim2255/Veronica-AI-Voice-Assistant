"""
Main Application Entry Point for VERONICA AI Voice Assistant.
Implements an ultra-futuristic Iron Man / JARVIS HUD desktop interface using CustomTkinter.
Features:
- Animated Holographic Arc Reactor Canvas with multi-ring rotation & dynamic state animations.
- Guaranteed Female Voice Output (Microsoft Zira / SAPI-5 Female).
- Full verbal responses (speaks aloud for date, time, questions, calculations, and commands).
- Live HUD Digital Clock, Date, and System Telemetry Badges.
- Multithreaded non-blocking architecture (60 FPS smooth GUI).
- Interactive Sliders for Voice Speed (WPM) and Volume (%).
- Quick-action Tactical Command Grid (Time, Date, Apps, Sites, Search, Diagnostics).
- Real-Time Tactical HUD Log with color-coded transaction events.
- Command Transceiver bar for hybrid voice and typed command testing.
"""

import math
import os
import sys
import threading
import time
from datetime import datetime
import tkinter as tk
import customtkinter as ctk

from command_handler import CommandHandler
from config import (
    ACCENT_COLOR,
    ACCENT_GOLD,
    ACCENT_GOLD_HOVER,
    ACCENT_HOVER,
    ASSISTANT_NAME,
    ASSISTANT_TAGLINE,
    BG_COLOR_DARK,
    CARD_BG_COLOR,
    CARD_BORDER_COLOR,
    DEFAULT_VOICE_RATE,
    DEFAULT_VOICE_VOLUME,
    ICON_PATH,
    PANEL_BG,
    STATUS_ERROR,
    STATUS_IDLE,
    STATUS_LISTENING,
    STATUS_PROCESSING,
    STATUS_SPEAKING,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    THEME_MODE,
)
from speech_engine import SpeechEngine
from voice_assistant import VoiceAssistant

# Set CustomTkinter theme
ctk.set_appearance_mode(THEME_MODE)
ctk.set_default_color_theme("blue")


class ArcReactorHUDCanvas(tk.Canvas):
    """
    Futuristic Iron Man Arc Reactor & Holographic HUD Canvas.
    Renders rotating mechanical rings, energy coils, pulsating core,
    and dynamic audio soundwave spectrum animations.
    """

    def __init__(self, master, width=400, height=270, **kwargs):
        super().__init__(
            master,
            width=width,
            height=height,
            bg="#070c17",
            highlightthickness=0,
            **kwargs,
        )
        self.width = width
        self.height = height
        self.angle_outer = 0.0
        self.angle_inner = 0.0
        self.pulse_phase = 0.0
        self.mode = "idle"  # 'idle', 'listening', 'processing', 'speaking'
        self.animating = True
        self._animate()

    def set_mode(self, mode: str):
        """Set visualizer mode ('idle', 'listening', 'processing', 'speaking')."""
        self.mode = mode

    def _animate(self):
        """Redraw the HUD Arc Reactor frame every 33ms (~30 FPS)."""
        if not self.animating:
            return

        self.delete("all")
        cx = self.width / 2
        cy = self.height / 2

        # 1. Background HUD Target Reticle & Crosshairs
        self.create_line(cx - 150, cy, cx + 150, cy, fill="#102035", width=1, dash=(3, 6))
        self.create_line(cx, cy - 110, cx, cy + 110, fill="#102035", width=1, dash=(3, 6))

        # Corner HUD brackets
        corner_len = 16
        pad_x, pad_y = 12, 10
        # Top-Left
        self.create_line(pad_x, pad_y, pad_x + corner_len, pad_y, fill="#1b3654", width=2)
        self.create_line(pad_x, pad_y, pad_x, pad_y + corner_len, fill="#1b3654", width=2)
        # Top-Right
        self.create_line(self.width - pad_x, pad_y, self.width - pad_x - corner_len, pad_y, fill="#1b3654", width=2)
        self.create_line(self.width - pad_x, pad_y, self.width - pad_x, pad_y + corner_len, fill="#1b3654", width=2)
        # Bottom-Left
        self.create_line(pad_x, self.height - pad_y, pad_x + corner_len, self.height - pad_y, fill="#1b3654", width=2)
        self.create_line(pad_x, self.height - pad_y, pad_x, self.height - pad_y - corner_len, fill="#1b3654", width=2)
        # Bottom-Right
        self.create_line(self.width - pad_x, self.height - pad_y, self.width - pad_x - corner_len, self.height - pad_y, fill="#1b3654", width=2)
        self.create_line(self.width - pad_x, self.height - pad_y, self.width - pad_x, self.height - pad_y - corner_len, fill="#1b3654", width=2)

        # 2. Outer Rotating Degree Ring (R ~ 108px)
        r_outer = 108
        self.create_oval(
            cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer,
            outline="#162e4a", width=1.5
        )

        # Degree Tick Marks
        num_ticks = 36
        tick_speed = 0.015 if self.mode != "processing" else 0.05
        self.angle_outer += tick_speed

        for i in range(num_ticks):
            theta = self.angle_outer + (i * (2 * math.pi / num_ticks))
            is_major = (i % 9 == 0)
            is_mid = (i % 3 == 0)

            t_len = 8 if is_major else (5 if is_mid else 3)
            r1 = r_outer - t_len
            r2 = r_outer

            x1 = cx + r1 * math.cos(theta)
            y1 = cy + r1 * math.sin(theta)
            x2 = cx + r2 * math.cos(theta)
            y2 = cy + r2 * math.sin(theta)

            tick_color = ACCENT_COLOR if is_major else ("#2c527a" if is_mid else "#18324f")
            self.create_line(x1, y1, x2, y2, fill=tick_color, width=1.5 if is_major else 1)

        # 3. Middle Counter-Rotating Tactical Arc Ring (R ~ 82px)
        r_mid = 82
        mid_speed = 0.025 if self.mode != "processing" else 0.08
        self.angle_inner -= mid_speed

        # 3 Segmented Tactical Arcs
        for seg in range(3):
            start_deg = math.degrees(self.angle_inner) + (seg * 120)
            extent_deg = 70
            arc_color = ACCENT_COLOR
            if self.mode == "listening":
                arc_color = STATUS_LISTENING
            elif self.mode == "processing":
                arc_color = ACCENT_GOLD
            elif self.mode == "speaking":
                arc_color = "#00f0ff"

            self.create_arc(
                cx - r_mid, cy - r_mid, cx + r_mid, cy + r_mid,
                start=start_deg, extent=extent_deg,
                outline=arc_color, width=2.5, style=tk.ARC
            )

            # Orbiting Satellite Nodes on the middle ring
            node_angle = math.radians(start_deg + (extent_deg / 2))
            nx = cx + r_mid * math.cos(node_angle)
            ny = cy - r_mid * math.sin(node_angle)
            self.create_oval(nx - 3, ny - 3, nx + 3, ny + 3, fill=arc_color, outline="#ffffff", width=1)

        # 4. Arc Reactor Inner Coils (R ~ 55px)
        r_coil = 55
        self.create_oval(
            cx - r_coil, cy - r_coil, cx + r_coil, cy + r_coil,
            outline="#1c385c", width=1.5
        )
        for c in range(12):
            coil_theta = c * (2 * math.pi / 12)
            cx1 = cx + 38 * math.cos(coil_theta)
            cy1 = cy + 38 * math.sin(coil_theta)
            cx2 = cx + r_coil * math.cos(coil_theta)
            cy2 = cy + r_coil * math.sin(coil_theta)
            coil_color = "#00f0ff" if (c % 3 == 0) else "#1a4066"
            if self.mode == "speaking":
                coil_color = ACCENT_GOLD if (c % 2 == 0) else "#00f0ff"
            self.create_line(cx1, cy1, cx2, cy2, fill=coil_color, width=2)

        # 5. Dynamic Mode Animations (Center Reactor Core & Shockwaves)
        self.pulse_phase += 0.12

        if self.mode == "listening":
            # Quantum Emerald Sonar Waves & Dynamic Equalizer Bars
            core_color = STATUS_LISTENING

            # Pulsing Sonar shockwaves
            for wave_idx in range(3):
                wave_r = 20 + ((self.pulse_phase * 15 + wave_idx * 28) % 75)
                self.create_oval(
                    cx - wave_r, cy - wave_r, cx + wave_r, cy + wave_r,
                    outline=STATUS_LISTENING, width=1.5
                )

            # Center Glowing Core
            pulse_r = 16 + 4 * math.sin(self.pulse_phase * 2)
            self.create_oval(cx - pulse_r, cy - pulse_r, cx + pulse_r, cy + pulse_r, fill=core_color, outline="#ffffff", width=1.5)

            # Audio Equalizer Frequency Bars across the bottom horizon
            bar_count = 25
            bar_spacing = 11
            start_x = cx - (bar_count * bar_spacing) / 2
            bar_y = self.height - 24
            for b in range(bar_count):
                bx = start_x + (b * bar_spacing)
                h = 18 * abs(math.sin(self.pulse_phase * 1.5 + b * 0.4)) + 4
                self.create_line(bx, bar_y - h, bx, bar_y, fill=STATUS_LISTENING, width=3, capstyle=tk.ROUND)

            # Status watermark text
            self.create_text(cx, cy + 86, text="[ ACOUSTIC CAPTURE ACTIVE ]", fill=STATUS_LISTENING, font=("Consolas", 8, "bold"))

        elif self.mode == "speaking":
            # Holographic Arc Core Flare & Voice Shockwaves
            core_color = "#00f0ff"

            # Concentric voice expansion rings
            for wave_idx in range(3):
                wave_r = 24 + ((self.pulse_phase * 20 + wave_idx * 30) % 80)
                self.create_oval(
                    cx - wave_r, cy - wave_r, cx + wave_r, cy + wave_r,
                    outline=ACCENT_GOLD if wave_idx % 2 == 0 else "#00f0ff", width=2
                )

            # High-energy pulsing reactor iris
            pulse_r = 18 + 7 * abs(math.sin(self.pulse_phase * 2.2))
            self.create_oval(cx - pulse_r, cy - pulse_r, cx + pulse_r, cy + pulse_r, fill="#072b47", outline="#00f0ff", width=2)
            self.create_oval(cx - 10, cy - 10, cx + 10, cy + 10, fill="#ffffff", outline=ACCENT_GOLD, width=1.5)

            # Symmetrical Audio harmonics
            for side in [-1, 1]:
                for h_idx in range(6):
                    hx = cx + side * (r_mid + 15 + h_idx * 8)
                    amp = 14 * abs(math.sin(self.pulse_phase * 2 + h_idx * 0.7)) + 3
                    self.create_line(hx, cy - amp, hx, cy + amp, fill="#00f0ff", width=2)

            self.create_text(cx, cy + 86, text="[ VERONICA VOICE SYNTHESIS ]", fill=ACCENT_COLOR, font=("Consolas", 8, "bold"))

        elif self.mode == "processing":
            # High-speed Tactical Radar & Target Analysis
            core_color = STATUS_PROCESSING
            # Sweeping radar line
            sweep_angle = self.pulse_phase * 3.5
            sx = cx + 65 * math.cos(sweep_angle)
            sy = cy + 65 * math.sin(sweep_angle)
            self.create_line(cx, cy, sx, sy, fill=STATUS_PROCESSING, width=2)

            # Target Lock Brackets around center
            lock_r = 26
            self.create_rectangle(cx - lock_r, cy - lock_r, cx + lock_r, cy + lock_r, outline=STATUS_PROCESSING, width=1.5)

            # Center core
            self.create_oval(cx - 10, cy - 10, cx + 10, cy + 10, fill=core_color, outline="#ffffff", width=1)
            self.create_text(cx, cy + 86, text="[ ANALYZING PROTOCOL ]", fill=STATUS_PROCESSING, font=("Consolas", 8, "bold"))

        else:
            # Standby Gentle Cyan Breathing Pulse
            breathe = 13 + 3.5 * math.sin(self.pulse_phase * 0.6)
            self.create_oval(cx - breathe, cy - breathe, cx + breathe, cy + breathe, fill="#0a253d", outline="#00f0ff", width=1.5)
            self.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill="#00f0ff", outline="#ffffff", width=1)
            self.create_text(cx, cy + 86, text="[ ARC REACTOR // STANDBY ]", fill="#3b5e82", font=("Consolas", 8, "bold"))

        self.after(33, self._animate)


class VeronicaGUI(ctk.CTk):
    """
    Main desktop graphical user interface for the VERONICA AI Assistant.
    Futuristic Iron Man HUD styling with real-time telemetry, responsive controls,
    voice synthesis, and automation triggers.
    """

    def __init__(self):
        super().__init__()

        # Window Geometry & Setup
        self.title("VERONICA — Tactical AI Voice Assistant [MK-IV]")
        self.geometry("1160x760")
        self.minsize(1040, 700)
        self.configure(fg_color=BG_COLOR_DARK)

        # Set Icon if available
        if os.path.exists(ICON_PATH):
            try:
                self.iconbitmap(ICON_PATH)
            except Exception as e:
                print(f"[GUI] Note: Could not set window icon: {e}")

        # Core Engines
        self.speech_engine = SpeechEngine(
            on_speak_callback=self._on_assistant_speak_threadsafe,
            on_speak_finished_callback=self._on_assistant_speak_finished_threadsafe,
        )
        self.command_handler = CommandHandler(
            speech_engine=self.speech_engine,
            ui_callback=self._on_assistant_reply_threadsafe,
            on_exit_callback=self._on_assistant_exit_threadsafe,
            on_clear_callback=self._on_clear_history_threadsafe,
        )
        self.voice_assistant = VoiceAssistant(
            command_handler=self.command_handler,
            status_callback=self._on_status_change_threadsafe,
            recognized_callback=self._on_recognized_text_threadsafe,
        )

        # Build HUD Interface
        self._build_hud_header()
        self._build_cockpit_body()

        # Handle Window Close Gracefully
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Start HUD Clock
        self._update_hud_clock()

    # ------------------ TOP HUD BANNER ------------------

    def _build_hud_header(self):
        """Construct top Iron Man HUD banner with branding, status pill, and digital clock."""
        header_frame = ctk.CTkFrame(
            self,
            fg_color=PANEL_BG,
            corner_radius=12,
            border_width=1,
            border_color=CARD_BORDER_COLOR,
        )
        header_frame.pack(fill="x", padx=16, pady=(12, 6))

        # Left Branding
        brand_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        brand_frame.pack(side="left", padx=18, pady=8)

        title_lbl = ctk.CTkLabel(
            brand_frame,
            text=f"⚡ {ASSISTANT_NAME.upper()}  //  MK-IV",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=ACCENT_COLOR,
        )
        title_lbl.pack(anchor="w")

        sub_lbl = ctk.CTkLabel(
            brand_frame,
            text=ASSISTANT_TAGLINE,
            font=ctk.CTkFont(family="Consolas", size=9, weight="bold"),
            text_color=TEXT_SECONDARY,
        )
        sub_lbl.pack(anchor="w")

        # Center Status Hologram Pill
        center_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        center_frame.pack(side="left", fill="x", expand=True, padx=20)

        self.hud_status_badge = ctk.CTkLabel(
            center_frame,
            text="[ ◉ SYSTEM ONLINE // VERONICA MK-IV READY ]",
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=STATUS_IDLE,
            fg_color="#060c18",
            corner_radius=8,
            padx=16,
            pady=6,
        )
        self.hud_status_badge.pack(anchor="center")

        # Right HUD Digital Clock & Calendar
        clock_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        clock_frame.pack(side="right", padx=18, pady=8)

        self.time_lbl = ctk.CTkLabel(
            clock_frame,
            text="",
            font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            text_color=ACCENT_COLOR,
        )
        self.time_lbl.pack(anchor="e")

        self.date_lbl = ctk.CTkLabel(
            clock_frame,
            text="",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            text_color=TEXT_SECONDARY,
        )
        self.date_lbl.pack(anchor="e")

    # ------------------ MAIN THREE-COLUMN COCKPIT BODY ------------------

    def _build_cockpit_body(self):
        """Construct the 3-panel Iron Man HUD cockpit grid."""
        body_frame = ctk.CTkFrame(self, fg_color="transparent")
        body_frame.pack(fill="both", expand=True, padx=16, pady=6)

        # ----------------- COLUMN 1: LEFT HUD (Systems & Voice Matrix) -----------------
        left_col = ctk.CTkFrame(
            body_frame,
            width=300,
            fg_color=PANEL_BG,
            corner_radius=12,
            border_width=1,
            border_color=CARD_BORDER_COLOR,
        )
        left_col.pack(side="left", fill="y", padx=(0, 10))
        left_col.pack_propagate(False)

        # Panel Header
        ctk.CTkLabel(
            left_col,
            text="SYSTEM DIAGNOSTICS & TELEMETRY",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            text_color=ACCENT_COLOR,
        ).pack(pady=(12, 6), padx=14, anchor="w")

        # Telemetry Status Readouts
        diag_box = ctk.CTkFrame(left_col, fg_color="#060c18", corner_radius=8, border_width=1, border_color="#14263d")
        diag_box.pack(fill="x", padx=14, pady=4)

        diag_items = [
            ("CORE EFFICIENCY", "99.8% [OPTIMAL]"),
            ("VOICE MODEL", f"FEMALE ({self.speech_engine.get_voice_name().split('-')[0].strip()})"),
            ("ACOUSTIC SENSORS", "CALIBRATED (ACTIVE)"),
            ("NEURAL LINK", "SYNCHRONIZED"),
            ("ORBITAL LINK", "STARKNET SECURE"),
        ]
        for label, val in diag_items:
            row = ctk.CTkFrame(diag_box, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=2)
            ctk.CTkLabel(row, text=label, font=ctk.CTkFont(family="Consolas", size=9), text_color=TEXT_SECONDARY).pack(side="left")
            ctk.CTkLabel(row, text=val, font=ctk.CTkFont(family="Consolas", size=9, weight="bold"), text_color="#7cd6ff").pack(side="right")

        # Sliders: Speech Rate and Volume Tuning
        ctk.CTkLabel(
            left_col,
            text="VOICE SYNTHESIS MATRIX",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            text_color=ACCENT_COLOR,
        ).pack(pady=(12, 4), padx=14, anchor="w")

        sliders_card = ctk.CTkFrame(left_col, fg_color="#060c18", corner_radius=8, border_width=1, border_color="#14263d")
        sliders_card.pack(fill="x", padx=14, pady=4)

        # Rate slider
        rate_hdr = ctk.CTkFrame(sliders_card, fg_color="transparent")
        rate_hdr.pack(fill="x", padx=10, pady=(6, 2))
        ctk.CTkLabel(rate_hdr, text="Voice Speed", font=ctk.CTkFont(size=11), text_color=TEXT_SECONDARY).pack(side="left")
        self.rate_val_lbl = ctk.CTkLabel(rate_hdr, text=f"{DEFAULT_VOICE_RATE} WPM", font=ctk.CTkFont(family="Consolas", size=11, weight="bold"), text_color=ACCENT_COLOR)
        self.rate_val_lbl.pack(side="right")

        self.rate_slider = ctk.CTkSlider(
            sliders_card,
            from_=100,
            to=250,
            number_of_steps=15,
            progress_color=ACCENT_COLOR,
            button_color=ACCENT_COLOR,
            command=self._on_rate_slider_changed,
        )
        self.rate_slider.set(DEFAULT_VOICE_RATE)
        self.rate_slider.pack(fill="x", padx=10, pady=(0, 6))

        # Volume slider
        vol_hdr = ctk.CTkFrame(sliders_card, fg_color="transparent")
        vol_hdr.pack(fill="x", padx=10, pady=(2, 2))
        ctk.CTkLabel(vol_hdr, text="Voice Volume", font=ctk.CTkFont(size=11), text_color=TEXT_SECONDARY).pack(side="left")
        self.vol_val_lbl = ctk.CTkLabel(vol_hdr, text=f"{int(DEFAULT_VOICE_VOLUME * 100)}%", font=ctk.CTkFont(family="Consolas", size=11, weight="bold"), text_color=ACCENT_COLOR)
        self.vol_val_lbl.pack(side="right")

        self.vol_slider = ctk.CTkSlider(
            sliders_card,
            from_=0.0,
            to=1.0,
            number_of_steps=20,
            progress_color=ACCENT_COLOR,
            button_color=ACCENT_COLOR,
            command=self._on_vol_slider_changed,
        )
        self.vol_slider.set(DEFAULT_VOICE_VOLUME)
        self.vol_slider.pack(fill="x", padx=10, pady=(0, 8))

        # Tactical Quick Action Grid (Cyberpunk Buttons)
        ctk.CTkLabel(
            left_col,
            text="TACTICAL COMMAND PROTOCOLS",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            text_color=ACCENT_COLOR,
        ).pack(pady=(12, 4), padx=14, anchor="w")

        grid_frame = ctk.CTkFrame(left_col, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=12, pady=4)

        quick_cmds = [
            ("🕒 System Time", "what is the time"),
            ("📅 Today's Date", "what is today's date"),
            ("🌐 YouTube", "open youtube"),
            ("🔍 Google Search", "search latest ai technology"),
            ("🧮 Calculator", "launch calculator"),
            ("📝 Notepad", "open notepad"),
            ("⚙️ Diagnostics", "system status"),
            ("🧹 Clear HUD", "clear history"),
        ]

        for idx, (label, cmd_text) in enumerate(quick_cmds):
            r = idx // 2
            c = idx % 2
            btn = ctk.CTkButton(
                grid_frame,
                text=label,
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                fg_color="#0e1b2e",
                hover_color="#183256",
                border_width=1,
                border_color="#1e3a5f",
                text_color=TEXT_PRIMARY,
                height=32,
                corner_radius=6,
                command=lambda ct=cmd_text: self._trigger_quick_command(ct),
            )
            btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
            grid_frame.grid_columnconfigure(c, weight=1)

        # ----------------- COLUMN 2: CENTER HUD (The Holographic Arc Reactor) -----------------
        center_col = ctk.CTkFrame(
            body_frame,
            fg_color=PANEL_BG,
            corner_radius=12,
            border_width=1,
            border_color=CARD_BORDER_COLOR,
        )
        center_col.pack(side="left", fill="both", expand=True, padx=0)

        # Center Section Header
        ctk.CTkLabel(
            center_col,
            text="HOLOGRAPHIC ARC REACTOR CORE",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=ACCENT_COLOR,
        ).pack(pady=(10, 4))

        # The Stunning Animated Arc Reactor Canvas
        self.arc_visualizer = ArcReactorHUDCanvas(center_col, width=420, height=270)
        self.arc_visualizer.pack(pady=2, padx=14)

        # Live Status Readout Banner
        self.status_banner = ctk.CTkLabel(
            center_col,
            text="● STANDBY  //  WAITING FOR INSTRUCTION",
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=STATUS_IDLE,
            fg_color="#060c18",
            corner_radius=8,
            padx=14,
            pady=5,
        )
        self.status_banner.pack(fill="x", padx=18, pady=(4, 8))

        # Giant Glowing Primary Voice Control Button
        self.voice_toggle_btn = ctk.CTkButton(
            center_col,
            text="🎙  INITIALIZE VOICE LISTENING",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color="#00a86b",
            hover_color="#008a57",
            text_color="#ffffff",
            height=46,
            corner_radius=10,
            command=self.toggle_voice_listening,
        )
        self.voice_toggle_btn.pack(fill="x", padx=18, pady=4)

        # Veronica Latest Response Box (Hero Display)
        resp_frame = ctk.CTkFrame(
            center_col,
            fg_color="#060c18",
            corner_radius=10,
            border_width=1,
            border_color="#183256",
        )
        resp_frame.pack(fill="both", expand=True, padx=18, pady=(8, 12))

        resp_title_row = ctk.CTkFrame(resp_frame, fg_color="transparent")
        resp_title_row.pack(fill="x", padx=12, pady=(8, 2))
        ctk.CTkLabel(
            resp_title_row,
            text="VERONICA VOICE OUTPUT [TRANSMITTED]",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            text_color=ACCENT_COLOR,
        ).pack(side="left")

        self.resp_time_tag = ctk.CTkLabel(
            resp_title_row,
            text="ONLINE",
            font=ctk.CTkFont(family="Consolas", size=9),
            text_color=TEXT_SECONDARY,
        )
        self.resp_time_tag.pack(side="right")

        self.response_text = ctk.CTkTextbox(
            resp_frame,
            wrap="word",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color="#040810",
            text_color=TEXT_PRIMARY,
            corner_radius=6,
            border_width=1,
            border_color="#14263d",
        )
        self.response_text.pack(fill="both", expand=True, padx=12, pady=(2, 10))
        self.response_text.insert(
            "1.0",
            f"Greetings, sir. I am {ASSISTANT_NAME}. All orbital and HUD systems are online. "
            "Click 'INITIALIZE VOICE LISTENING' or transmit a command to begin."
        )
        self.response_text.configure(state="disabled")

        # ----------------- COLUMN 3: RIGHT HUD (Tactical Telemetry Log & Transceiver) -----------------
        right_col = ctk.CTkFrame(
            body_frame,
            width=360,
            fg_color=PANEL_BG,
            corner_radius=12,
            border_width=1,
            border_color=CARD_BORDER_COLOR,
        )
        right_col.pack(side="right", fill="both", padx=(10, 0))
        right_col.pack_propagate(False)

        # Tactical Log Header
        log_hdr = ctk.CTkFrame(right_col, fg_color="transparent")
        log_hdr.pack(fill="x", padx=14, pady=(10, 4))

        ctk.CTkLabel(
            log_hdr,
            text="TACTICAL TELEMETRY & EVENT LOG",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            text_color=ACCENT_COLOR,
        ).pack(side="left")

        ctk.CTkButton(
            log_hdr,
            text="🧹 Clear",
            width=50,
            height=22,
            font=ctk.CTkFont(size=10),
            fg_color="#0e1b2e",
            hover_color="#183256",
            command=self.clear_history,
        ).pack(side="right")

        # Log Terminal Box
        self.history_box = ctk.CTkTextbox(
            right_col,
            wrap="word",
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color="#050a14",
            text_color="#c8e1ff",
            corner_radius=8,
            border_width=1,
            border_color="#14263d",
        )
        self.history_box.pack(fill="both", expand=True, padx=14, pady=(0, 8))
        self.history_box.configure(state="disabled")

        # Command Transceiver Bar (Supports typed commands with instant speech & action)
        input_container = ctk.CTkFrame(right_col, fg_color="#060c18", corner_radius=10, border_width=1, border_color="#183256")
        input_container.pack(fill="x", padx=14, pady=(0, 12))

        self.cmd_entry = ctk.CTkEntry(
            input_container,
            placeholder_text="❯ Transmit command (e.g. 'what time is it', 'open youtube')...",
            font=ctk.CTkFont(size=12),
            fg_color="#040810",
            border_color="#14263d",
            height=38,
            corner_radius=6,
        )
        self.cmd_entry.pack(side="left", fill="x", expand=True, padx=(8, 6), pady=8)
        self.cmd_entry.bind("<Return>", lambda event: self.send_manual_command())

        self.transmit_btn = ctk.CTkButton(
            input_container,
            text="TRANSMIT ⚡",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color=ACCENT_COLOR,
            hover_color=ACCENT_HOVER,
            text_color="#000000",
            width=92,
            height=38,
            corner_radius=6,
            command=self.send_manual_command,
        )
        self.transmit_btn.pack(side="right", padx=(0, 8), pady=8)

    # ------------------ EVENT HANDLERS & CALLBACKS ------------------

    def _update_hud_clock(self):
        """Update live HUD digital clock and calendar date."""
        now = datetime.now()
        self.time_lbl.configure(text=f"[ {now.strftime('%I:%M:%S %p')} ]")
        self.date_lbl.configure(text=f"[ {now.strftime('%a, %d %b %Y').upper()} ]")
        self.after(1000, self._update_hud_clock)

    def _on_rate_slider_changed(self, value):
        """Update speech speed setting."""
        val = int(value)
        self.rate_val_lbl.configure(text=f"{val} WPM")
        self.speech_engine.set_rate(val)

    def _on_vol_slider_changed(self, value):
        """Update speech volume setting."""
        val = float(value)
        self.vol_val_lbl.configure(text=f"{int(val * 100)}%")
        self.speech_engine.set_volume(val)

    def toggle_voice_listening(self):
        """Toggle microphone listening state."""
        if not self.voice_assistant.is_active():
            self.voice_toggle_btn.configure(
                text="⏹  DISENGAGE LISTENING",
                fg_color="#b3261e",
                hover_color="#8c1d18",
            )
            self.voice_assistant.start()
        else:
            self.voice_assistant.stop()
            self.voice_toggle_btn.configure(
                text="🎙  INITIALIZE VOICE LISTENING",
                fg_color="#00a86b",
                hover_color="#008a57",
            )
            self._on_status_change_threadsafe("Standby // Disengaged", "idle")

    def _trigger_quick_command(self, cmd_text: str):
        """Execute quick command button."""
        self.append_history(f"[ACTION] Triggered protocol: '{cmd_text}'")
        def _exec():
            self._on_status_change_threadsafe("Analyzing Protocol...", "processing")
            self.command_handler.process(cmd_text)
            if self.voice_assistant.is_active():
                self._on_status_change_threadsafe("Acoustic Sensor Online & Listening", "listening")
            else:
                self._on_status_change_threadsafe("Standby // Disengaged", "idle")
        threading.Thread(target=_exec, daemon=True).start()

    def send_manual_command(self):
        """Execute command typed into the transceiver input."""
        text = self.cmd_entry.get().strip()
        if not text:
            return
        self.cmd_entry.delete(0, "end")
        self.append_history(f"[USER] {text}")

        def _exec():
            self._on_status_change_threadsafe("Analyzing Transceiver Command...", "processing")
            self.command_handler.process(text)
            if self.voice_assistant.is_active():
                self._on_status_change_threadsafe("Acoustic Sensor Online & Listening", "listening")
            else:
                self._on_status_change_threadsafe("Standby // Disengaged", "idle")

        threading.Thread(target=_exec, daemon=True).start()

    def clear_history(self):
        """Wipes HUD command history log."""
        self.history_box.configure(state="normal")
        self.history_box.delete("1.0", "end")
        self.history_box.configure(state="disabled")

    def append_history(self, line: str):
        """Append formatted timestamped line to transaction log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.history_box.configure(state="normal")
        self.history_box.insert("end", f"[{timestamp}] {line}\n")
        self.history_box.configure(state="disabled")
        self.history_box.see("end")

    def set_response_display(self, text: str):
        """Update hero card with assistant verbal statement."""
        self.resp_time_tag.configure(text=f"TRANSMITTED {datetime.now().strftime('%H:%M:%S')}")
        self.response_text.configure(state="normal")
        self.response_text.delete("1.0", "end")
        self.response_text.insert("1.0", text)
        self.response_text.configure(state="disabled")

    # ------------------ THREAD-SAFE DISPATCHERS ------------------

    def _on_status_change_threadsafe(self, status_text: str, color_key: str):
        """Thread-safe status and arc reactor mode update."""
        def _ui_update():
            color_map = {
                "idle": (STATUS_IDLE, "idle"),
                "listening": (STATUS_LISTENING, "listening"),
                "processing": (STATUS_PROCESSING, "processing"),
                "speaking": (STATUS_SPEAKING, "speaking"),
                "error": (STATUS_ERROR, "idle"),
            }
            color, vis_mode = color_map.get(color_key, (STATUS_IDLE, "idle"))
            self.status_banner.configure(
                text=f"● {status_text.upper()}",
                text_color=color,
            )
            self.hud_status_badge.configure(
                text=f"[ ◉ {status_text.upper()} ]",
                text_color=color,
            )
            self.arc_visualizer.set_mode(vis_mode)

        self.after(0, _ui_update)

    def _on_recognized_text_threadsafe(self, recognized_text: str):
        """Thread-safe logging of user spoken audio transcript."""
        self.after(0, lambda: self.append_history(f"[VOICE] {recognized_text}"))

    def _on_assistant_speak_threadsafe(self, spoken_text: str):
        """Thread-safe update when Veronica speaks aloud."""
        def _ui():
            self.set_response_display(spoken_text)
            self.append_history(f"[{ASSISTANT_NAME.upper()}] {spoken_text}")
            self.arc_visualizer.set_mode("speaking")
        self.after(0, _ui)

    def _on_assistant_speak_finished_threadsafe(self):
        """Thread-safe update when Veronica finishes speaking aloud."""
        def _ui():
            if self.voice_assistant.is_active():
                self._on_status_change_threadsafe("Acoustic Sensor Online & Listening", "listening")
            else:
                self._on_status_change_threadsafe("Standby // Disengaged", "idle")
        self.after(0, _ui)

    def _on_assistant_reply_threadsafe(self, reply_text: str):
        """Thread-safe response update."""
        self.after(0, lambda: self.set_response_display(reply_text))

    def _on_assistant_exit_threadsafe(self):
        """Shutdown handler when voice exit command is issued."""
        def _ui():
            self.voice_assistant.stop()
            self.after(1600, self.destroy)
        self.after(0, _ui)

    def _on_clear_history_threadsafe(self):
        """Thread-safe clear HUD."""
        self.after(0, self.clear_history)

    def on_closing(self):
        """Handle window closing event."""
        self.arc_visualizer.animating = False
        self.voice_assistant.stop()
        self.destroy()


# Alias for backwards compatibility
JarvisGUI = VeronicaGUI


def main():
    """Main application launcher."""
    app = VeronicaGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
