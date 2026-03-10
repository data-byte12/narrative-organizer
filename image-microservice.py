"""
Image Storage Microservice
--------------------------
Communication: file-based JSON IPC (same pattern as all other microservices)

Request file:  ./image-storage/request.json
Response file: ./image-storage/response.json

Actions
-------
store   - copy an image into local storage
display - render image in the terminal (requires Pillow: pip install Pillow)
open    - open image with the system default viewer (macOS: 'open', Windows: 'start')
list    - list all stored images
delete  - remove a stored image

Request / Response examples
----------------------------
{"action": "store",   "source_path": "/path/to/photo.png", "name": "photo"}
{"action": "display", "name": "photo", "width": 80}        # width optional, default 80
{"action": "open",    "name": "photo"}
{"action": "list"}
{"action": "delete",  "name": "photo"}

All responses:
{"status": "success", "result": <string or list>}
{"status": "error",   "result": <error message>}
"""

import json
import os
import shutil
import subprocess
import sys
import time

# ── Paths ──────────────────────────────────────────────────────────────────────
SERVICE_DIR   = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR   = os.path.join(SERVICE_DIR, "stored_images")
REQUEST_FILE  = os.path.join(SERVICE_DIR, "image-request.json")
RESPONSE_FILE = os.path.join(SERVICE_DIR, "image-response.json")

os.makedirs(STORAGE_DIR, exist_ok=True)

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tiff", ".ico"}


# ── Helpers ────────────────────────────────────────────────────────────────────

def respond(status, result):
    with open(RESPONSE_FILE, "w") as f:
        json.dump({"status": status, "result": result}, f, indent=4)


def stored_path(name):
    """Return the full path for a stored image name (searches for any extension)."""
    for fname in os.listdir(STORAGE_DIR):
        base, _ = os.path.splitext(fname)
        if base == name:
            return os.path.join(STORAGE_DIR, fname)
    return None


# ── Actions ────────────────────────────────────────────────────────────────────

def action_store(data):
    source = data.get("source_path", "").strip()
    name   = data.get("name", "").strip()

    if not source or not name:
        return respond("error", "Both 'source_path' and 'name' are required.")

    source = os.path.normpath(source)
    if not os.path.isfile(source):
        return respond("error", f"File not found: {source}")

    ext = os.path.splitext(source)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        return respond("error", f"Unsupported file type '{ext}'. Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}")

    dest = os.path.join(STORAGE_DIR, name + ext)
    shutil.copy2(source, dest)
    respond("success", f"Image stored as '{name}' ({os.path.basename(dest)}).")


def action_display(data):
    name  = data.get("name", "").strip()
    width = int(data.get("width", 80))

    if not name:
        return respond("error", "'name' is required.")

    path = stored_path(name)
    if path is None:
        return respond("error", f"No stored image named '{name}'.")

    try:
        from PIL import Image
    except ImportError:
        return respond("error", "Pillow is not installed. Run: pip install Pillow")

    img = Image.open(path).convert("RGB")
    # Each terminal "pixel" is 2 rows tall (▀ / ▄), so height = width * aspect / 2
    orig_w, orig_h = img.size
    height = max(1, int(orig_h / orig_w * width * 0.45))
    img = img.resize((width, height * 2), Image.LANCZOS)

    lines = []
    pixels = list(img.getdata())
    for row in range(height):
        line = ""
        for col in range(width):
            top_idx = (row * 2)     * width + col
            bot_idx = (row * 2 + 1) * width + col
            tr, tg, tb = pixels[top_idx]
            br, bg, bb = pixels[bot_idx]
            # Top color = foreground (▀), bottom = background
            line += f"\033[38;2;{tr};{tg};{tb}m\033[48;2;{br};{bg};{bb}m▀\033[0m"
        lines.append(line)

    terminal_art = "\n".join(lines)
    print(terminal_art)
    respond("success", f"Image '{name}' displayed in terminal ({width} cols × {height * 2} rows).")


def action_open(data):
    name = data.get("name", "").strip()
    if not name:
        return respond("error", "'name' is required.")

    path = stored_path(name)
    if path is None:
        return respond("error", f"No stored image named '{name}'.")

    if sys.platform == "darwin":
        subprocess.Popen(["open", path])
    elif sys.platform == "win32":
        os.startfile(path)
    else:
        subprocess.Popen(["xdg-open", path])

    respond("success", f"Opened '{name}' with the system viewer.")


def action_list(_data):
    files = sorted(os.listdir(STORAGE_DIR))
    if not files:
        return respond("success", [])
    names = [os.path.splitext(f)[0] for f in files if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS]
    respond("success", names)


def action_delete(data):
    name = data.get("name", "").strip()
    if not name:
        return respond("error", "'name' is required.")

    path = stored_path(name)
    if path is None:
        return respond("error", f"No stored image named '{name}'.")

    os.remove(path)
    respond("success", f"Image '{name}' deleted.")


# ── Dispatch ───────────────────────────────────────────────────────────────────

ACTIONS = {
    "store":   action_store,
    "display": action_display,
    "open":    action_open,
    "list":    action_list,
    "delete":  action_delete,
}


# ── Main loop ─────────────────────────────────────────────────────────────────

def main():
    print("Image Storage Microservice running...")
    print(f"  Storage directory : {STORAGE_DIR}")
    print(f"  Watching for      : {REQUEST_FILE}")

    while True:
        try:
            with open(REQUEST_FILE, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            time.sleep(0.1)
            continue

        os.remove(REQUEST_FILE)

        action = data.get("action", "").strip().lower()
        handler = ACTIONS.get(action)
        if handler:
            handler(data)
        else:
            respond("error", f"Unknown action '{action}'. Valid actions: {', '.join(sorted(ACTIONS))}")


if __name__ == "__main__":
    main()
