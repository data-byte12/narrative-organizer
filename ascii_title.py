import json
import time
import os

# ASCII art font - each letter is 5 lines tall
ASCII_FONT = {
    'A': [
        "  █  ",
        " █ █ ",
        "█████",
        "█   █",
        "█   █"
    ],
    'B': [
        "████ ",
        "█   █",
        "████ ",
        "█   █",
        "████ "
    ],
    'C': [
        " ████",
        "█    ",
        "█    ",
        "█    ",
        " ████"
    ],
    'D': [
        "████ ",
        "█   █",
        "█   █",
        "█   █",
        "████ "
    ],
    'E': [
        "█████",
        "█    ",
        "████ ",
        "█    ",
        "█████"
    ],
    'F': [
        "█████",
        "█    ",
        "████ ",
        "█    ",
        "█    "
    ],
    'G': [
        " ████",
        "█    ",
        "█  ██",
        "█   █",
        " ████"
    ],
    'H': [
        "█   █",
        "█   █",
        "█████",
        "█   █",
        "█   █"
    ],
    'I': [
        "█████",
        "  █  ",
        "  █  ",
        "  █  ",
        "█████"
    ],
    'J': [
        "█████",
        "   █ ",
        "   █ ",
        "█  █ ",
        " ██  "
    ],
    'K': [
        "█   █",
        "█  █ ",
        "███  ",
        "█  █ ",
        "█   █"
    ],
    'L': [
        "█    ",
        "█    ",
        "█    ",
        "█    ",
        "█████"
    ],
    'M': [
        "█   █",
        "██ ██",
        "█ █ █",
        "█   █",
        "█   █"
    ],
    'N': [
        "█   █",
        "██  █",
        "█ █ █",
        "█  ██",
        "█   █"
    ],
    'O': [
        " ███ ",
        "█   █",
        "█   █",
        "█   █",
        " ███ "
    ],
    'P': [
        "████ ",
        "█   █",
        "████ ",
        "█    ",
        "█    "
    ],
    'Q': [
        " ███ ",
        "█   █",
        "█   █",
        "█  █ ",
        " ██ █"
    ],
    'R': [
        "████ ",
        "█   █",
        "████ ",
        "█  █ ",
        "█   █"
    ],
    'S': [
        " ████",
        "█    ",
        " ███ ",
        "    █",
        "████ "
    ],
    'T': [
        "█████",
        "  █  ",
        "  █  ",
        "  █  ",
        "  █  "
    ],
    'U': [
        "█   █",
        "█   █",
        "█   █",
        "█   █",
        " ███ "
    ],
    'V': [
        "█   █",
        "█   █",
        "█   █",
        " █ █ ",
        "  █  "
    ],
    'W': [
        "█   █",
        "█   █",
        "█ █ █",
        "██ ██",
        "█   █"
    ],
    'X': [
        "█   █",
        " █ █ ",
        "  █  ",
        " █ █ ",
        "█   █"
    ],
    'Y': [
        "█   █",
        " █ █ ",
        "  █  ",
        "  █  ",
        "  █  "
    ],
    'Z': [
        "█████",
        "   █ ",
        "  █  ",
        " █   ",
        "█████"
    ],
    '0': [
        " ███ ",
        "█  ██",
        "█ █ █",
        "██  █",
        " ███ "
    ],
    '1': [
        "  █  ",
        " ██  ",
        "  █  ",
        "  █  ",
        "█████"
    ],
    '2': [
        " ███ ",
        "█   █",
        "  ██ ",
        " █   ",
        "█████"
    ],
    '3': [
        "████ ",
        "    █",
        " ███ ",
        "    █",
        "████ "
    ],
    '4': [
        "█   █",
        "█   █",
        "█████",
        "    █",
        "    █"
    ],
    '5': [
        "█████",
        "█    ",
        "████ ",
        "    █",
        "████ "
    ],
    '6': [
        " ███ ",
        "█    ",
        "████ ",
        "█   █",
        " ███ "
    ],
    '7': [
        "█████",
        "    █",
        "   █ ",
        "  █  ",
        "  █  "
    ],
    '8': [
        " ███ ",
        "█   █",
        " ███ ",
        "█   █",
        " ███ "
    ],
    '9': [
        " ███ ",
        "█   █",
        " ████",
        "    █",
        " ███ "
    ],
    ' ': [
        "     ",
        "     ",
        "     ",
        "     ",
        "     "
    ],
    '!': [
        "  █  ",
        "  █  ",
        "  █  ",
        "     ",
        "  █  "
    ],
    '?': [
        " ███ ",
        "█   █",
        "  █  ",
        "     ",
        "  █  "
    ],
    '-': [
        "     ",
        "     ",
        "█████",
        "     ",
        "     "
    ],
    '.': [
        "     ",
        "     ",
        "     ",
        "     ",
        "  █  "
    ]
}


def text_to_ascii(text):
    """Convert text to ASCII art."""
    text = text.upper()
    lines = ["", "", "", "", ""]

    for char in text:
        if char in ASCII_FONT:
            for i in range(5):
                lines[i] += ASCII_FONT[char][i] + " "
        else:
            # Unknown character - use space
            for i in range(5):
                lines[i] += "     " + " "

    return "\n".join(lines)


def write_response(response_data):
    with open(response_path, "w") as f:
        json.dump(response_data, f, indent=4)
    os.remove(request_path)


# The microservice works inside its own directory
service_dir = "."
request_path = os.path.join(service_dir, "title-request.json")
response_path = os.path.join(service_dir, "title-response.json")

print("ASCII Title microservice running...")

while True:
    try:
        with open(request_path, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        time.sleep(0.1)
        continue

    text = data.get("text")

    # Validate input
    if not isinstance(text, str):
        response_data = {
            "result": "Error: text must be a string."
        }
        write_response(response_data)
        continue

    if len(text) > 20:
        response_data = {
            "result": "Error: text must be 20 characters or less."
        }
        write_response(response_data)
        continue

    ascii_art = text_to_ascii(text)

    response_data = {
        "result": ascii_art
    }
    write_response(response_data)
