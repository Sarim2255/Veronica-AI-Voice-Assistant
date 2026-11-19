import os
import subprocess
import urllib.parse
import webbrowser
from typing import Tuple

from config import APP_COMMANDS, WEBSITE_URLS


def open_website(site_key: str) -> Tuple[bool, str]:

    key = site_key.lower().strip()
    url = WEBSITE_URLS.get(key)

    if not url:
    
        normalized_key = key.replace(" ", "")
        for k, v in WEBSITE_URLS.items():
            if k.replace(" ", "") == normalized_key:
                url = v
                break

    if url:
        try:
            webbrowser.open_new_tab(url)
            return True, f"Opening {site_key.title()} in your browser."
        except Exception as e:
            return False, f"Failed to open {site_key}. Error: {str(e)}"

    return False, f"Website '{site_key}' is not in the supported list."


def launch_application(app_name: str) -> Tuple[bool, str]:

    name = app_name.lower().strip()
    cmd = APP_COMMANDS.get(name)

    if not cmd:
        # Check partial match
        for k, v in APP_COMMANDS.items():
            if k in name or name in k:
                cmd = v
                name = k
                break

    if not cmd:
        return False, f"Application '{app_name}' is not configured for automatic launch."

    try:

        if cmd.startswith("ms-settings:"):
            os.system(f"start {cmd}")
        elif cmd == "code":

            subprocess.Popen("code", shell=True)
        elif cmd == "cmd.exe":
            subprocess.Popen("start cmd.exe", shell=True)
        else:
            subprocess.Popen(cmd, shell=True)

        return True, f"Launching {name.title()}."
    except FileNotFoundError:
        return False, f"Could not find executable for {name}. Please ensure it is installed and in PATH."
    except Exception as exc:
        return False, f"An error occurred while launching {name}: {str(exc)}"


def play_youtube(query: str) -> Tuple[bool, str]:

    clean_query = query.strip()
    if not clean_query:
        return False, "Please specify what you would like to play on YouTube."

    try:
        import pywhatkit
        pywhatkit.playonyt(clean_query)
        return True, f"Playing '{clean_query}' on YouTube."
    except Exception:
        # Graceful fallback: Open YouTube search results directly
        try:
            encoded_query = urllib.parse.quote(clean_query)
            search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            webbrowser.open_new_tab(search_url)
            return True, f"Opened YouTube search for '{clean_query}'."
        except Exception as e:
            return False, f"Could not open YouTube: {str(e)}"


def google_search(query: str) -> Tuple[bool, str]:

    clean_query = query.strip()
    if not clean_query:
        return False, "Please specify what you would like to search for."

    try:
        encoded_query = urllib.parse.quote(clean_query)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        webbrowser.open_new_tab(search_url)
        return True, f"Searching Google for '{clean_query}'."
    except Exception as e:
        return False, f"Failed to execute Google search: {str(e)}"


def open_new_tab(url: str = "https://www.google.com") -> Tuple[bool, str]:

    try:
        webbrowser.open_new_tab(url)
        return True, "Opening a new browser tab."
    except Exception as e:
        return False, f"Could not open a new browser tab: {str(e)}"