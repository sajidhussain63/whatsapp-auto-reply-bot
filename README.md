# WhatsApp Auto-Reply Bot

A mini-project that automates WhatsApp Web using screen automation (PyAutoGUI):
it copies the latest message from a chat, generates a short reply using
Cohere's language model, and sends it back automatically.

## How it works

1. Clicks/focuses the WhatsApp Web window.
2. Drag-selects the latest message text and copies it to the clipboard.
3. Sends that text to Cohere's `generate` API with a short-reply prompt.
4. Pastes the generated reply into the WhatsApp message box and sends it.
5. Repeats on a loop.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Get a Cohere API key

Sign up at [cohere.com](https://cohere.com) and grab an API key from your dashboard.

### 3. Set the API key as an environment variable

**Never hardcode the key in the script.** Set it in your shell:

```bash
# macOS/Linux
export COHERE_API_KEY="your-key-here"

# Windows (PowerShell)
$env:COHERE_API_KEY="your-key-here"
```

Or create a `.env` file locally (already git-ignored) and load it with
[`python-dotenv`](https://pypi.org/project/python-dotenv/) if you prefer.

### 4. Calibrate screen coordinates ⚠️

The script uses hardcoded screen coordinates to click and drag on specific
parts of your screen — these are **specific to the original author's
screen resolution and window layout** and will not work as-is on your
machine.

To find your own coordinates, run:

```python
import pyautogui, time
time.sleep(3)  # move your mouse to the target spot during this delay
print(pyautogui.position())
```

Update the `CONFIG` section at the top of `whatsapp_bot.py` with your values:
- `ICON_POSITION` — where to click to focus the WhatsApp Web window
- `DRAG_START` / `DRAG_END` — drag range to select the latest message
- `DESELECT_CLICK` — an empty area to click to clear the selection
- `TEXTBOX_POSITION` — the WhatsApp message input box
- `SEND_BUTTON_POSITION` — the send button

### 5. Run it

```bash
python whatsapp_bot.py
```

Stop it anytime with `Ctrl+C`.

## ⚠️ Disclaimer

- This is a personal/educational project. Automating WhatsApp Web through
  GUI scripting is not officially supported by WhatsApp.
- Auto-replying on someone's behalf without their knowledge can raise
  consent and privacy concerns — use responsibly and only on chats/accounts
  you have permission to automate.
- The script relies on fragile screen-coordinate clicks; UI changes,
  popups, or notifications on your screen can cause it to misclick or
  paste text in the wrong place.

## Tech stack

- [PyAutoGUI](https://pyautogui.readthedocs.io/) — GUI automation
- [Pyperclip](https://pypi.org/project/pyperclip/) — clipboard access
- [Cohere](https://docs.cohere.com/) — language model for generating replies
