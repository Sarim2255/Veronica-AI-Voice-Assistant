# ⚡ VERONICA — Advanced Iron Man Tactical AI Voice Assistant [MK-IV]

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![GUI Framework](https://img.shields.io/badge/GUI-CustomTkinter%20HUD-00f0ff.svg?logo=tkinter&logoColor=black)](https://customtkinter.tomschimansky.com/)
[![Speech Engine](https://img.shields.io/badge/TTS-Microsoft%20Zira%20(Female)-ffb800.svg)](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ee125663(v=vs.85))
[![Speech Recognition](https://img.shields.io/badge/STT-Google%20Speech%20API-00ff9d.svg)](https://pypi.org/project/SpeechRecognition/)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-0078d4.svg?logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

> An intelligent, futuristic desktop AI voice assistant engineered in Python with an authentic **Iron Man / JARVIS cockpit HUD** interface. Named **VERONICA** (*inspired by Tony Stark's orbital combat intelligence system*), it listens to user voice commands in real time, executes automation workflows across Windows applications and web platforms, solves math problems, queries Wikipedia, and **verbally speaks every answer aloud** using an expressive **female voice** (Microsoft Zira SAPI-5).

---

## 📑 Table of Contents
1. [🌟 Key Features & Architectural Highlights](#-key-features--architectural-highlights)
2. [🖥️ Iron Man HUD Interface Overview](#️-iron-man-hud-interface-overview)
3. [🛠️ Technology Stack](#️-technology-stack)
4. [📋 Prerequisites & System Requirements](#-prerequisites--system-requirements)
5. [📥 Step-by-Step Installation Instructions](#-step-by-step-installation-instructions)
6. [▶️ How to Run the Assistant](#️-how-to-run-the-assistant)
7. [🗣️ User Guide & Operating Instructions](#️-user-guide--operating-instructions)
8. [🚀 Complete Voice Commands Reference](#-complete-voice-commands-reference)
9. [🧪 Automated Testing & Verification Guide](#-automated-testing--verification-guide)
10. [📤 How to Upload the Project to GitHub](#-how-to-upload-the-project-to-github)
11. [📁 Repository Structure](#-repository-structure)
12. [🔧 Troubleshooting & FAQ](#-troubleshooting--faq)
13. [👤 Author & Internship Details](#-author--internship-details)

---

## 🌟 Key Features & Architectural Highlights

- **🔊 Expressive Female Voice Synthesis (TTS):** Engineered with native Windows SAPI-5 female voice synthesis (**Microsoft Zira**). Every single response—from date and time to math and web confirmations—is **spoken aloud** through the speakers rather than printed to the terminal.
- **⚡ Iron Man Holographic HUD Interface:** CustomTkinter dark-mode cockpit HUD featuring an animated **Arc Reactor Canvas** running at 30 FPS with rotating degree-notched mechanical rings, tactical arcs, and dynamic voice frequency spectrum visualizations.
- **🎙️ Acoustic Speech Recognition:** Real-time microphone listening via `SpeechRecognition` with dynamic ambient noise calibration to filter out computer fans and background hum.
- **🧠 Cognitive Intelligence & Math Solver:** Evaluates spoken arithmetic calculations (e.g., *"calculate 25 times 4"*) and extracts 2-sentence summaries from Wikipedia (e.g., *"who is Tony Stark"*).
- **🌐 Web & Media Automation:** Instantly launches 8 popular websites (YouTube, Google, Gmail, GitHub, LinkedIn, Stack Overflow, Naukri, Instagram) and plays any song or artist on YouTube via PyWhatKit.
- **💻 Desktop Application Automation:** Launches core Windows desktop applications (Notepad, Calculator, MS Paint, Command Prompt, File Explorer, VS Code, Settings).
- **⚡ Non-Blocking Multithreaded Architecture:** Microphone listening, command processing, application spawning, and voice synthesis run on dedicated worker threads, ensuring the GUI remains silky-smooth at 60 FPS without ever showing `(Not Responding)`.
- **💰 Zero Paid APIs:** Built completely with local SAPI-5 TTS, free Google Speech Recognition, and standard open-source Python libraries.

---

## 🖥️ Iron Man HUD Interface Overview

The interface is structured into a 3-column tactical cockpit dashboard:

```text
+----------------------------------------------------------------------------------------------------+
| ⚡ VERONICA // MK-IV     [ ◉ SYSTEM ONLINE // READY ]             [ 04:05:12 PM ] [ 19 NOV 2026 ]  |
+----------------------------------------------------------------------------------------------------+
| LEFT PANEL (300px)         | CENTER PANEL (FLUID EXPAND)              | RIGHT PANEL (360px)        |
|                            |                                          |                            |
| ⚙️ SYSTEM DIAGNOSTICS      |         ◎ HOLOGRAPHIC ARC REACTOR        | 📜 TACTICAL TELEMETRY LOG  |
| - Core Status: 99.8%       |         (Animated 30 FPS Multi-Ring Core | [16:05:01] [VERONICA] Ready|
| - Voice: Microsoft Zira    |          Outer Ticks, Arcs & Soundwaves) | [16:05:05] [USER] Time     |
| - Sensors: Calibrated      |                                          | [16:05:06] [VERONICA] 4 PM |
|                            | ● STANDBY // WAITING FOR INSTRUCTION     |                            |
| 🎚️ VOICE SYNTH MATRIX     |                                          |                            |
| - Speed Slider (WPM)       | [ 🎙 INITIALIZE VOICE LISTENING ]        |                            |
| - Volume Slider (%)        |                                          |                            |
|                            | 💬 VERONICA SPOKEN OUTPUT [TRANSMITTED]  | ⌨️ COMMAND TRANSCEIVER     |
| 🎯 QUICK ACTION GRID       | "The current time is 04:05 PM, sir."     | [ ❯ Transmit command...  ] |
| [Time] [Date] [YouTube]    |                                          | [ TRANSMIT ⚡ ]            |
| [Calc] [Notes] [Clear]     |                                          |                            |
+----------------------------------------------------------------------------------------------------+
```

### Arc Reactor Dynamic States:
1. **Standby (Idle):** Gentle cyan breathing pulse with smooth gyroscopic ring rotations.
2. **Listening:** Concentric Quantum Emerald (`#00ff9d`) sonar waves ripple outward while an active equalizer frequency bar graph dances along the horizon.
3. **Processing:** Rings spin in hyper-drive rotation with laser targeting crosshairs and radar sweeps locking onto the core.
4. **Speaking:** Electric cyan and gold arc reactor flare with expanding voice shockwaves and audio harmonics.

---

## 🛠️ Technology Stack

| Technology | Purpose |
| :--- | :--- |
| **Python 3.10 - 3.13** | Core programming language |
| **CustomTkinter** | Modern, hardware-accelerated dark HUD desktop graphical interface |
| **Windows SAPI-5** | Native offline female voice synthesis (Microsoft Zira) |
| **comtypes / winsound** | Direct Windows audio streaming & thread-safe TTS playback |
| **SpeechRecognition** | Microphone capture and Google Speech-to-Text translation |
| **PyAudio** | PortAudio audio stream interface for real-time microphone capture |
| **PyWhatKit** | Automated YouTube song/video playback |
| **Wikipedia API** | Real-time general knowledge and encyclopedia queries |
| **Webbrowser / Urllib** | Browser tab dispatching and query encoding |
| **Subprocess / OS** | Non-blocking Windows desktop application launching |
| **Threading** | Decoupled background workers maintaining 60 FPS GUI responsiveness |

---

## 📋 Prerequisites & System Requirements

Before setting up VERONICA, verify your system meets the following prerequisites:

- **Operating System:** Windows 10 or Windows 11 (64-bit recommended).
- **Python:** Python 3.10, 3.11, 3.12, or 3.13 installed.
  - Make sure **"Add Python to PATH"** was checked during Python installation.
- **Hardware:**
  - Working microphone (headset, external USB mic, or built-in laptop mic).
  - Working speakers or headphones for hearing Veronica's verbal responses.
- **Internet Connection:** Required for Google Speech Recognition, YouTube playback, and Wikipedia queries.

---

## 📥 Step-by-Step Installation Instructions

### Step 1: Open Terminal in Project Directory
Open **PowerShell** or **Command Prompt** and navigate to the project directory:
```powershell
cd "d:\all\pynexia technology internship\ai_voice_assistant"
```

### Step 2: Create a Virtual Environment (Recommended)
Isolate dependencies by creating a dedicated virtual environment:
```powershell
# Create virtual environment named 'myvenv'
python -m venv myvenv
```

### Step 3: Activate the Virtual Environment
- **On PowerShell:**
  ```powershell
  .\myvenv\Scripts\Activate.ps1
  ```
  *(If PowerShell displays a script execution policy error, run: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`)*

- **On Command Prompt (CMD):**
  ```cmd
  myvenv\Scripts\activate.bat
  ```

### Step 4: Install Required Packages
Install all pinned dependencies using `requirements.txt`:
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> [!TIP]
> **Note on PyAudio on Windows:**  
> If `pip install PyAudio` encounters a compiler warning on your system, install the precompiled wheel using pipwin:
> ```powershell
> pip install pipwin
> pipwin install pyaudio
> ```

---

## ▶️ How to Run the Assistant

You have two convenient ways to start VERONICA:

### Method 1: Using the One-Click Batch Launcher (Easiest)
Simply double-click the **`run_veronica.bat`** file located in the project folder.  
It automatically detects the virtual environment, initializes the audio drivers, and launches the HUD!

### Method 2: Running from the Command Line
With your virtual environment activated:
```powershell
python main.py
```
Or directly specifying the virtual environment Python executable:
```powershell
.\myvenv\Scripts\python.exe main.py
```

---

## 🗣️ User Guide & Operating Instructions

### 1. Interacting via Voice (Microphone Mode)
1. Launch the application.
2. Click the large green **`🎙 INITIALIZE VOICE LISTENING`** button.
3. The button turns red (**`⏹ DISENGAGE LISTENING`**), and the Arc Reactor switches to emerald green sonar waves.
4. Speak your command clearly (e.g., *"Veronica, what is the time?"* or *"Open YouTube"*).
5. Veronica will:
   - Display what she heard in the Tactical Telemetry Log.
   - Switch the Arc Reactor to the golden **Speaking** animation.
   - **Verbally speak the answer out loud** through your speakers.
   - Execute the requested action (e.g., open a website or app).
6. To pause or stop microphone listening, click **`⏹ DISENGAGE LISTENING`** or say *"Exit"*.

### 2. Interacting via Typed Commands (Silent Transceiver Mode)
In quiet environments (such as a library or office):
1. Locate the **Command Transceiver Bar** at the bottom-right of the HUD.
2. Type any command (e.g., `what is the date`, `calculate 150 / 3`, `open notepad`).
3. Press **Enter** or click **`TRANSMIT ⚡`**.
4. Veronica immediately processes the command, updates the HUD, speaks the answer aloud, and executes the action!

### 3. Tuning Speech Speed and Volume
- **Voice Speed (WPM):** Drag the **Voice Speed Slider** on the left panel between **100 WPM** (deliberate, slow) and **250 WPM** (rapid). Default is `175 WPM`.
- **Voice Volume (%):** Drag the **Voice Volume Slider** between **0%** and **100%**.

### 4. Tactical Quick Action Buttons
On the left panel, click any of the 8 cyber-buttons for instant execution:
- `🕒 System Time` — Speaks current time aloud.
- `📅 Today's Date` — Speaks today's full date aloud.
- `🌐 YouTube` — Opens YouTube in a new tab.
- `🔍 Google Search` — Searches latest AI news.
- `🧮 Calculator` — Spawns Windows Calculator.
- `📝 Notepad` — Spawns Windows Notepad.
- `⚙️ Diagnostics` — Speaks system health and voice status.
- `🧹 Clear HUD` — Clears the transaction log.

---

## 🚀 Complete Voice Commands Reference

Veronica understands natural conversational language (e.g., *"Veronica, can you please tell me the time?"* or simply *"Time"*).

### 1. Date, Time & Conversational Queries (Always Spoken Aloud)
| Spoken Voice Command | Verbal Female Speech Response | Action / Display |
| :--- | :--- | :--- |
| `"What is the time?"` | *"The current time is 04:05 PM, sir."* | Speaks aloud + updates hero box |
| `"Tell me today's date"` | *"Today's date is Thursday, November 19, 2026, sir."* | Speaks aloud + updates hero box |
| `"What day is today?"` | *"Today is Thursday, sir."* | Speaks current day of the week |
| `"Hello"` / `"Hi Veronica"` | *"Good afternoon! I am Veronica. All systems operational. How may I assist you, sir?"* | Time-sensitive greeting |
| `"How are you?"` | *"All systems are operating at peak efficiency, sir. Ready for your command."* | System check |
| `"System status"` / `"Diagnostics"` | *"All systems nominal, sir. SAPI-5 female voice synthesis synchronized, acoustic sensors active, core efficiency at 99.8%."* | Full diagnostic report |
| `"Repeat that"` | *"I said: [Exact text of previous statement]"* | Repeats prior verbal statement |
| `"Clear history"` | *"Tactical HUD and transaction history have been cleared, sir."* | Wipes HUD transaction log |
| `"Help"` / `"What can you do?"` | Speaks overview and displays full 7-point capability summary. | Help documentation |
| `"Exit"` / `"Goodbye"` | *"Goodbye, sir. Deactivating Veronica systems. Have a wonderful day!"* | Safe application power-down |

### 2. Math Calculations & General Knowledge
| Spoken Voice Command | Verbal Female Speech Response | Action Performed |
| :--- | :--- | :--- |
| `"Calculate 25 times 4"` | *"The calculated result is 100, sir."* | Evaluates arithmetic expression |
| `"What is 50 plus 70?"` | *"The calculated result is 120, sir."* | Evaluates arithmetic expression |
| `"Calculate 150 divided by 3"`| *"The calculated result is 50, sir."* | Evaluates division |
| `"Who is Tony Stark?"` | Spoken 2-sentence summary from Wikipedia. | Queries Wikipedia online |
| `"What is machine learning?"` | Spoken 2-sentence summary from Wikipedia. | Queries Wikipedia online |

### 3. Website Automation (8 Core Sites + Custom URLs)
| Spoken Voice Command | Browser Action Performed | Verbal Confirmation |
| :--- | :--- | :--- |
| `"Open YouTube"` | Launches `https://www.youtube.com` | *"Opening Youtube in your browser, sir."* |
| `"Open Google"` | Launches `https://www.google.com` | *"Opening Google in your browser, sir."* |
| `"Open Gmail"` | Launches `https://mail.google.com` | *"Opening Gmail in your browser, sir."* |
| `"Open GitHub"` | Launches `https://www.github.com` | *"Opening Github in your browser, sir."* |
| `"Open LinkedIn"` | Launches `https://www.linkedin.com` | *"Opening Linkedin in your browser, sir."* |
| `"Open Stack Overflow"` | Launches `https://stackoverflow.com` | *"Opening Stack Overflow in your browser, sir."* |
| `"Open Naukri"` | Launches `https://www.naukri.com` | *"Opening Naukri in your browser, sir."* |
| `"Open Instagram"` | Launches `https://www.instagram.com` | *"Opening Instagram in your browser, sir."* |
| `"Open Facebook"` | Launches `https://www.facebook.com` | *"Opening Facebook in your browser, sir."* |

### 4. Desktop Application Automation (7 Core Apps)
| Spoken Voice Command | Windows Action Performed | Verbal Confirmation |
| :--- | :--- | :--- |
| `"Open Notepad"` | Spawns Windows Notepad (`notepad.exe`) | *"Launching Notepad, sir."* |
| `"Launch Calculator"` | Spawns Windows Calculator (`calc.exe`) | *"Launching Calculator, sir."* |
| `"Open Paint"` | Spawns MS Paint (`mspaint.exe`) | *"Launching Paint, sir."* |
| `"Open Command Prompt"` | Spawns Command Prompt terminal (`cmd.exe`) | *"Launching Command Prompt, sir."* |
| `"Open File Explorer"` | Launches Windows File Explorer (`explorer.exe`) | *"Launching File Explorer, sir."* |
| `"Open Visual Studio Code"` | Launches VS Code editor (`code`) | *"Launching Visual Studio Code, sir."* |
| `"Open Windows Settings"` | Launches Windows Settings app (`ms-settings:`) | *"Launching Windows Settings, sir."* |

### 5. Media Playback & Web Searching
| Spoken Voice Command | Action Performed | Verbal Confirmation |
| :--- | :--- | :--- |
| `"Play Believer"` | Automatically plays Believer by Imagine Dragons on YouTube | *"Playing 'believer' on YouTube, sir."* |
| `"Play Arijit Singh songs"` | Launches YouTube playing top Arijit Singh songs | *"Playing 'arijit singh songs' on YouTube, sir."* |
| `"Search Python programming"` | Opens Google search for *Python programming* | *"Searching Google for 'python programming', sir."* |
| `"Open a new tab"` | Opens a blank new tab in default web browser | *"Opening a new browser tab, sir."* |

---

## 🧪 Automated Testing & Verification Guide

Two automated testing suites are provided to examine and verify assistant functionality:

### Suite 1: Command Handler & Intent Parsing Test
Tests 16 regex intent variations, stripping of conversational prefixes, math solving, and response generation:
```powershell
.\myvenv\Scripts\python.exe test_assistant.py
```
**Expected Result:**
```text
=== VERONICA COMMAND HANDLER VERIFICATION ===
[+] PASSED [greetings]: 'hello' -> 'Good afternoon! I am Veronica...'
[+] PASSED [time]: 'Veronica, what is the time?' -> 'The current time is 04:05 PM, sir...'
[+] PASSED [date]: 'Can you please tell me today's date?' -> 'Today's date is Thursday...'
...
All 16 command pattern tests passed successfully!
```

### Suite 2: Full System & Hardware Integration Test
Tests SAPI-5 female voice detection, microphone hardware enumeration, URL dictionaries, app bindings, and GUI frame rendering:
```powershell
.\myvenv\Scripts\python.exe test_system_integration.py
```
**Expected Result:**
```text
=== STARTING VERONICA FULL SYSTEM INTEGRATION TEST ===
[1/5] Testing SpeechEngine initialization & Female Voice...
 -> SpeechEngine initialized successfully!
 -> Active Voice: Microsoft Zira Desktop - English (United States)
 -> Default Rate: 175 WPM, Volume: 100%
[2/5] Testing Microphone device availability...
 -> Found audio input device(s).
[3/5] Testing Automation mappings...
 -> All 8 requested websites mapped correctly.
 -> All requested desktop applications mapped correctly.
[4/5] Testing Command Variations...
 -> Successfully normalized all 6 variation patterns.
[5/5] Testing GUI Launch & Tear-down...
 -> CustomTkinter Iron Man HUD GUI initialized, rendered frame, and closed cleanly!
=== SYSTEM INTEGRATION TESTS COMPLETED SUCCESSFULLY ===
```

> 📖 **Need more test cases?** Check out [`TEST_CASES.md`](TEST_CASES.md) for 56 comprehensive test scenarios covering stress tests, edge cases, and hardware diagnostics!

---

## 📤 How to Upload the Project to GitHub

Follow these simple steps to upload the entire project to GitHub:

### Step 1: Open PowerShell in the Project Directory
```powershell
cd "d:\all\pynexia technology internship\ai_voice_assistant"
```

### Step 2: Initialize Git Repository
```powershell
git init
```

### Step 3: Stage and Commit Project Files
```powershell
git add .
git commit -m "feat: complete VERONICA AI voice assistant with Iron Man HUD and female voice"
```

> [!NOTE]
> The included `.gitignore` file automatically excludes `myvenv/`, `__pycache__/`, temporary `.wav` files, and crash logs so only clean source code is committed.

### Step 4: Link to Your GitHub Repository and Push
```powershell
# Rename branch to main
git branch -M main

# Link remote repository (replace with your GitHub URL)
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPOSITORY_NAME>.git

# Push source code to GitHub
git push -u origin main
```

---

## 📁 Repository Structure

```text
ai_voice_assistant/
│
├── 🟢 CORE RUNTIME MODULES
│   ├── main.py                     # Entry point: Iron Man HUD GUI & Arc Reactor Canvas
│   ├── speech_engine.py            # SAPI-5 female voice synthesis engine (Microsoft Zira)
│   ├── command_handler.py          # Intent parser, math solver, Wikipedia & responses
│   ├── automation.py               # Desktop apps, websites, YouTube & Google search
│   ├── voice_assistant.py          # Background microphone capture & Google STT
│   ├── config.py                   # Global constants, URLs, app mappings & theme colors
│   └── requirements.txt            # Python package dependencies
│
├── 🚀 LAUNCHERS & ASSETS
│   ├── run_veronica.bat            # One-click Windows batch launcher
│   └── assets/
│       └── jarvis_icon.ico         # Application window icon
│
├── 📚 COMPREHENSIVE DOCUMENTATION
│   ├── README.md                   # Complete project documentation & setup guide
│   ├── TEST_CASES.md               # 56-scenario master test suite & verification guide
│   ├── CODE_EXPLANATION.md         # Deep-dive line-by-line code & architecture guide
│   └── .gitignore                  # Git exclusion rules (ignores myvenv and cache)
│
└── 🧪 AUTOMATED TEST HARNESSES
    ├── test_assistant.py           # Command parsing verification suite
    └── test_system_integration.py  # Hardware & system integration test suite
```

---

## 🔧 Troubleshooting & FAQ

### Q1: The assistant is not speaking. How do I fix it?
- Ensure your speakers or headphones are connected and not muted in Windows.
- Open Windows **Settings > Time & Language > Speech** and verify that **Microsoft Zira (English - United States)** is installed.
- VERONICA's custom SAPI-5 engine writes audio directly to a stream and plays through `winsound`. If you adjusted the volume slider to 0%, slide it back up to 100%.

### Q2: `SpeechRecognition` gives an error or does not hear my voice.
- Check Windows **Settings > Privacy & Security > Microphone** and confirm **"Allow desktop apps to access your microphone"** is toggled **ON**.
- Check if your microphone is selected as the default input device in Windows Sound Settings.
- When you click **"INITIALIZE VOICE LISTENING"**, wait 1 second for ambient noise calibration to finish before speaking.

### Q3: `pip install PyAudio` fails during installation.
On some Windows installations without C++ build tools, PyAudio needs a precompiled wheel:
```powershell
pip install pipwin
pipwin install pyaudio
```

### Q4: Can I test the assistant without speaking into the microphone?
**Yes!** Type any command into the **Command Transceiver Bar** at the bottom right of the HUD and press **Enter**. Veronica will speak the answer aloud and execute the command identically to voice mode.

---

## 👤 Author & Internship Details

- **Developer:** Mohd Sarim Khan
- **Project Title:** VERONICA — Advanced Desktop AI Voice Assistant (MK-IV)
- **Internship:** Artificial Intelligence Internship
- **Organization:** Pynexia Technology
- **Submission Date:** November 2026

---

*Engineered with ❤️ for Pynexia Technology Internship.*
