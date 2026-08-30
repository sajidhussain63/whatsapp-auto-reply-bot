"""
WhatsApp Auto-Reply Bot
------------------------
Uses PyAutoGUI to read the latest message from a WhatsApp Web chat window,
sends it to Cohere's language model to generate a short reply, and pastes
the reply back into the chat.

IMPORTANT SETUP NOTES:
1. This script relies on hardcoded screen coordinates (see CONFIG section
   below). These WILL be different on your screen/window layout. Run the
   position-finder snippet at the bottom of this file to recalibrate.
2. Requires WhatsApp Web open in your browser, positioned consistently.
3. Set your Cohere API key as an environment variable (see README.md) —
   never hardcode it in this file.
4. Educational / personal use only. Automating WhatsApp Web via GUI
   scripting is not officially supported by WhatsApp, and auto-replying
   on someone's behalf without their knowledge can raise consent issues.
"""

import os
import time

import pyautogui
import pyperclip
import cohere
from dotenv import load_dotenv

load_dotenv()  # loads variables from a local .env file, if present

# ── CONFIG: screen coordinates (recalibrate for your own screen) ──────────
ICON_POSITION = (1302, 1057)      # icon/app to click to focus the window
DRAG_START = (920, 258)           # start of text selection drag
DRAG_END = (1752, 1008)           # end of text selection drag
DESELECT_CLICK = (906, 544)       # empty area to click to deselect text
TEXTBOX_POSITION = (1054, 971)    # WhatsApp message input box
SEND_BUTTON_POSITION = (1859, 965)  # send button

# ── CONFIG: behavior ────────────────────────────────────────────────────
POLL_INTERVAL_SECONDS = 5
COHERE_MODEL = "command-xlarge"
MAX_REPLY_TOKENS = 100

PROMPT_TEMPLATE = (
    "You are me, replying to a friend in a casual chat. Don't mention "
    "your own name or your friend's name. Keep the answer as short as "
    "possible while still being a real reply.\n\n"
    "Message: {message}\n"
    "Response:"
)


def get_api_key() -> str:
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError(
            "COHERE_API_KEY environment variable is not set. "
            "See README.md for setup instructions."
        )
    return api_key


def generate_reply(client: cohere.Client, message: str) -> str | None:
    """Ask Cohere for a short reply to the given message."""
    try:
        response = client.generate(
            model=COHERE_MODEL,
            prompt=PROMPT_TEMPLATE.format(message=message),
            max_tokens=MAX_REPLY_TOKENS,
        )
        return response.generations[0].text.strip()
    except cohere.errors.UnauthorizedError as e:
        print(f"Authentication error (check your API key): {e}")
    except Exception as e:
        print(f"Error generating reply: {e}")
    return None


def copy_latest_message() -> str:
    """Select and copy the latest visible message text via drag-select."""
    pyautogui.click(DRAG_START)
    pyautogui.moveTo(DRAG_START)
    pyautogui.dragTo(DRAG_END, duration=1.0, button="left")
    pyautogui.hotkey("ctrl", "c")
    pyautogui.click(DESELECT_CLICK)  # deselect so it doesn't stay highlighted
    time.sleep(POLL_INTERVAL_SECONDS)
    return pyperclip.paste()


def send_reply(text: str) -> None:
    pyperclip.copy(text)
    pyautogui.click(TEXTBOX_POSITION)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.click(SEND_BUTTON_POSITION)


def main() -> None:
    client = cohere.Client(get_api_key())

    print("Focusing WhatsApp Web window...")
    time.sleep(2)
    pyautogui.moveTo(ICON_POSITION)
    pyautogui.click()

    print("Starting auto-reply loop. Press Ctrl+C to stop.")
    while True:
        copied_text = copy_latest_message()
        print("Copied Text:", copied_text)

        if not copied_text.strip():
            continue

        reply = generate_reply(client, copied_text)
        if reply:
            send_reply(reply)
        else:
            print("Skipping send — no reply was generated.")


if __name__ == "__main__":
    main()

    # ── Coordinate finder (run separately, not as part of the loop) ──────
    # Uncomment and run this to find coordinates for your own screen:
    #
    # import pyautogui, time
    # time.sleep(3)  # move your mouse to the target spot during this delay
    # print(pyautogui.position())
