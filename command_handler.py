import datetime
import re
from typing import Callable, Optional, Tuple

from automation import (
    google_search,
    launch_application,
    open_new_tab,
    open_website,
    play_youtube,
)
from config import APP_COMMANDS, ASSISTANT_NAME, WEBSITE_URLS


class CommandHandler:

    def __init__(
        self,
        speech_engine,
        ui_callback: Optional[Callable[[str], None]] = None,
        on_exit_callback: Optional[Callable[[], None]] = None,
        on_clear_callback: Optional[Callable[[], None]] = None,
    ):
        self.speech_engine = speech_engine
        self.ui_callback = ui_callback
        self.on_exit_callback = on_exit_callback
        self.on_clear_callback = on_clear_callback
        self.last_response: str = f"Systems initialized. I am {ASSISTANT_NAME}, ready for your command, sir."

    def _respond(self, message: str) -> str:

        self.last_response = message
        if self.ui_callback:
            try:
                self.ui_callback(message)
            except Exception as e:
                print(f"[CommandHandler] UI callback error: {e}")

        if self.speech_engine:
            self.speech_engine.speak(message, block=True)
        return message

    def preprocess_command(self, raw_command: str) -> str:

        if not raw_command:
            return ""

        text = raw_command.lower().strip()

        text = re.sub(r"[?!.,]", "", text)

        prefixes = [
            r"^hey\s+veronica\s*,?\s*",
            r"^hello\s+veronica\s*,?\s*",
            r"^ok\s+veronica\s*,?\s*",
            r"^okay\s+veronica\s*,?\s*",
            r"^veronica\s*,?\s*",
            r"^वेरोनिका\s*,?\s*",
            r"^hey\s+jarvis\s*,?\s*",
            r"^hello\s+jarvis\s*,?\s*",
            r"^ok\s+jarvis\s*,?\s*",
            r"^okay\s+jarvis\s*,?\s*",
            r"^jarvis\s*,?\s*",
            r"^जार्विस\s*,?\s*",
            r"^सुनो\s*,?\s*",
            r"^कृपया\s*,?\s*",
            r"^can\s+you\s+please\s+",
            r"^could\s+you\s+please\s+",
            r"^can\s+you\s+",
            r"^could\s+you\s+",
            r"^please\s+",
            r"^would\s+you\s+",
            r"^tell\s+me\s+",
            r"^batao\s+",
            r"^bataiye\s+",
        ]
        for pattern in prefixes:
            text = re.sub(pattern, "", text)

        return text.strip()

    def _try_simple_math(self, text: str) -> Optional[str]:

        math_text = text.lower()
        if not any(k in math_text for k in ["calculate", "plus", "minus", "times", "divided by", "multiplied by", "+", "-", "*", "/"]):
            return None

        s = math_text.replace("calculate", "").replace("what is", "").strip()
        s = s.replace("plus", "+").replace("add", "+")
        s = s.replace("minus", "-").replace("subtract", "-")
        s = s.replace("times", "*").replace("multiplied by", "*").replace("into", "*").replace("x", "*")
        s = s.replace("divided by", "/").replace("divide by", "/")


        clean_expr = re.sub(r"[^0-9\+\-\*\/\.\(\) ]", "", s).strip()
        if clean_expr and any(op in clean_expr for op in ["+", "-", "*", "/"]):
            try:

                if re.match(r"^[\d\s\+\-\*\/\.\(\)]+$", clean_expr):
                    result = eval(clean_expr, {"__builtins__": None}, {})
                    if isinstance(result, float) and result.is_integer():
                        result = int(result)
                    return f"The calculated result is {result}, sir."
            except Exception:
                pass
        return None

    def _try_wikipedia(self, query: str) -> Optional[str]:

        try:
            import wikipedia
            wikipedia.set_lang("en")

            summary = wikipedia.summary(query, sentences=2, auto_suggest=False)
            if summary:

                clean = re.sub(r"\[\d+\]", "", summary).strip()
                return f"According to Wikipedia: {clean}"
        except Exception:
            pass
        return None

    def process(self, raw_text: str) -> Tuple[bool, str]:

        if not raw_text or not raw_text.strip():
            return True, ""

        command = self.preprocess_command(raw_text)

        # 1. Exit / Goodbye / Stop Listening
        exit_terms = [
            "exit", "quit", "goodbye", "bye", "shutdown", "stop listening",
            "terminate", "power down", "बंद करो", "अलविदा", "बंद हो जाओ",
            "रुक जाओ", "चुप हो जाओ", "band karo", "alvida", "chup", "stop"
        ]
        if any(w in command for w in exit_terms):
            farewell = f"Goodbye, sir. Deactivating Veronica systems. Have a wonderful day!"
            self._respond(farewell)
            if self.on_exit_callback:
                self.on_exit_callback()
            return False, farewell

        # 2. Clear HUD / Screen
        clear_terms = [
            "clear history", "clear command history", "clear screen", "clear hud",
            "clear", "साफ करो", "स्क्रीन साफ करो", "क्लियर करो", "clear karo"
        ]
        if any(w in command for w in clear_terms):
            if self.on_clear_callback:
                self.on_clear_callback()
            msg = "Tactical HUD and transaction history have been cleared, sir."
            self._respond(msg)
            return True, msg

        # 3. Repeat Last Statement
        repeat_terms = [
            "repeat", "repeat that", "what did you say", "say again",
            "repeat last", "फिर से बोलो", "दोबारा बोलो", "phir se bolo"
        ]
        if any(w in command for w in repeat_terms):
            msg = f"I said: {self.last_response}"
            self._respond(msg)
            return True, msg

        # 4. Greetings & Conversational Queries
        greet_terms = [
            "hello", "hi", "hey", "नमस्ते", "नमस्कार", "प्रणाम",
            "सुप्रभात", "kya haal", "kaise ho", "shubh prabhat"
        ]
        if any(g in command for g in greet_terms):
            hour = datetime.datetime.now().hour
            if hour < 12:
                greeting = "Good morning!"
            elif hour < 17:
                greeting = "Good afternoon!"
            else:
                greeting = "Good evening!"
            msg = f"{greeting} I am {ASSISTANT_NAME}. All orbital and HUD systems are fully operational. How may I assist you, sir?"
            self._respond(msg)
            return True, msg

        if any(h in command for h in ["how are you", "कैसी हो", "आप कैसी हैं", "kya haal hai"]):
            msg = "All systems are operating at peak efficiency, sir. Ready for your command."
            self._respond(msg)
            return True, msg

        who_terms = [
            "who are you", "what is your name", "introduce yourself",
            "तुम कौन हो", "तुम्हारा नाम क्या है", "आप कौन हैं", "tum kaun ho", "naam kya hai"
        ]
        if any(w in command for w in who_terms):
            msg = f"I am {ASSISTANT_NAME}, your personal tactical AI voice assistant, engineered with full voice synthesis and desktop automation."
            self._respond(msg)
            return True, msg

        if any(k in command for k in ["status", "system status", "diagnostics", "system check", "सिस्टम स्टेटस", "हालत", "status batao"]):
            msg = f"All systems nominal, sir. SAPI-5 female voice synthesis synchronized, acoustic sensors active, core efficiency at 99.8%."
            self._respond(msg)
            return True, msg

        # 5. Help / Capabilities
        if any(w in command for w in ["help", "what can you do", "commands", "show commands", "मदद", "क्या कर सकती हो", "kya kar sakti ho"]):
            help_msg = (
                "I am Veronica, your tactical voice assistant. Here is what I can do:\n"
                "1. Open websites: YouTube, Google, Gmail, GitHub, LinkedIn, Stack Overflow, etc.\n"
                "2. Launch applications: Notepad, Calculator, Paint, Command Prompt, VS Code, Settings.\n"
                "3. Media: Play any song or artist on YouTube (e.g. 'Play Believer').\n"
                "4. Search: Perform real-time Google web searches.\n"
                "5. Utilities: Report current time, date, and day of the week aloud.\n"
                "6. General Knowledge: Answer questions via Wikipedia and solve basic calculations.\n"
                "7. Bilingual: Responds to English, Hindi, and Hinglish voice or typed commands."
            )
            spoken_help = (
                "I am Veronica. I can launch applications, open websites, play music on YouTube, "
                "search Google, report current time and date, and answer questions in English and Hindi. "
                "How may I assist you, sir?"
            )
            self.last_response = help_msg
            if self.ui_callback:
                self.ui_callback(help_msg)
            if self.speech_engine:
                self.speech_engine.speak(spoken_help, block=True)
            return True, help_msg

        # 6. Date & Time Commands (Spoken aloud via TTS)
        time_terms = ["time", "समय", "टाइम", "वक्त", "कितने बजे", "samay", "kitne baje"]
        if any(t in command for t in time_terms) and not any(k in command for k in ["play", "search", "बजाओ"]):
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            msg = f"The current time is {current_time}, sir."
            self._respond(msg)
            return True, msg

        date_terms = ["date", "today's date", "todays date", "तारीख", "आज क्या तारीख", "आज की तारीख", "taarikh", "aaj ki date"]
        if any(d in command for d in date_terms):
            current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            msg = f"Today's date is {current_date}, sir."
            self._respond(msg)
            return True, msg

        if re.search(r"\bday\b", command) or "दिन" in command or "aaj kaun sa din" in command:
            current_day = datetime.datetime.now().strftime("%A")
            msg = f"Today is {current_day}, sir."
            self._respond(msg)
            return True, msg

        # 7. Math calculations
        math_res = self._try_simple_math(command)
        if math_res:
            self._respond(math_res)
            return True, math_res

        # 8. New browser tab
        if "new tab" in command or "open a new tab" in command or "नया टैब" in command:
            success, msg = open_new_tab()
            self._respond(msg)
            return True, msg

        # 9. YouTube Video / Song Playback
        yt_triggers = ["play ", "play on youtube", "youtube play", "गाना चलाओ", "गाना बजाओ", "यूट्यूब पर चलाओ", "play karo", "gana chalao", "song bajao"]
        if any(t in command for t in yt_triggers):
            query = command
            for word in yt_triggers + ["play on youtube", "play youtube", "play", "on youtube", "youtube", "गाना चलाओ", "गाना बजाओ", "बजाओ", "चलाओ"]:
                query = query.replace(word, "")
            query = query.strip()

            if query:
                success, msg = play_youtube(query)
                self._respond(msg)
            else:
                msg = "What song or video would you like me to play on YouTube, sir?"
                self._respond(msg)
            return True, msg

        # 10. Google Search
        search_triggers = ["search ", "google ", "search for ", "सर्च करो", "गूगल सर्च", "ढूंढो", "search karo"]
        if any(command.startswith(st) or st in command for st in search_triggers):
            query = command
            for word in ["google search", "search google", "search for", "search", "google", "on google", "गूगल सर्च", "सर्च करो", "ढूंढो", "search karo"]:
                query = query.replace(word, "")
            query = query.strip()

            if query:
                success, msg = google_search(query)
                self._respond(msg)
            else:
                msg = "What query would you like to search on Google, sir?"
                self._respond(msg)
            return True, msg

        # 11. Website & Application Automation (English & Hindi support)
        # Normalization dictionary for Hindi app/site names
        hindi_map = {
            "यूट्यूब": "youtube", "गूगल": "google", "जीमेल": "gmail",
            "कैलकुलेटर": "calculator", "नोटपैड": "notepad", "पेंट": "paint",
            "सेटिंग्स": "settings", "कोड": "vs code", "विजुअल स्टूडियो": "vs code",
            "फ़ाइल एक्सप्लोरर": "explorer", "कमांड प्रॉम्प्ट": "cmd",
        }
        normalized_command = command
        for h_k, h_v in hindi_map.items():
            if h_k in normalized_command:
                normalized_command = normalized_command.replace(h_k, h_v)

        is_open_intent = (
            normalized_command.startswith("open ")
            or normalized_command.startswith("launch ")
            or normalized_command.startswith("start ")
            or "खोलो" in normalized_command
            or "ओपन करो" in normalized_command
            or "chalao" in normalized_command
            or "kholo" in normalized_command
        )

        if is_open_intent:
            target = normalized_command
            for kw in ["open", "launch", "start", "खोलो", "ओपन करो", "chalao", "kholo"]:
                target = target.replace(kw, "")
            target = target.strip()

            # Check supported websites first
            matched_site = None
            for site in WEBSITE_URLS.keys():
                if site in target or (target and target in site):
                    matched_site = site
                    break

            if matched_site:
                success, msg = open_website(matched_site)
                self._respond(msg)
                return True, msg

            # Check supported desktop applications
            matched_app = None
            for app in APP_COMMANDS.keys():
                if app in target or (target and target in app):
                    matched_app = app
                    break

            if matched_app:
                success, msg = launch_application(matched_app)
                self._respond(msg)
                return True, msg

            # If general domain like amazon.com or reddit
            if "." in target or "com" in target or "org" in target:
                web_url = target if target.startswith("http") else f"https://{target}"
                try:
                    import webbrowser
                    webbrowser.open_new_tab(web_url)
                    msg = f"Opening {target} in your browser, sir."
                    self._respond(msg)
                    return True, msg
                except Exception:
                    pass

            if target:
                # Fallback: search Google for the target
                google_search(target)
                msg = f"Opening search results for '{target}', sir."
                self._respond(msg)
                return True, msg

        # 12. Direct desktop app mention without 'open'
        for app in APP_COMMANDS.keys():
            if command == app or f"launch {app}" in command or f"start {app}" in command:
                success, msg = launch_application(app)
                self._respond(msg)
                return True, msg

        # 13. General Knowledge / Wikipedia Queries
        wiki_triggers = ["who is ", "what is ", "tell me about ", "wikipedia ", "explain ", "कौन है", "क्या है", "के बारे में बताओ"]
        if any(prefix in command for prefix in wiki_triggers):
            wiki_query = command
            for prefix in ["who is", "what is", "tell me about", "wikipedia", "explain", "कौन है", "क्या है", "के बारे में बताओ"]:
                wiki_query = wiki_query.replace(prefix, "")
            wiki_query = wiki_query.strip()

            if wiki_query:
                wiki_answer = self._try_wikipedia(wiki_query)
                if wiki_answer:
                    self._respond(wiki_answer)
                    return True, wiki_answer
                else:
                    google_search(wiki_query)
                    msg = f"I have opened Google search results for '{wiki_query}', sir."
                    self._respond(msg)
                    return True, msg

        # 14. Fallback for unrecognized commands
        fallback_msg = (
            f"I recognized: '{raw_text}', sir. "
            "You can say 'help' to review my capabilities, or try asking for the time, date, or opening YouTube."
        )
        self._respond(fallback_msg)
        return True, fallback_msg
