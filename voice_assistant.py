"""
Voice Assistant Module for VERONICA.
Handles real-time microphone audio input, speech recognition using robust HTTPS Google Speech API,
ambient noise calibration, dual-language detection (English en-IN & Hindi hi-IN),
error handling, and thread-safe dispatching to the CommandHandler.
"""

import json
import socket
import threading
import time
from typing import Callable, Optional
import requests
import speech_recognition as sr

from command_handler import CommandHandler
from config import (
    DYNAMIC_ENERGY_THRESHOLD,
    ENERGY_THRESHOLD,
    RECOGNITION_TIMEOUT,
    SPEECH_PHRASE_TIME_LIMIT,
    SPEECH_RECOGNITION_TIMEOUT,
)

# Global socket timeout to prevent any thread from hanging indefinitely
socket.setdefaulttimeout(8.0)


class VoiceAssistant:
    """
    Manages continuous microphone listening and speech-to-text processing for VERONICA.
    Features:
    - Direct Linear PCM (audio/l16) + FLAC fallback - completely immune to flac-win32.exe WinError 623.
    - Dual language detection (en-IN first, then hi-IN).
    - Strict network timeouts so the Arc Reactor visualizer NEVER hangs or freezes.
    - Ambient noise threshold clamping to prevent infinite noise triggering.
    """

    def __init__(
        self,
        command_handler: CommandHandler,
        status_callback: Optional[Callable[[str, str], None]] = None,
        recognized_callback: Optional[Callable[[str], None]] = None,
    ):
        """
        Initialize the voice assistant.

        Args:
            command_handler (CommandHandler): Parser and dispatcher for speech commands.
            status_callback (Callable[[str, str], None]): Callback for status change (status_text, color_code).
            recognized_callback (Callable[[str], None]): Callback when user speech is transcribed.
        """
        self.command_handler = command_handler
        self.status_callback = status_callback
        self.recognized_callback = recognized_callback

        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = ENERGY_THRESHOLD
        self.recognizer.dynamic_energy_threshold = DYNAMIC_ENERGY_THRESHOLD
        self.recognizer.pause_threshold = 0.8  # seconds of non-speaking to consider end of phrase
        self.recognizer.operation_timeout = RECOGNITION_TIMEOUT

        self._is_listening = False
        self._stop_event = threading.Event()

    def set_status(self, status: str, color_key: str = "idle") -> None:
        """Helper to invoke GUI status callback."""
        if self.status_callback:
            try:
                self.status_callback(status, color_key)
            except Exception as e:
                print(f"[VoiceAssistant] Status callback error: {e}")

    def on_recognized(self, text: str) -> None:
        """Helper to notify GUI of recognized speech."""
        if self.recognized_callback:
            try:
                self.recognized_callback(text)
            except Exception as e:
                print(f"[VoiceAssistant] Recognized callback error: {e}")

    def is_active(self) -> bool:
        """Check if assistant listening loop is active."""
        return self._is_listening

    def start(self) -> None:
        """Start the listening thread."""
        if not self._is_listening:
            self._stop_event.clear()
            self._is_listening = True
            threading.Thread(target=self._listen_loop, daemon=True).start()

    def stop(self) -> None:
        """Signal the listening thread to stop gracefully."""
        self._stop_event.set()
        self._is_listening = False
        self.set_status("Standby // Disengaged", "idle")

    def _recognize_speech(self, audio: sr.AudioData) -> str:
        """
        Robustly transcribes audio using Google Speech Recognition API.
        Uses requests HTTPS POST with strict connect and read timeouts.
        Supports both raw 16-bit Linear PCM (audio/l16) and FLAC,
        bypassing legacy 32-bit flac.exe DLL relocation bugs on Windows 11.
        Tries en-IN (English/Indian accents/Hinglish) first, then hi-IN (Hindi).
        """
        # 1. Prepare audio payload (try FLAC safely; fallback to raw 16kHz 16-bit PCM)
        raw_pcm = audio.get_raw_data(convert_rate=16000, convert_width=2)
        flac_data = None
        try:
            flac_data = audio.get_flac_data(convert_rate=16000, convert_width=2)
        except Exception:
            flac_data = None

        if flac_data and len(flac_data) > 0:
            payload = flac_data
            content_type = "audio/x-flac; rate=16000"
        else:
            payload = raw_pcm
            content_type = "audio/l16; rate=16000"

        languages = ["en-IN", "hi-IN"]
        last_req_err = None

        for lang in languages:
            if self._stop_event.is_set():
                break

            url = (
                f"https://www.google.com/speech-api/v2/recognize?"
                f"client=chromium&lang={lang}&key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw&pFilter=0"
            )
            headers = {"Content-Type": content_type}

            try:
                resp = requests.post(
                    url,
                    data=payload,
                    headers=headers,
                    timeout=(3.5, 6.0),
                )
                if resp.status_code == 200:
                    for line in resp.text.splitlines():
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            data = json.loads(line)
                            results = data.get("result", [])
                            if results and len(results) > 0:
                                alts = results[0].get("alternative", [])
                                if alts and len(alts) > 0:
                                    transcript = alts[0].get("transcript", "").strip()
                                    if transcript:
                                        return transcript
                        except Exception:
                            continue
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as conn_err:
                last_req_err = conn_err
                # Network is unreachable or timed out; no need to retry second language
                break
            except Exception as e:
                last_req_err = e

        # 2. Secondary fallback via sr.Recognizer.recognize_google if requests didn't return
        if not last_req_err:
            try:
                return self.recognizer.recognize_google(audio, language="en-IN")
            except (sr.UnknownValueError, sr.RequestError):
                pass

        if last_req_err:
            raise sr.RequestError(f"Network error: {last_req_err}")

        raise sr.UnknownValueError("Speech was unintelligible")

    def _listen_loop(self) -> None:
        """
        Continuous listening loop.
        Calibrates for ambient noise, captures microphone audio,
        invokes robust speech recognition, and passes text to command handler.
        """
        try:
            mic = sr.Microphone()
        except Exception as mic_err:
            self.set_status(f"Microphone Offline: {mic_err}", "error")
            self._is_listening = False
            return

        with mic as source:
            self.set_status("Calibrating Acoustic Sensors...", "processing")
            try:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                # Clamp energy threshold to prevent infinite room noise triggers
                if self.recognizer.energy_threshold < 350:
                    self.recognizer.energy_threshold = 350
                elif self.recognizer.energy_threshold > 3500:
                    self.recognizer.energy_threshold = 3500
            except Exception as adj_err:
                print(f"[VoiceAssistant] Ambient adjustment warning: {adj_err}")

            self.set_status("Acoustic Sensor Online & Listening", "listening")

            while not self._stop_event.is_set():
                audio = None
                self.set_status("Listening for voice command...", "listening")

                try:
                    # Listen with timeout so we regularly check the stop event
                    audio = self.recognizer.listen(
                        source,
                        timeout=SPEECH_RECOGNITION_TIMEOUT,
                        phrase_time_limit=SPEECH_PHRASE_TIME_LIMIT,
                    )
                except sr.WaitTimeoutError:
                    # Timeout reached without speech; loop back to check stop_event
                    continue
                except Exception as listen_err:
                    if not self._stop_event.is_set():
                        print(f"[VoiceAssistant] Mic listen error: {listen_err}")
                    time.sleep(0.4)
                    continue

                if self._stop_event.is_set():
                    break

                if audio is not None:
                    self.set_status("Analyzing Speech Pattern...", "processing")
                    try:
                        recognized_text = self._recognize_speech(audio)
                        print(f"[VoiceAssistant] Recognized: {recognized_text}")

                        # Update GUI with recognized user text
                        self.on_recognized(recognized_text)

                        # Process command & speak response
                        self.set_status("Veronica Speaking...", "speaking")
                        continue_listening, _ = self.command_handler.process(recognized_text)

                        if not continue_listening:
                            self.stop()
                            break

                    except sr.UnknownValueError:
                        print("[VoiceAssistant] Speech was unclear.")
                        self.on_recognized("[Speech Unclear // Awaiting Input]")
                        self.set_status("Speech Unclear // Awaiting Input", "idle")
                        time.sleep(0.5)

                    except sr.RequestError as req_err:
                        err_msg = "Network Unreachable: Speech Service Offline."
                        print(f"[VoiceAssistant] {err_msg} ({req_err})")
                        self.on_recognized(f"[{err_msg}]")
                        self.set_status(err_msg, "error")
                        if self.command_handler.speech_engine:
                            self.command_handler.speech_engine.speak(
                                "I am having trouble reaching the speech recognition servers, sir. Please verify your internet connection.",
                                block=False,
                            )
                        time.sleep(1.0)

                    except Exception as gen_err:
                        print(f"[VoiceAssistant] Error during recognition processing: {gen_err}")
                        self.on_recognized(f"[Recognition Anomaly: {gen_err}]")
                        self.set_status("Processing Anomaly Detected", "error")
                        time.sleep(0.5)

        self._is_listening = False
        self.set_status("Standby // Disengaged", "idle")
